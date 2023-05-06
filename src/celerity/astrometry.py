from datetime import datetime
from math import atan2, cos, degrees, pow, radians, sin, tan

from .common import EquatorialCoordinate, GeographicCoordinate
from .temporal import get_julian_date, get_local_sidereal_time


def get_hour_angle(date: datetime, ra: float, longitude: float) -> float:
    """
    Gets the hour angle for a particular object for a particular observer at a given datetime

    :param date: The datetime object to convert.
    :param ra: The right ascension of the observed object's equatorial coordinate in degrees.
    :param longitude: The longitude of the observer in degrees.
    :return The hour angle in degrees.
    """
    LST = get_local_sidereal_time(date, longitude)

    ha = LST * 15 - ra

    # If the hour angle is less than zero, ensure we rotate by 2π radians (360 degrees)
    if ha < 0:
        ha += 360

    return ha


def get_obliquity_of_the_ecliptic(date: datetime) -> float:
    """
    Gets the obliquity of the ecliptic for a particular datetime

    The obliquity of the ecliptic is the angle between the ecliptic and the celestial equator, and is used to
    convert between ecliptic and equatorial coordinates.

    :param date: The datetime object to convert.
    :return The obliquity of the ecliptic in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    # Calculate the obliquity of the ecliptic:
    return 23.439292 - (46.845 * T + 0.00059 * pow(T, 2) + 0.001813 * pow(T, 3)) / 3600


def get_parallactic_angle(
    date: datetime,
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
) -> float:
    """
    Gets the parallactic angle for a particular object for a particular observer at a given datetime

    :param date: The datetime object to convert.
    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :return The parallactic angle in degrees.
    """
    lat, lon = radians(observer["lat"]), observer["lon"]

    dec = radians(target["dec"])

    # Get the hour angle for the target:
    ha = radians(get_hour_angle(date, target["ra"], lon))

    # Calculate the parallactic angle and return in degrees:
    return degrees(
        atan2(
            sin(ha),
            tan(lat) * cos(dec) - sin(dec) * cos(ha),
        )
    )
