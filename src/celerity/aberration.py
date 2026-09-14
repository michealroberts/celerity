# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timezone
from math import atan2, cos, degrees, hypot, radians, sin, sqrt

from .common import EquatorialCoordinate
from .constants import AU, c
from .earth import get_heliocentric_velocity
from .planet import Planet
from .planets import get_planetary_heliocentric_coordinate
from .sun import SCHWARZSCHILD_RADIUS_OF_THE_SUN

# **************************************************************************************


def get_correction_to_equatorial_for_aberration(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for annual aberration due to the
    orbital motion of the Earth.

    :param date: The datetime object to convert.
    :param target: The equatorial coordinates of the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    # Treat a naive datetime as UTC, and bring an aware datetime to UTC, so that the
    # Earth's velocity and distance are evaluated for the same UTC instant regardless of
    # the host's local timezone:
    date = (
        date.replace(tzinfo=timezone.utc)
        if date.tzinfo is None
        else date.astimezone(tz=timezone.utc)
    )

    # Get the direction cosines of the target (dimensionless):
    px, py, pz = cos(dec) * cos(ra), cos(dec) * sin(ra), sin(dec)

    # Get the heliocentric velocity of the Earth (in metres per second):
    velocity = get_heliocentric_velocity(date)

    # Get the velocity of the Earth in units of the speed of light (dimensionless):
    vx, vy, vz = velocity["x"] / c, velocity["y"] / c, velocity["z"] / c

    # Get the heliocentric distance of the Earth (in metres):
    s = get_planetary_heliocentric_coordinate(date, Planet.EARTH)["r"] * AU

    # Get the reciprocal of the Lorentz factor (dimensionless):
    bm1 = sqrt(1 - (vx**2 + vy**2 + vz**2))

    # Get the component of the Earth's velocity along the direction of the target:
    pdv = px * vx + py * vy + pz * vz

    # Get the relativistic aberration factor (dimensionless):
    w1 = 1 + pdv / (1 + bm1)

    # Get the gravitational potential term of the Sun at the Earth (dimensionless):
    w2 = SCHWARZSCHILD_RADIUS_OF_THE_SUN / s

    # Calculate the x component of the aberrated direction, before normalisation:
    ax = px * bm1 + w1 * vx + w2 * (vx - pdv * px)

    # Calculate the y component of the aberrated direction, before normalisation:
    ay = py * bm1 + w1 * vy + w2 * (vy - pdv * py)

    # Calculate the z component of the aberrated direction, before normalisation:
    az = pz * bm1 + w1 * vz + w2 * (vz - pdv * pz)

    # Calculate the aberrated right ascension (in degrees):
    α = degrees(atan2(ay, ax)) % 360

    # Calculate the aberrated declination (in degrees):
    δ = degrees(atan2(az, hypot(ax, ay)))

    # Calculate the abberation correction in right ascension (in degrees):
    Δra = (α - target["ra"] + 180) % 360 - 180

    # Calculate the abberation correction in declination (in degrees):
    Δdec = δ - target["dec"]

    return {"ra": Δra, "dec": Δdec}


# **************************************************************************************
