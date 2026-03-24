# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import cos, radians

from .astrometry import get_obliquity_of_the_ecliptic
from .moon import (
    get_mean_ecliptic_longitude_of_the_ascending_node,
    get_mean_geometric_longitude as get_mean_lunar_geometric_longitude,
)
from .sun import get_mean_geometric_longitude as get_mean_solar_geometric_longitude

# **************************************************************************************


def get_true_obliquity_of_the_ecliptic(date: datetime) -> float:
    """
    Gets the true obliquity of the ecliptic for a particular datetime

    The true obliquity of the ecliptic is the mean obliquity corrected for
    nutation in obliquity.

    :param date: The datetime object to convert.
    :return: The true obliquity of the ecliptic in degrees.
    """
    # Get the ecliptic longitude of the ascending node of the Moon (in degrees):
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date)

    # Get the mean solar geometric longitude (in degrees):
    L = get_mean_solar_geometric_longitude(date)

    # Get the mean lunar geometric longitude (in degrees):
    longitude = get_mean_lunar_geometric_longitude(date)

    # Calculate the nutation in obliquity (in degrees):
    Δε = (
        9.20 * cos(radians(Ω))
        + 0.57 * cos(radians(2.0 * L))
        + 0.10 * cos(radians(2.0 * longitude))
        - 0.09 * cos(radians(2.0 * Ω))
    ) / 3600.0

    # Calculate the true obliquity of the ecliptic:
    return get_obliquity_of_the_ecliptic(date) + Δε


# **************************************************************************************
