# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timezone
from math import cos, radians, sin

from .astrometry import get_obliquity_of_the_ecliptic
from .common import EquatorialCoordinate
from .constants import AU
from .matrix import apply_matrix
from .nutation import get_nutation_matrix
from .planet import Planet
from .planets import get_planetary_heliocentric_coordinate
from .sun import SCHWARZSCHILD_RADIUS_OF_THE_SUN
from .vector import convert_equatorial_to_vector, convert_vector_to_equatorial

# **************************************************************************************

# The lower limit on the quantity q·(q + e) in the deflection formula (dimensionless),
# below which the deflection is held constant to keep it finite for a target in the
# direction of the Sun (as in SOFA ldsun, for an observer at one astronomical unit):
LIGHT_DEFLECTION_LIMIT: float = 1e-6

# **************************************************************************************


def get_correction_to_equatorial_for_light_deflection(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for the gravitational deflection of
    its light by the Sun.

    The correction follows the post-Newtonian formulation of the IAU (Klioner 2003, AJ
    125, 1580; as implemented in SOFA ldsun), which deflects the direction of the target
    away from the Sun by an angle that falls from 1.75 arcseconds at the solar limb to
    about 4 milliarcseconds at 90 degrees from the Sun. The target is taken to be
    referred to the true equator and equinox of date, matching the frame in which the
    Earth's heliocentric position is used.

    :param date: The datetime object to convert.
    :param target: The equatorial coordinates of the target.
    """
    # Treat a naive datetime as UTC, and bring an aware datetime to UTC, so that the
    # Earth's position is evaluated for the same UTC instant regardless of the host's
    # local timezone:
    date = (
        date.replace(tzinfo=timezone.utc)
        if date.tzinfo is None
        else date.astimezone(tz=timezone.utc)
    )

    # Get the direction cosines of the target (dimensionless):
    px, py, pz = convert_equatorial_to_vector(target)

    # Get the heliocentric ecliptic spherical coordinates of the Earth:
    earth = get_planetary_heliocentric_coordinate(date, Planet.EARTH)

    # Get the ecliptic longitude of the Earth (in radians):
    λ = radians(earth["λ"])

    # Get the ecliptic latitude of the Earth (in radians):
    β = radians(earth["β"])

    # Get the heliocentric distance of the Earth (in metres):
    em = earth["r"] * AU

    # Get the mean obliquity of the ecliptic (in radians):
    ε = radians(get_obliquity_of_the_ecliptic(date))

    # Get the heliocentric direction of the Earth referred to the mean equator and
    # equinox of date, by rotating the ecliptic direction cosines about the x axis
    # through the mean obliquity (dimensionless):
    ex, ey, ez = (
        cos(β) * cos(λ),
        cos(β) * sin(λ) * cos(ε) - sin(β) * sin(ε),
        cos(β) * sin(λ) * sin(ε) + sin(β) * cos(ε),
    )

    # Get the heliocentric direction of the Earth referred to the true equator and
    # equinox of date, the frame of the target (dimensionless):
    ex, ey, ez = apply_matrix(get_nutation_matrix(date), (ex, ey, ez))

    # Get the scalar product of the target direction with the sum of the target and
    # Earth directions, which is 1 + cos(θ) for the angle θ between them (dimensionless):
    qdqpe = px * (px + ex) + py * (py + ey) + pz * (pz + ez)

    # Get the deflection factor, the Schwarzschild radius of the Sun over the Earth's
    # distance, divided by the limited scalar product (dimensionless):
    w = SCHWARZSCHILD_RADIUS_OF_THE_SUN / em / max(qdqpe, LIGHT_DEFLECTION_LIMIT)

    # Get the vector product of the Earth and target directions (dimensionless):
    eqx, eqy, eqz = ey * pz - ez * py, ez * px - ex * pz, ex * py - ey * px

    # Get the vector product of the target direction with that product, which points
    # away from the Sun on the sky (dimensionless):
    peqx, peqy, peqz = py * eqz - pz * eqy, pz * eqx - px * eqz, px * eqy - py * eqx

    # Calculate the deflected direction (dimensionless):
    deflected = convert_vector_to_equatorial(
        (px + w * peqx, py + w * peqy, pz + w * peqz)
    )

    # Calculate the light deflection correction in right ascension (in degrees),
    # normalised to the range [-180, 180):
    Δra = (deflected["ra"] - target["ra"] + 180) % 360 - 180

    # Calculate the light deflection correction in declination (in degrees):
    Δdec = deflected["dec"] - target["dec"]

    return {"ra": Δra, "dec": Δdec}


# **************************************************************************************
