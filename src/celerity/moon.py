import math
from datetime import datetime

from .epoch import get_number_of_fractional_days_since_j2000
from .sun import get_mean_anomaly


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
    M = get_mean_anomaly(date)

    return Ω - 0.16 * math.sin(math.radians(M))
