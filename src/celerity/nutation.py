# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import cos, degrees, radians, sin, tan

from .astrometry import get_obliquity_of_the_ecliptic
from .common import EquatorialCoordinate
from .moon import get_mean_ecliptic_longitude_of_the_ascending_node
from .moon import get_mean_geometric_longitude as get_mean_lunar_geometric_longitude
from .sun import get_mean_geometric_longitude as get_mean_solar_geometric_longitude

# **************************************************************************************


def get_correction_to_equatorial_for_nutation(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for nutation in longitude and obliquity.

    :param date: The datetime object to convert.
    :param longitude: The longitude of the observer in degrees.
    :param target: The equatorial coordinates of the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    # Get the ecliptic longitude of the ascending node of the mode (in degrees)
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date)

    # Get the mean solar geometric longitude (in degrees):
    L = get_mean_solar_geometric_longitude(date)

    # Get the mean lunar geometric longitude (in degrees):
    longitude = get_mean_lunar_geometric_longitude(date)

    # Get the nutation in longitude (in arcseconds)
    Δψ = (
        -17.2 * sin(radians(Ω))
        - 1.32 * sin(radians(2 * L))
        - 0.23 * sin(radians(2 * longitude))
        + 0.21 * sin(radians(2 * Ω))
    )

    # Get the nutation in obliquity (in arcseconds)
    Δε = (
        9.2 * cos(radians(Ω))
        + 0.57 * cos(radians(2 * L))
        + 0.1 * cos(radians(2 * longitude))
        - 0.09 * cos(radians(2 * Ω))
    )

    # Get the true obliquity of the ecliptic (in degrees):
    ε = radians(get_obliquity_of_the_ecliptic(date) + Δε / 3600)

    # Calculate the nutation correction in right ascension (in degrees)
    Δra = (degrees(cos(ε) + sin(ε) * sin(ra) * tan(dec)) * Δψ / 3600) - degrees(
        cos(ra) * tan(dec)
    ) * Δε / 3600

    # Calculate the nutation correction in declination (in degrees)
    Δdec = degrees(sin(ε) * cos(ra)) * Δψ / 3600 + degrees(sin(ra)) * Δε / 3600

    return {"ra": Δra, "dec": Δdec}


# **************************************************************************************
