# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import cos, pow, radians, sin, tan

from .astrometry import get_obliquity_of_the_ecliptic
from .common import EquatorialCoordinate
from .earth import get_eccentricity_of_orbit
from .moon import (
    get_mean_ecliptic_longitude_of_the_ascending_node as get_lunar_mean_ecliptic_longitude_of_the_ascending_node,
)
from .moon import get_mean_geometric_longitude as get_lunar_mean_geometric_longitude
from .sun import get_mean_geometric_longitude as get_solar_mean_geometric_longitude
from .sun import get_true_geometric_longitude as get_solar_true_geometric_longitude
from .temporal import get_julian_date

# **************************************************************************************


def get_correction_to_equatorial_for_aberration(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for abberation in
    longitude and obliquity due to the apparent motion of the Earth.

    :param date: The datetime object to convert.
    :param longitude: The longitude of the observer in degrees.
    :param target: The equatorial coordinates of the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    # Get the Julian date:
    JD = get_julian_date(date)

    # Get the difference in fractional Julian centuries between the target
    # date and J2000.0
    T = (JD - 2451545.0) / 36525

    # Get the ecliptic longitude of the ascending node of the mode (in degrees):
    Ω = get_lunar_mean_ecliptic_longitude_of_the_ascending_node(date)

    # Get the mean geometric longitude of the sun (in degrees):
    L = get_solar_mean_geometric_longitude(date)

    # Get the mean geometric longitude of the moon (in degrees):
    longitude = get_lunar_mean_geometric_longitude(date)

    # Get the nutation in obliquity (in degrees):
    Δε = (
        9.2 * cos(radians(Ω))
        + 0.57 * cos(radians(2 * L))
        + 0.1 * cos(radians(2 * longitude ))
        - 0.09 * cos(radians(2 * Ω))
    ) / 3600

    # Get the true obliquity of the ecliptic (in degrees):
    ε = radians(get_obliquity_of_the_ecliptic(date) + Δε)

    # Get the constant of abberation (in degrees):
    κ = 20.49552 / 3600

    # Get the eccentricity of the Earth's orbit (dimensionless):
    e = get_eccentricity_of_orbit(date)

    # Get the longitude of perihelion (in degrees):
    ϖ = radians(102.93735 + 1.71953 * T + 0.00046 * pow(T, 2))

    # Get the true geometric longitude of the sun (in degrees):
    S = radians(get_solar_true_geometric_longitude(date))

    # Calculate the abberation correction in right ascension (in degrees):
    Δra = -κ * (cos(ra) * cos(S) * cos(ε) + sin(ra) * sin(S) / cos(dec)) + e * κ * (
        cos(ra) * cos(ϖ) * cos(ε) + sin(ra) * sin(ϖ) / cos(dec)
    )

    # Calculate the abberation correction in declination (in degrees):
    Δdec = -κ * (
        (cos(S) * cos(ε) * (tan(ε) * cos(dec) - sin(ra) * sin(dec)))
        + (cos(ra) * sin(dec) * sin(S))
    ) + e * κ * (
        (cos(ϖ) * cos(ε) * (tan(ε) * cos(dec) - sin(ra) * sin(dec)))
        + (cos(ra) * sin(dec) * sin(ϖ))
    )

    return {"ra": Δra, "dec": Δdec}


# **************************************************************************************
