# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from math import floor, pow
from typing import Tuple
from urllib.parse import urlencode

from .common import GeographicCoordinate
from .constants import J1900, J2000, JULIAN_DAYS_PER_CENTURY
from .iers import IERS_EOP_BASE_URL, fetch_iers_rapid_service_data
from .tai import get_tai_utc_offset

# **************************************************************************************


def get_julian_date(date: datetime) -> float:
    """
    The Julian date (JD) of any instant is the Julian day number
    plus the fraction of a day since the preceding noon in Universal
    Time (UT).

    :param date: The datetime object to convert.
    :return: The Julian Date (JD) of the given date normalised to UTC.
    """
    return (
        int(
            (
                date.astimezone(tz=timezone.utc)
                - datetime(1970, 1, 1, tzinfo=timezone.utc)
            ).total_seconds()
            * 1000
        )
        / 86400000.0
    ) + 2440587.5


# **************************************************************************************


def get_julian_centuries(date: datetime) -> float:
    """
    The Julian centuries (T) is the number of Julian centuries since
    epoch J2000.0.

    :param date: The datetime object to convert.
    :return: The Julian centuries (T) of the given date normalised to UTC.
    """
    JD = get_julian_date(date)

    return (JD - J2000) / JULIAN_DAYS_PER_CENTURY


# **************************************************************************************


def get_julian_millennia(date: datetime) -> float:
    """
    The Julian millennia (τ) is the number of Julian millennia since
    epoch J2000.0.

    :param date: The datetime object to convert.
    :return: The Julian millennia (τ) of the given date normalised to UTC.
    """
    T = get_julian_centuries(date)

    return T / 10.0


# **************************************************************************************


def get_modified_julian_date(date: datetime) -> float:
    """
    The Modified Julian Date (MJD) is the number of fractional days since midnight
    on November 17, 1858.

    :param date: The datetime object to convert.
    :return: The Modified Julian Date (MJD) of the given date normalised to UTC.
    """
    return get_julian_date(date) - 2400000.5


# **************************************************************************************


def get_modified_julian_date_as_parts(when: datetime) -> Tuple[int, float]:
    """
    Convert a UTC datetime object to Modified Julian Date (MJD) and its
    corresponding seconds of the day (e.g., 0.0 to 86400.0).

    :param when: The datetime object to convert.
    :return: A tuple containing the Modified Julian Date (MJD) and the seconds of the day.
    """
    # If the datetime does not have a timezone (e.g., a naive datetime), assume UTC;
    # otherwise, convert it to UTC:
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    else:
        when = when.astimezone(tz=timezone.utc)

    # Get the Modified Julian Date for the given datetime:
    MJD = get_modified_julian_date(when)

    # Get the UTC date at midnight for the given datetime:
    midnight = when.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    # Calculate the seconds of the day since midnight for the currrent datetime:
    seconds_of_day = (when - midnight).total_seconds()

    return floor(MJD), seconds_of_day


# **************************************************************************************


def get_greenwich_sidereal_time(date: datetime, dut1: float = 0.0) -> float:
    """
    The Greenwich Sidereal Time (GST) is the hour angle of the vernal
    equinox, the ascending node of the ecliptic on the celestial equator.

    :param date: The datetime object to convert.
    :return: The Greenwich Sidereal Time (GST) of the given date normalised to UTC.
    """
    JD = get_julian_date(date)

    JD_0 = floor(JD - 0.5) + 0.5

    S = JD_0 - J2000

    T = S / 36525.0

    T_0 = (6.697374558 + 2400.051336 * T + 0.000025862 * pow(T, 2)) % 24

    if T_0 < 0:
        T_0 += 24

    # Convert the UTC time to a decimal fraction of hours:
    UTC = (
        (date.microsecond / 3.6e9)
        + (date.second / 3600)
        + (date.minute / 60)
        + date.hour
    ) + (dut1 / 3600.0)

    A = UTC * 1.002737909

    T_0 += A

    GST = T_0 % 24

    return GST + 24 if GST < 0 else GST


