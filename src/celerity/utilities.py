# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import floor

from .common import Angle, HourAngle

# **************************************************************************************


def get_normalised_azimuthal_degree(degree: float) -> float:
    """
    Applies a correction to a degree value greater than 360°

    :param degree: The degree value to correct
    :return: The corrected degree value (0° <= degree < 360°)
    """
    # Correct for large angles (+ive or -ive):
    d = degree % 360

    # Correct for negative angles
    if d < 0:
        d += 360

    return d


# **************************************************************************************


def get_normalised_inclination_degree(degree: float) -> float:
    """
    Applies a correction to a degree value greater than 90° or less than -90°

    :param degree: The degree value to correct
    :return: The corrected degree value (-90° <= degree <= 90°)
    """
    d = degree

    # Correct for angles greater than 90° or less than -90°
    if degree > 90:
        d = 180 - degree

    # Correct for angles less than -90°
    if degree < -90:
        d = -180 - degree

    if d < 0:
        d % -90

    if d > 0:
        d % 90

    return d


# **************************************************************************************


def convert_degree_to_dms(degree: float) -> Angle:
    """
    Convert coordinate (in decimal degrees) to degrees (°), minutes ('), seconds (").

    :param degree: decimal degree
    :return: the components of the degree in degrees, minutes, seconds
    """

    degree = get_normalised_inclination_degree(degree)

    deg = floor(abs(degree))

    min = floor((abs(degree) - deg) * 60)

    # Get the second component:
    sec = round((abs(degree) - deg - min / 60) * 3600 * 1000) / 1000

    return {"deg": deg if degree >= 0 else -deg, "min": min, "sec": sec}


# **************************************************************************************


def convert_degree_to_hms(degree: float) -> HourAngle:
    degree = get_normalised_azimuthal_degree(degree)

    hour = floor(abs(degree) / 15)

    min = floor((abs(degree) / 15 - hour) * 60)

    # Get the second component:
    sec = round((abs(degree) / 15 - hour - min / 60) * 3600 * 1000) / 1000

    return {"hour": hour, "min": min, "sec": sec}
