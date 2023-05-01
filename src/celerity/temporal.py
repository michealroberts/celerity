import math
from datetime import datetime, timezone

from .constants import J2000


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
    GST = get_greenwhich_sidereal_time(date)

    d = (GST + longitude / 15.0) / 24.0

    d = d - math.floor(d)

    if d < 0:
        d += 1

    return 24.0 * d
