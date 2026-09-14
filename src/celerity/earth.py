# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from math import cos, pow, radians, sin

from .astrometry import get_obliquity_of_the_ecliptic
from .common import CartesianVelocity
from .constants import AU
from .planet import Planet
from .planets import get_planetary_heliocentric_coordinate
from .temporal import get_julian_date, get_terrestrial_time_in_julian_centuries

# **************************************************************************************


def get_eccentricity_of_orbit(date: datetime) -> float:
    """
    Get the eccentricity of the Earth's orbit.

    :param date: The datetime object to convert.
    :return: The eccentricity of the Earth's orbit in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Get the difference in fractional Julian centuries between the target date and J2000.0
    T = (JD - 2451545.0) / 36525

    # Get the eccentricity of the Earth's orbit
    return 0.0167086342 - 0.000042037 * T - 0.0000001267 * pow(T, 2) % 360


# **************************************************************************************


def get_heliocentric_velocity(date: datetime) -> CartesianVelocity:
    """
    Get the heliocentric velocity of the Earth (in metres per second), referred to the
    mean equator and equinox of date.

    :param date: The datetime object to convert.
    :return: The heliocentric velocity of the Earth (in metres per second).
    """
    # Treat a naive datetime as UTC, and bring an aware datetime to UTC, so that the
    # positions either side of the instant are evaluated for the same UTC instants
    # regardless of the host's local timezone:
    date = (
        date.replace(tzinfo=timezone.utc)
        if date.tzinfo is None
        else date.astimezone(tz=timezone.utc)
    )

    # Half of the central differencing interval:
    Δt = timedelta(hours=6)

    # Get the Julian centuries of TT since J2000.0 at the central instant:
    T = get_terrestrial_time_in_julian_centuries(date)

    # Get the rate of general precession in longitude (in arcseconds per Julian century)
    # at the central instant, from the IAU 2006 expression for p_A:
    p = 5028.796195 + 2 * 1.1054348 * T

    # Get the precession in longitude accumulated over half the differencing interval (in
    # radians), by which the ecliptic frame of each evaluation differs from the frame of
    # the central instant:
    Δλ = radians(p * (Δt.total_seconds() / (86400 * 36525)) / 3600)

    # Get the heliocentric ecliptic spherical coordinates of the Earth before the instant:
    before = get_planetary_heliocentric_coordinate(date - Δt, Planet.EARTH)

    # Get the heliocentric ecliptic spherical coordinates of the Earth after the instant:
    after = get_planetary_heliocentric_coordinate(date + Δt, Planet.EARTH)

    # Get the ecliptic longitude before (in radians), referred to the central frame:
    λ0 = radians(before["λ"]) + Δλ

    # Get the ecliptic latitude before (in radians):
    β0 = radians(before["β"])

    # Get the heliocentric radius before (in metres):
    r0 = before["r"] * AU

    # Get the ecliptic longitude after (in radians), referred to the central frame:
    λ1 = radians(after["λ"]) - Δλ

    # Get the ecliptic latitude after (in radians):
    β1 = radians(after["β"])

    # Get the heliocentric radius after (in metres):
    r1 = after["r"] * AU

    # Calculate the ecliptic rectangular coordinates (in metres) before:
    x0, y0, z0 = r0 * cos(β0) * cos(λ0), r0 * cos(β0) * sin(λ0), r0 * sin(β0)

    # Calculate the ecliptic rectangular coordinates (in metres) after:
    x1, y1, z1 = r1 * cos(β1) * cos(λ1), r1 * cos(β1) * sin(λ1), r1 * sin(β1)

    # Get the full central differencing interval (in seconds):
    seconds = 2 * Δt.total_seconds()

    # Calculate the ecliptic velocity components (in metres per second):
    vx, vy, vz = (x1 - x0) / seconds, (y1 - y0) / seconds, (z1 - z0) / seconds

    # Get the mean obliquity of the ecliptic (in radians) at the central instant:
    ε = radians(get_obliquity_of_the_ecliptic(date))

    return {
        "x": vx,
        "y": vy * cos(ε) - vz * sin(ε),
        "z": vy * sin(ε) + vz * cos(ε),
    }


# **************************************************************************************
