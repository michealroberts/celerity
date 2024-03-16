# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime

from .temporal import get_julian_date

# **************************************************************************************


def get_number_of_fractional_days_since_j2000(date: datetime) -> float:
    """
    The number of fractional days since J2000.0 is the number of
    fractional days since January 1, 2000 at 12:00 UT.

    :param date: The datetime object to convert.
    :return: The number of fractional days since J2000.0 of the given date normalised to UTC.
    """
    return get_julian_date(date) - 2451545.0


# **************************************************************************************