# **************************************************************************************


def get_local_sidereal_time(date: datetime, longitude: float) -> float:
    """
    The Local Sidereal Time (LST) is the hour angle of the vernal
    equinox, the ascending node of the ecliptic on the celestial equator.

    :param date: The datetime object to convert.
    :param longitude: The longitude of the observer.
    :return: The Local Sidereal Time (LST) of the given date normalised to UTC.
    """
    GST = get_greenwich_sidereal_time(date)

    d = (GST + longitude / 15.0) / 24.0

    d = d - floor(d)

    if d < 0:
        d += 1

    return 24.0 * d


# **************************************************************************************


def get_universal_time(date: datetime) -> float:
    """
    Universal Time (UT or UT1) is a time standard based on Earth's
    rotation. While originally it was mean solar time at 0° longitude,
    precise measurements of the Sun are difficult. Therefore, UT1 is
    computed from a measure of the Earth's angle with respect to the
    International Celestial Reference Frame (ICRF), called the Earth
    Rotation Angle (ERA, which serves as a modern replacement for
    Greenwich Mean Sidereal Time).

    UT1 is the same everywhere on Earth.

    :param date: The datetime object to convert.
    :return The Universal Time (UT) of the given date normalised to UTC.
    """

    year = date.astimezone(tz=timezone.utc).year

    GST = get_greenwich_sidereal_time(date.astimezone(tz=timezone.utc))

    # Get the Julian Date at 0h:
    JD = get_julian_date(
        datetime(year, date.month, date.day, 0, 0, 0, 0).astimezone(tz=timezone.utc)
    )

    # Get the Julian Date at 0h on 1st January for the current year:
    JD_0 = get_julian_date(datetime(year, 1, 1, 0, 0, 0, 0).astimezone(tz=timezone.utc))

    # Get the number of days since 1st January for the current year:
    days = JD - JD_0

    # Get the number of Julian Centuries since 1900:
    T = (JD_0 - J1900) / 36525

    R = 6.6460656 + 2400.051262 * T + 0.00002581 * pow(T, 2)

    B = (24 - R + 24 * (year - 1900)) % 24

    T_0 = (0.0657098 * days - B) % 24

    A = (GST - T_0) % 24

    return 0.99727 * A


# **************************************************************************************


def convert_local_sidereal_time_to_greenwich_sidereal_time(
    LST: float, observer: GeographicCoordinate
) -> float:
    """
    Converts the Local Sidereal Time (LST) to the Greenwich Sidereal Time (GST).

    :param date: The datetime object to convert.
    :param longitude: The longitude of the observer.
    :return: The Local Sidereal Time (LST) of the given date normalised to UTC.
    """
    lon = observer["longitude"]

    GST = LST - (lon / 15.0)

    if GST < 0:
        GST += 24

    if GST > 24:
        GST -= 24

    return GST


# **************************************************************************************


def convert_greenwich_sidereal_time_to_universal_coordinate_time(
    date: datetime, GST: float
) -> datetime:
    """
    Convert the Greenwich Sidereal Time (GST) to the Universal Coordinated Time (UTC).

    :param date: The datetime object to convert.
    :param GST: The Greenwich Sidereal Time (GST) to convert.
    :return: The Universal Coordinated Time (UTC) of the given date normalised to UTC.
    """
    # Adjust the date to UTC:
    date = date.astimezone(tz=timezone.utc)

    # Get the Julian Date at 0h:
    JD = get_julian_date(datetime(date.year, date.month, date.day, 0, 0, 0, 0))

    # Get the Julian Date at 0h on 1st January for the current year:
    JD_0 = (
        get_julian_date(
            datetime(date.year, 1, 1, 0, 0, 0, 0).astimezone(tz=timezone.utc)
        )
        - 1
    )

    # Get the number of Julian days since 1st January for the current year:
    d = JD - JD_0

    # Calculate the number of centuries since J1900.0 and JD_0:
    T = (JD_0 - 2415020.0) / 36525

    R = 6.6460656 + 2400.051262 * T + 0.00002581 * pow(T, 2)

    B = 24 - R + (24 * (date.year - 1900))

    T_0 = (0.0657098 * d) - B

    if T_0 < 0:
        T_0 += 24

    if T_0 > 24:
        T_0 -= 24

    A = GST - T_0

    # Correct for negative hour angles
    if A < 0:
        A += 24

    UTC = 0.99727 * A

    # Convert decimal hours to hours, minutes and seconds:

    hours = floor(UTC)

    minutes = floor((UTC - hours) * 60)

    seconds = floor(((UTC - hours) * 60 - minutes) * 60)

    microseconds = floor((((UTC - hours) * 60 - minutes) * 60 - seconds) * 1000000)

    return datetime(
        date.year,
        date.month,
        date.day,
        hours,
        minutes,
        seconds,
        microseconds,
        tzinfo=timezone.utc,
    )


