# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import pow

from .temporal import get_julian_date

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
