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


class IERSTAIUTCDriftEntry(TypedDict):
    # The datetime from which the drift expression applies:
    at: datetime
    # The TAI-UTC offset (in seconds) at the reference epoch of the expression:
    offset: float
    # The reference epoch of the expression, as a Modified Julian Date (in days):
    epoch: float
    # The rate of change of the TAI-UTC offset (in seconds per day):
    rate: float


# **************************************************************************************

# The TAI-UTC offset expressions in force between the introduction of UTC on 1960-01-01
# and the introduction of leap seconds on 1972-01-01, during which UTC was kept close to
# UT by frequency offsets and small steps, so that TAI-UTC varied linearly within each
# interval as offset + (MJD - epoch) * rate. The expressions are those tabulated in the
# IERS Conventions and SOFA dat:
IERS_TAI_UTC_DRIFT: Final[List[IERSTAIUTCDriftEntry]] = [
    {
        "at": datetime(1960, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 1.417818,
        "epoch": 37300.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1961, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 1.422818,
        "epoch": 37300.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1961, 8, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 1.372818,
        "epoch": 37300.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1962, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 1.845858,
        "epoch": 37665.0,
        "rate": 0.0011232,
    },
    {
        "at": datetime(1963, 11, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 1.945858,
        "epoch": 37665.0,
        "rate": 0.0011232,
    },
    {
        "at": datetime(1964, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.24013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1964, 4, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.34013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1964, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.44013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1965, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.54013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1965, 3, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.64013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1965, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.74013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1965, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 3.84013,
        "epoch": 38761.0,
        "rate": 0.001296,
    },
    {
        "at": datetime(1966, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 4.31317,
        "epoch": 39126.0,
        "rate": 0.002592,
    },
    {
        "at": datetime(1968, 2, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 4.21317,
        "epoch": 39126.0,
        "rate": 0.002592,
    },
]

# **************************************************************************************

# The IERS leap seconds data, representing the TAI-UTC offset (in seconds) in force
# from each date, as announced in IERS Bulletin C. The first entry is the initial offset
# of 10 seconds at the introduction of the current UTC system on 1972-01-01, and each of
# the 27 subsequent entries records the offset after a positive leap second was inserted
# at the end of the preceding day. This data is subject to change with future bulletins.
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
        "at": datetime(1980, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 19.0,
    },
    {
        "at": datetime(1981, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 20.0,
    },
    {
        "at": datetime(1982, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 21.0,
    },
    {
        "at": datetime(1983, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 22.0,
    },
    {
        "at": datetime(1985, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 23.0,
    },
    {
        "at": datetime(1988, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 24.0,
    },
    {
        "at": datetime(1990, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 25.0,
    },
    {
        "at": datetime(1991, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 26.0,
    },
    {
        "at": datetime(1992, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 27.0,
    },
    {
        "at": datetime(1993, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 28.0,
    },
    {
        "at": datetime(1994, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 29.0,
    },
    {
        "at": datetime(1996, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 30.0,
    },
    {
        "at": datetime(1997, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 31.0,
    },
    {
        "at": datetime(1999, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 32.0,
    },
    {
        "at": datetime(2006, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 33.0,
    },
    {
        "at": datetime(2009, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 34.0,
    },
    {
        "at": datetime(2012, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 35.0,
    },
    {
        "at": datetime(2015, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "offset": 36.0,
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

    # If the datetime is before UTC was introduced on 1960-01-01, return 0.0:
    if date < datetime(1960, 1, 1, tzinfo=timezone.utc):
        return 0.0

    # If the datetime is before leap seconds were introduced on 1972-01-01, evaluate the
    # drift expression in force at the datetime:
    if date < datetime(1972, 1, 1, tzinfo=timezone.utc):
        # Get the Modified Julian Date of the datetime (in days):
        MJD = (
            date - datetime(1858, 11, 17, tzinfo=timezone.utc)
        ).total_seconds() / 86400

        # Get the last drift expression that came into force on or before the datetime:
        drift = IERS_TAI_UTC_DRIFT[0]

        for expression in IERS_TAI_UTC_DRIFT:
            if expression["at"] <= date:
                drift = expression
            else:
                break

        # Return the TAI-UTC offset for the date (in seconds):
        return drift["offset"] + (MJD - drift["epoch"]) * drift["rate"]

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
