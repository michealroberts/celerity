# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timezone
from math import floor, pow

from .common import GeographicCoordinate
from .constants import J1900, J2000

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


def get_modified_julian_date(date: datetime) -> float:
    """
    The Modified Julian Date (MJD) is the number of fractional days since midnight
    on November 17, 1858.

    :param date: The datetime object to convert.
    :return: The Modified Julian Date (MJD) of the given date normalised to UTC.
    """
    return get_julian_date(date) - 2400000.5


# **************************************************************************************


def get_greenwich_sidereal_time(date: datetime) -> float:
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
    )

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
    JD_0 = (
        get_julian_date(datetime(year, 1, 1, 0, 0, 0, 0).astimezone(tz=timezone.utc))
        + 30
    )

    # Get the number of days since 1st January for the current year:
    days = JD - JD_0

    # Get the number of Julian Centuries since 1900:
    T = (JD_0 - J1900) / 36525

    R = 6.6460656 + 2400.051262 * T + 0.00002581 * pow(T, 2)

    B = 24 - R + 24 * (year - 1900)

    T_0 = 0.0657098 * days - B

    if T_0 < 0:
        T_0 += 24

    if T_0 > 24:
        T_0 -= 24

    A = GST - T_0

    if A < 0:
        A += 24

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
    lon = observer["lon"]

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
