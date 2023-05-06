from datetime import datetime

from .epoch import get_number_of_fractional_days_since_j2000


def get_mean_anomaly(date: datetime, longitude: float) -> float:
    """
    The mean anomaly is the angle between the perihelion and the current position
    of the planet, as seen from the Sun.

    :param date: The datetime object to convert.
    :return: The mean anomaly in degrees
    """
    # Get the number of days since the standard epoch J2000:
    d = get_number_of_fractional_days_since_j2000(date) - longitude / 360

    # Get the Sun's mean anomaly at the current epoch relative to J2000:
    M = (357.5291092 + (0.98560028 * d)) % 360

    # Correct for negative angles
    if M < 0:
        M += 360

    return M
