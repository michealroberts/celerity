# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from .constants import c as SPEED_OF_LIGHT

# **************************************************************************************

def get_light_travel_distance(time: float) -> float:
    """
    Calculate the distance light travels in a given time.

    :param time: The time in seconds.
    :return: The distance light travels in the given time in meters.
    """
    return SPEED_OF_LIGHT * time

# **************************************************************************************