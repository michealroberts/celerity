from datetime import datetime
from math import pow, radians, sin

from .epoch import get_number_of_fractional_days_since_j2000
from .sun import get_mean_anomaly as get_solar_mean_anomaly
from .temporal import get_julian_date


def get_mean_anomaly(date: datetime) -> float:
    """
    The mean anomaly is the angle between the perihelion and the current position
    of the planet, as seen from the Moon.

    :param date: The datetime object to convert.
    :return: The mean anomaly in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    # Get the Moon's mean anomaly at the current epoch relative to J2000:
    M = (
        134.9634114
        + 477198.8676313 * T
        + 0.008997 * pow(T, 2)
        + pow(T, 3) / 69699
        - pow(T, 4) / 14712000
    ) % 360

    # Correct for negative angles
    if M < 0:
        M += 360

    return M


def get_mean_geometric_longitude(date: datetime) -> float:
    """
    The mean lunar geometric longitude is the ecliptic longitude of the
    Moon if the Moon's orbit where free of perturbations

    :param date: The datetime object to convert.
    :return: The mean lunar geometric longitude in degrees
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    l = (
        218.3164477
        + 481267.88123421 * T
        - 0.0015786 * pow(T, 2)
        + pow(T, 3) / 538841
        - pow(T, 4) / 65194000
    ) % 360

    # Correct for negative angles
    if l < 0:
        l += 360

    return l


def get_mean_ecliptic_longitude_of_the_ascending_node(date: datetime) -> float:
    """
    The mean lunar ecliptic longitude of the ascending node is the angle where
    the Moon's orbit crosses the ecliptic

    :param date: The datetime object to convert.
    :return: The mean lunar ecliptic longitude of the ascending node in degrees
    """
    # Get the number of days since the standard epoch J2000:
    d = get_number_of_fractional_days_since_j2000(date)

    # Get the Moon's ecliptic longitude of the ascending node at the current epoch relative to J2000:
    Ω = (125.044522 - (0.0529539 * d)) % 360

    # Correct for negative angles
    if Ω < 0:
        Ω += 360

    # Correct for the Sun's mean anomaly:
    M = radians(get_solar_mean_anomaly(date))

    return Ω - 0.16 * sin(M)
