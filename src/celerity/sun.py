from datetime import datetime
from math import pow, radians, sin

from .temporal import get_julian_date


def get_equation_of_center(date) -> float:
    """
    The equation of center is the difference between the mean geometric longitude
    and the mean anomaly.

    :param date: The datetime object to convert.
    :return: The equation of center in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    # Get the mean anomaly:
    M = get_mean_anomaly(date)

    # Calculate the equation of center:
    C = (
        (1.914602 - 0.004817 * pow(T, 2) - 0.000014 * pow(T, 3)) * sin(radians(M))
        + (0.019993 - 0.000101 * pow(T, 2)) * sin(radians(2 * M))
        + 0.000289 * sin(radians(3 * M))
    )

    return C


def get_mean_anomaly(date: datetime) -> float:
    """
    The mean anomaly is the angle between the perihelion and the current position
    of the planet, as seen from the Sun.

    :param date: The datetime object to convert.
    :return: The mean anomaly in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    # Get the Sun's mean anomaly at the current epoch relative to J2000:
    M = (357.52911 + 35999.05029 * T - 0.0001537 * pow(T, 2)) % 360

    # Correct for negative angles
    if M < 0:
        M += 360

    return M


def get_mean_geometric_longitude(date: datetime) -> float:
    """
    The mean geometric longitude for the Sun is the angle between the perihelion
    and the current position of the Sun, as seen from the centre of the Earth.

    :param date: The datetime object to convert.
    :return: The mean geometric longitude in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    # Calculate the mean geometric longitude:
    L = (280.46646 + 36000.76983 * T + 0.0003032 * pow(T, 2)) % 360

    # Correct for negative angles
    if L < 0:
        L += 360

    return L


def get_true_geometric_longitude(date: datetime) -> float:
    """
    The true geometric longitude for the Sun is the angle between the perihelion
    and the current position of the Sun, as seen from the centre of the Earth,
    corrected for the equation of center.

    :param date: The datetime object to convert.
    :return: The true geometric longitude in degrees.
    """
    # Get the Julian date:
    L = get_mean_geometric_longitude(date)

    C = get_equation_of_center(date)

    return (L + C) % 360