# **************************************************************************************


def get_ut1_utc_offset(when: datetime) -> float:
    MJD, _ = get_modified_julian_date_as_parts(when)

    # Setup the query parameters for the IERS Rapid Service data:
    q = {
        "param": "UT1-UTC",
        "mjd": MJD,
        "series": "Finals All IAU1980",
    }

    # Construct the URL for the IERS Rapid Service data with the UT1-UTC, mjd and series
    # parameters set:
    url = f"{IERS_EOP_BASE_URL}?{urlencode(q, safe=' ')}".replace("+", "%20")

    # Fetch the DUT1 entry from the IERS Rapid Service data:
    entry = fetch_iers_rapid_service_data(url)

    return entry["dut1"]


# **************************************************************************************


class Time(datetime):
    when: datetime

    def __new__(cls, when: datetime):
        cls.when = when

        return super(Time, cls).__new__(
            cls,
            when.year,
            when.month,
            when.day,
            when.hour,
            when.minute,
            when.second,
            when.microsecond,
            tzinfo=timezone.utc,
        )

    def at(self, when: datetime) -> "Time":
        """
        Create a new Time object at the given datetime.
        """
        return Time(when)

    @property
    def UT(self) -> float:
        """
        Get the Universal Time for the given datetime.
        """
        return get_universal_time(self.when)

    @property
    def TAI(self) -> datetime:
        """
        Get the International Atomic Time for the given datetime.
        """
        # Ensure the datetime is in UTC:
        now = self.when.astimezone(tz=timezone.utc)

        # Get the TAI-UTC offset for the given datetime:
        offset = get_tai_utc_offset(now)

        # Create the TAI timezone:
        TZ = timezone(timedelta(seconds=offset), name="TAI")

        return (now + timedelta(seconds=offset)).replace(tzinfo=TZ)

    @property
    def UT1(self) -> datetime:
        """
        Get the Universal Time 1 for the given datetime.
        """
        # Ensure the datetime is in UTC:
        now = self.when.astimezone(tz=timezone.utc)

        # Get the UT1-UTC offset for the given datetime (seconds):
        offset = get_ut1_utc_offset(now)

        # Create the UT1 timezone:
        TZ = timezone(timedelta(seconds=offset), name="UT1")

        return (now + timedelta(seconds=offset)).replace(tzinfo=TZ)

    @property
    def JD(self) -> float:
        """
        Get the Julian Date for the given datetime.
        """
        return get_julian_date(self.when)

    @property
    def MJD(self) -> float:
        """
        Get the Modified Julian Date for the given datetime.
        """
        return get_modified_julian_date(self.when)

    @property
    def GST(self) -> float:
        """
        Get the Greenwich Sidereal Time for the given datetime.
        """
        return get_greenwich_sidereal_time(self.when)

    def LST(self, longitude) -> float:
        return get_local_sidereal_time(self.when, longitude)

    def __str__(self) -> str:
        return self.when.isoformat()

    def __repr__(self) -> str:
        return self.when.isoformat()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Time) and self.when.timestamp() == other.when.timestamp()
        )


# **************************************************************************************
