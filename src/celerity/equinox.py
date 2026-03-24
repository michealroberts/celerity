# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timezone
from math import cos, radians, sin

from .ecliptic import get_true_obliquity_of_the_ecliptic
from .moon import (
    get_mean_ecliptic_longitude_of_the_ascending_node,
)
from .moon import (
    get_mean_geometric_longitude as get_mean_lunar_geometric_longitude,
)
from .sun import get_mean_geometric_longitude as get_mean_solar_geometric_longitude

# **************************************************************************************


def get_spring_equinox(year: int) -> datetime:
    """
    Get the datetime of the spring equinox for the given year.

    :param year: The year to get the spring equinox for.
    :return: The datetime of the spring equinox for the given year.
    """
    T = year / 1000

    # Get the Julian date of the spring equinox (using Meeus' formula):
    JD = (
        1721139.2855 + 365.2421376 * year + 0.067919 * pow(T, 2) - 0.0027879 * pow(T, 3)
    )

    # Convert the Julian date to a datetime UTC object:
    return datetime.fromtimestamp((JD - 2440587.5) * 86400).astimezone(tz=timezone.utc)


# **************************************************************************************


def get_autumn_equinox(year: int) -> datetime:
    """
    Get the datetime of the autumn equinox for the given year.

    :param year: The year to get the autumn equinox for.
    :return: The datetime of the autumn equinox for the given year.
    """
    T = year / 1000

    # Get the Julian date of the autumn equinox (using Meeus' formula):
    JD = (
        1721325.6978 + 365.2425055 * year - 0.126689 * pow(T, 2) + 0.0019401 * pow(T, 3)
    )

    # Convert the Julian date to a datetime UTC object:
    return datetime.fromtimestamp((JD - 2440587.5) * 86400).astimezone(tz=timezone.utc)


# **************************************************************************************


def get_equation_of_the_equinoxes(date: datetime) -> float:
    """
    Gets the equation of the equinoxes for a particular datetime

    The equation of the equinoxes is the difference between apparent sidereal
    time and mean sidereal time.

    :param date: The datetime object to convert.
    :return: The equation of the equinoxes in degrees.
    """
    # Get the ecliptic longitude of the ascending node of the Moon (in degrees):
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date)

    # Get the mean solar geometric longitude (in degrees):
    L = get_mean_solar_geometric_longitude(date)

    # Get the mean lunar geometric longitude (in degrees):
    longitude = get_mean_lunar_geometric_longitude(date)

    # Get the nutation in longitude (in arcseconds):
    Δψ = (
        -17.20 * sin(radians(Ω))
        - 1.32 * sin(radians(2.0 * L))
        - 0.23 * sin(radians(2.0 * longitude))
        + 0.21 * sin(radians(2.0 * Ω))
    )

    # Get the true obliquity of the ecliptic (in degrees):
    ε = get_true_obliquity_of_the_ecliptic(date)

    # Calculate the equation of the equinoxes (in arcseconds):
    Ee = (
        Δψ * cos(radians(ε))
        + 0.00264 * sin(radians(Ω))
        + 0.000063 * sin(radians(2.0 * Ω))
    )

    return Ee / 3600.0


# **************************************************************************************
