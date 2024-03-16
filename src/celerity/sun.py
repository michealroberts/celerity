# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import asin, atan2, cos, degrees, pow, radians, sin

from .astrometry import get_obliquity_of_the_ecliptic
from .common import EquatorialCoordinate, get_F_orbital_parameter
from .temporal import get_julian_date

# **************************************************************************************


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


# **************************************************************************************


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


# **************************************************************************************


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


# **************************************************************************************


def get_true_anomaly(date: datetime) -> float:
    """
    The true anomaly for the Sun is the angle between the perihelion and the
    current position of the Sun, as seen from the centre of the Earth, corrected
    for the equation of center.

    :param date: The datetime object to convert.
    :return: The true anomaly in degrees.
    """
    # Get the mean anomaly:
    M = get_mean_anomaly(date)

    # Get the equation of center:
    C = get_equation_of_center(date)

    # Correct the mean anomaly for the equation of center:
    return (M + C) % 360


# **************************************************************************************


def get_true_geometric_longitude(date: datetime) -> float:
    """
    The true geometric longitude for the Sun is the angle between the perihelion
    and the current position of the Sun, as seen from the centre of the Earth,
    corrected for the equation of center.

    :param date: The datetime object to convert.
    :return: The true geometric longitude in degrees.
    """
    # Get the mean geometric longitude:
    L = get_mean_geometric_longitude(date)

    # Get the equation of center:
    C = get_equation_of_center(date)

    # Correct the mean geometric longitude for the equation of center:
    return (L + C) % 360


# **************************************************************************************


def get_ecliptic_longitude(date: datetime) -> float:
    """
    The ecliptic longitude for the Sun is the angle between the perihelion and
    the current position of the Sun, as seen from the centre of the Earth,
    corrected for the equation of center and the Sun's ecliptic longitude at
    perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The ecliptic longitude in degrees.
    """
    # Get the true anomaly:
    ν = get_true_anomaly(date)

    # Correct the true anomaly with the Sun's ecliptic longitude
    # at perigee at the epoch:
    λ = ν + 282.938346 % 360

    # Correct for negative angles
    if λ < 0:
        λ += 360

    return λ


# **************************************************************************************


def get_equatorial_coordinate(date: datetime) -> EquatorialCoordinate:
    """
    The equatorial coordinate of the Sun is the standard equatorial coordinate
    of the Sun, as seen from the centre of the Earth, corrected for the equation
    of center and the Sun's ecliptic longitude at perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The equatorial coordinate in degrees.
    """
    # Get the ecliptic longitude:
    λ = radians(get_ecliptic_longitude(date))

    # Get the ecliptic latitude:
    # This term is zero for the Sun, so we can largely ignore it by refactoring
    # the standard equations for the conversion between ecliptic and equatorial
    # coordinates.
    # β = 0

    # Get the obliquity of the ecliptic:
    ε = radians(get_obliquity_of_the_ecliptic(date))

    # Get the corresponding Right Ascension, α:
    ra = degrees(atan2(sin(λ) * cos(ε), cos(λ))) % 360

    # Correct ra for negative angles
    if ra < 0:
        ra += 360

    dec = degrees(asin(sin(ε) * sin(λ)))

    return {"ra": ra, "dec": dec}


# **************************************************************************************


def get_angular_diameter(date: datetime) -> float:
    """
    The angular diameter of the Moon is the angle subtended by the Moon, as seen
    from the centre of the Earth.

    :param date: The datetime object to convert.
    :return: The angular diameter in degrees.
    """
    # Get the true anomaly:
    ν = get_true_anomaly(date)

    # Get the F orbital paramater which applies corrections
    # due to the Sun's orbital eccentricity:
    F = get_F_orbital_parameter(ν, 0.016708)

    return 0.533128 * F


# **************************************************************************************


def get_distance(date: datetime) -> float:
    """
    The distance to the Sun is the distance between the centre of the Earth
    and the centre of the Sun, corrected for the equation of center and the
    Sun's ecliptic longitude at perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The distance in metres.
    """
    # Get the true anomaly:
    ν = get_true_anomaly(date)

    # Get the F orbital paramater which applies corrections
    # due to the Sun's orbital eccentricity:
    F = get_F_orbital_parameter(ν, 0.016708)

    return 1.495985e11 / F


# **************************************************************************************
