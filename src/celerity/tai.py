# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime, timezone
from typing import Final, List, TypedDict

# **************************************************************************************


class IERSTAIUTCOffsetEntry(TypedDict):
    """
    Represents a TAI-UTC offset entry.
    """

    # The datetime of the TAI-UTC offset entry:
    at: datetime
    # The TAI-UTC offset (in seconds):
    offset: float


# **************************************************************************************

# The IERS leap seconds data, representing the TAI-UTC offset at specific dates.
# This data is based on the IERS Bulletin C and is subject to change.
# see https://data.iana.org/time-zones/data/leap-seconds.list
# see https://hpiers.obspm.fr/eop-pc/earthor/utc/leapsecond.html
IERS_LEAP_SECONDS: Final[List[IERSTAIUTCOffsetEntry]] = [
    {
        "at": datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 10.0,
    },
    {
        "at": datetime(1972, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 11.0,
    },
    {
        "at": datetime(1973, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 12.0,
    },
    {
        "at": datetime(1974, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 13.0,
    },
    {
        "at": datetime(1975, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 14.0,
    },
    {
        "at": datetime(1976, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 15.0,
    },
    {
        "at": datetime(1977, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 16.0,
    },
    {
        "at": datetime(1978, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 17.0,
    },
    {
        "at": datetime(1979, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 18.0,
    },
    {
        "at": datetime(1981, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 19.0,
    },
    {
        "at": datetime(1982, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 20.0,
    },
    {
        "at": datetime(1983, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 21.0,
    },
    {
        "at": datetime(1985, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 22.0,
    },
    {
        "at": datetime(1988, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 23.0,
    },
    {
        "at": datetime(1990, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 24.0,
    },
    {
        "at": datetime(1991, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 25.0,
    },
    {
        "at": datetime(1992, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 26.0,
    },
    {
        "at": datetime(1993, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 27.0,
    },
    {
        "at": datetime(1994, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 28.0,
    },
    {
        "at": datetime(1996, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 29.0,
    },
    {
        "at": datetime(1997, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 30.0,
    },
    {
        "at": datetime(1999, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 31.0,
    },
    {
        "at": datetime(2006, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 32.0,
    },
    {
        "at": datetime(2009, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 33.0,
    },
    {
        "at": datetime(2012, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 34.0,
    },
    {
        "at": datetime(2015, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 35.0,
    },
    {
        "at": datetime(2017, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 37.0,
    },
]

# **************************************************************************************


def get_tai_utc_offset(date: datetime) -> float:
    """
    Returns the TAI-UTC offset (in seconds) for the given date.

    :param date: The datetime for which to get the TAI-UTC offset.
    :return: The TAI-UTC offset in seconds.
    """
    # Ensure the date is in UTC:
    date = (
        date.replace(tzinfo=timezone.utc)
        if date.tzinfo is None
        else date.astimezone(tz=timezone.utc)
    )

    # If the datetime is before TAI was introduced, return 0.0:
    if date < datetime(1972, 1, 1, tzinfo=timezone.utc):
        return 0.0

    # If the datetime is greater than or equal to 1972-01-01, then we know we have a
    # minimum offset of 10 seconds:
    offset = 10.0

    # If the datetime is after TAI was introduced, return the current TAI-UTC offset:
    for entry in IERS_LEAP_SECONDS:
        if entry["at"] <= date:
            offset = entry["offset"]
        else:
            break

    # Return the TAI-UTC offset for the date (in seconds):
    return offset


# **************************************************************************************


def get_tt_utc_offset(date: datetime) -> float:
    """
    Returns the TT-UTC offset (in seconds) for the given date.

    :return: The TT-UTC offset in seconds.
    """
    # TT is always 32.184 seconds ahead of TAI:
    return get_tai_utc_offset(date) + 32.184


# **************************************************************************************
