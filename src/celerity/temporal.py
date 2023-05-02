import math
from datetime import datetime, timezone

from .constants import J1900, J2000


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
                - datetime(1970, 1, 1).astimezone(tz=timezone.utc)
            ).total_seconds()
            * 1000
        )
        / 86400000.0
    ) + 2440587.5


def get_greenwhich_sidereal_time(date: datetime) -> float:
    """
    The Greenwich Sidereal Time (GST) is the hour angle of the vernal
    equinox, the ascending node of the ecliptic on the celestial equator.

    :param date: The datetime object to convert.
    :return: The Greenwich Sidereal Time (GST) of the given date normalised to UTC.
    """
    JD = get_julian_date(date)

    JD_0 = math.floor(JD - 0.5) + 0.5

    S = JD_0 - J2000

    T = S / 36525.0

    T_0 = (6.697374558 + 2400.051336 * T + 0.000025862 * math.pow(T, 2)) % 24

    if T_0 < 0:
        T_0 += 24

    # Ensure that the date is in UTC
    d = date.astimezone(tz=timezone.utc)

    # Convert the UTC time to a decimal fraction of hours:
    UTC = d.microsecond * 1e-6 + d.second + d.minute * 60 + d.hour

    A = UTC * 1.002737909

    T_0 += A

    GST = T_0 % 24

    return GST + 24 if GST < 0 else GST


def get_local_sidereal_time(date: datetime, longitude: float) -> float:
    """
    The Local Sidereal Time (LST) is the hour angle of the vernal
    equinox, the ascending node of the ecliptic on the celestial equator.

    :param date: The datetime object to convert.
    :param longitude: The longitude of the observer.
    :return: The Local Sidereal Time (LST) of the given date normalised to UTC.
    """
    GST = get_greenwhich_sidereal_time(date.astimezone(tz=timezone.utc))

    d = (GST + longitude / 15.0) / 24.0

    d = d - math.floor(d)

    if d < 0:
        d += 1

    return 24.0 * d


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

    GST = get_greenwhich_sidereal_time(date.astimezone(tz=timezone.utc))

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

    R = 6.6460656 + 2400.051262 * T + 0.00002581 * math.pow(T, 2)

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
