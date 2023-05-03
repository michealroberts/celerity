from datetime import datetime

from .temporal import get_local_sidereal_time


def get_hour_angle(date: datetime, ra: float, longitude: float) -> float:
    """
    Gets the hour angle for a particular object for a particular observer at a given datetime

    :param date: The datetime object to convert.
    :param ra: The right ascension of the observed object's equatorial coordinate in degrees.
    :param longitude: The longitude of the observer in degrees.
    """
    LST = get_local_sidereal_time(date, longitude)

    ha = LST * 15 - ra

    # If the hour angle is less than zero, ensure we rotate by 2π radians (360 degrees)
    if ha < 0:
        ha += 360

    return ha
