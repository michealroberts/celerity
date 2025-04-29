# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from enum import Enum
from math import acos, asin, atan2, cos, degrees, pow, radians, sin, tan

from .astrometry import get_obliquity_of_the_ecliptic
from .common import Age, EquatorialCoordinate, get_F_orbital_parameter
from .epoch import get_number_of_fractional_days_since_j2000
from .sun import get_ecliptic_longitude as get_mean_solar_ecliptic_longitude
from .sun import get_ecliptic_longitude as get_solar_ecliptic_longitude
from .sun import get_mean_anomaly as get_solar_mean_anomaly
from .temporal import get_julian_date

# **************************************************************************************


class Phase(Enum):
    New = "New"
    WaxingCrescent = "Waxing Crescent"
    FirstQuarter = "First Quarter"
    WaxingGibbous = "Waxing Gibbous"
    Full = "Full"
    WaningGibbous = "Waning Gibbous"
    LastQuarter = "Last Quarter"
    WaningCrescent = "Waning Crescent"


# **************************************************************************************


def get_annual_equation_correction(date: datetime) -> float:
    # Correct for the Sun's mean anomaly:
    M = radians(get_solar_mean_anomaly(date))

    # Get the annual equation correction:
    return 0.1858 * sin(M)


# **************************************************************************************


def get_evection_correction(date: datetime) -> float:
    # Get the Moon's mean anomaly at the current epoch relative to J2000:
    M = radians(get_mean_anomaly(date))

    # Get the Moon's mean ecliptic longitude:
    λ = radians(get_mean_ecliptic_longitude(date))

    # Get the Sun's mean ecliptic longitude:
    longitude = radians(get_mean_solar_ecliptic_longitude(date))

    # Get the avection correction:
    return 1.2739 * sin(2 * (λ - longitude) - M)


# **************************************************************************************


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


# **************************************************************************************


def get_mean_anomaly_correction(date: datetime) -> float:
    # Get the annual equation correction:
    Ae = get_annual_equation_correction(date)

    # Get the evection correction:
    Ev = get_evection_correction(date)

    # Get the mean anomaly for the Moon:
    M = get_mean_anomaly(date)

    # Correct for the Sun's mean anomaly:
    S = radians(get_solar_mean_anomaly(date))

    # Get the mean anomaly correction:
    Ca = (M + Ev - Ae - 0.37 * sin(S)) % 360

    # Correct for negative angles
    if Ca < 0:
        Ca += 360

    return Ca


# **************************************************************************************


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

    longitude = (
        218.3164477
        + 481267.88123421 * T
        - 0.0015786 * pow(T, 2)
        + pow(T, 3) / 538841
        - pow(T, 4) / 65194000
    ) % 360

    # Correct for negative angles
    if longitude < 0:
        longitude += 360

    return longitude


# **************************************************************************************


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


# **************************************************************************************


def get_mean_ecliptic_longitude(date: datetime) -> float:
    """
    The mean lunar ecliptic longitude is the ecliptic longitude of the Moon
    if the Moon's orbit where free of perturbations

    :param date: The datetime object to convert.
    :return: The mean lunar ecliptic longitude in degrees
    """
    # Get the number of days since the standard epoch J2000:
    De = get_number_of_fractional_days_since_j2000(date)

    # Get the uncorrected mean eclptic longitude:
    λ = (13.176339686 * De + 218.31643388) % 360

    # Correct for negative angles
    if λ < 0:
        λ += 360

    return λ


# **************************************************************************************


def get_true_anomaly(date: datetime) -> float:
    """
    The true anomaly of the Moon is the angle between the perihelion and the
    current position of the Moon, as seen from the Earth.

    :param date: The datetime object to convert.
    :return: The true anomaly in degrees.
    """
    # Get the mean anomaly correction:
    Ca = get_mean_anomaly_correction(date)

    # Get the true anomaly:
    ν = 6.2886 * sin(radians(Ca)) + 0.214 * sin(radians(2 * Ca))

    # Correct for negative angles
    if ν < 0:
        ν += 360

    return ν


# **************************************************************************************


def get_true_ecliptic_longitude(date: datetime) -> float:
    """
    The corrected lunar ecliptic longitude is the ecliptic longitude of the Moon
    if the Moon's orbit where free of perturbations

    :param date: The datetime object to convert.
    :return: The corrected lunar ecliptic longitude in degrees
    """
    # Get the mean ecliptic longitude:
    λ = get_mean_ecliptic_longitude(date)

    # Get the
    Ae = get_annual_equation_correction(date)

    # Get the evection correction:
    Ev = get_evection_correction(date)

    # Get the true anomaly:
    ν = get_true_anomaly(date)

    # Get the corrected ecliptic longitude:
    λ = (λ + Ev + ν - Ae) % 360

    # Correct for negative angles
    if λ < 0:
        λ += 360

    # Get the solar ecliptic longitude:
    L = get_solar_ecliptic_longitude(date)

    # Get the correction of variation:
    V = 0.6583 * sin(2 * radians(λ - L))

    λt = (λ + V) % 360

    # Correct for negative angles
    if λt < 0:
        λt += 360

    return λt


# **************************************************************************************


def get_corrected_ecliptic_longitude_of_the_ascending_node(date: datetime) -> float:
    """
    The corrected ecliptic longitude of the ascending node is the angle where
    the Moon's orbit crosses the ecliptic corrected for perturbations in the
    Moon's orbit due to the Sun

    :param date: The datetime object to convert.
    :return: The corrected ecliptic longitude of the ascending node of the Moon in degrees
    """
    # Get the ecliptic longitude of the ascending node:
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date)

    # Get the solar mean anomaly:
    M = get_solar_mean_anomaly(date)

    return Ω - 0.16 * sin(radians(M))


# **************************************************************************************


def get_ecliptic_longitude(date: datetime) -> float:
    """
    The ecliptic longitude for the Mon is the angle between the perihelion and
    the current position of the Mon, as seen from the centre of the Earth,
    corrected for the equation of center and the Mon's ecliptic longitude at
    perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The ecliptic longitude in degrees.
    """
    # Get the true ecliptic longitude:
    λt = get_true_ecliptic_longitude(date)

    # Get the corrected ecliptic longitude of the ascending node:
    Ωcorr = get_corrected_ecliptic_longitude_of_the_ascending_node(date)

    # Get the Moon's orbital inclination:
    ι = radians(5.1453964)

    # Calculate the ecliptic longitude of the Moon (in degrees):
    λ = Ωcorr + degrees(
        atan2(sin(radians(λt - Ωcorr)) * cos(ι), cos(radians(λt - Ωcorr)))
    )

    # Correct for negative angles
    if λ < 0:
        λ += 360

    return λ


# **************************************************************************************


def get_ecliptic_latitude(date: datetime) -> float:
    """
    The ecliptic latitude for the Mon is the angle between the ecliptic and
    the current position of the Mon, as seen from the centre of the Earth,
    corrected for the equation of center and the Mon's ecliptic longitude at
    perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The ecliptic latitude in degrees.
    """
    # Get the true ecliptic longitude:
    λt = get_true_ecliptic_longitude(date)

    # Get the corrected ecliptic longitude of the ascending node:
    Ωcorr = get_corrected_ecliptic_longitude_of_the_ascending_node(date)

    # Get the Moon's orbital inclination:
    ι = radians(5.1453964)

    # Calculate the ecliptic longitude of the Moon (in degrees):
    β = degrees(asin(sin(radians(λt - Ωcorr)) * sin(ι)))

    return β


# **************************************************************************************


def get_equatorial_coordinate(date: datetime) -> EquatorialCoordinate:
    """
    The equatorial coordinate of the Moon is the standard equatorial coordinate
    of the Moon, as seen from the centre of the Earth, corrected for the equation
    of center and the Moon's ecliptic longitude at perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The equatorial coordinate in degrees.
    """
    # Get the ecliptic longitude:
    λ = radians(get_ecliptic_longitude(date))

    # Get the ecliptic latitude:
    β = radians(get_ecliptic_latitude(date))

    # Get the obliquity of the ecliptic:
    ε = radians(get_obliquity_of_the_ecliptic(date))

    # Get the corresponding Right Ascension, α:
    ra = degrees(atan2(sin(λ) * cos(ε) - tan(β) * sin(ε), cos(λ))) % 360

    # Correct ra for negative angles
    if ra < 0:
        ra += 360

    dec = degrees(asin(sin(β) * cos(ε) + cos(β) * sin(ε) * sin(λ)))

    return {"ra": ra, "dec": dec}


# **************************************************************************************


def get_elongation(date: datetime):
    """
    The elongation of the Moon is the angle between the Sun and the Moon, as
    seen from the reference observer Earth.

    :param date:
    :return: The Lunar elongation in degrees.
    """
    # Get the ecliptic longitude:
    λ = get_ecliptic_longitude(date)

    # Get the ecliptic latitude:
    β = radians(get_ecliptic_latitude(date))

    # Get the solar ecliptic longitude:
    λS = get_solar_ecliptic_longitude(date)

    # Get the age of the Moon in degrees:
    d = degrees(acos(cos(radians(λ - λS)) * cos(β))) % 360

    if d < 0:
        d += 360

    return d


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
    # due to the Moon's orbital eccentricity:
    F = get_F_orbital_parameter(ν, 0.0549)

    return 0.5181 * F


# **************************************************************************************


def get_distance(date: datetime) -> float:
    """
    The distance to the Moon is the distance between the centre of the Earth
    and the centre of the Moon, corrected for the equation of center and the
    Moon's ecliptic longitude at perigee at the epoch.

    :param date: The datetime object to convert.
    :return: The distance in metres.
    """
    # Get the true anomaly:
    ν = get_true_anomaly(date)

    # Get the F orbital paramater which applies corrections
    # due to the Moon's orbital eccentricity:
    F = get_F_orbital_parameter(ν, 0.0549)

    return 3.84400e8 / F


# **************************************************************************************


def get_age(date: datetime) -> Age:
    """
    The age of the Moon is calculated by ascertaining the number of degrees
    the Moon has traversed in it's orbit, given that it takes the Moon
    29.5306 days to traverse a full 360° in one orbit cycle.

    :param date: The datetime object to convert.
    :return: The age of the Moon in both degrees and days.
    """

    # Get the true ecliptic longitude:
    λt = get_true_ecliptic_longitude(date)

    # Get the solar ecliptic longitude:
    λ = get_solar_ecliptic_longitude(date)

    # Get the Moon's age in degrees:
    A = (λt - λ) % 360

    # correct for negative angles:
    if A < 0:
        A += 360

    # Get the Moon's age in days by multiplying the age, A,
    # by the number of degrees traversed per day given that
    # the Moon orbits the Earth every 29.5306 days:
    age = A * (29.5306 / 360)

    return {"A": A, "a": age}


# **************************************************************************************


def get_phase_angle(date: datetime) -> float:
    """
    The phase angle of the Moon is the angle subtended by the incident
    light from the Sun as seen from the Earth's line of sight.

    :param date: The datetime object to convert.
    :return: The phase angle of the Moon in degrees.
    """
    # Get the mean anomaly:
    M = radians(get_mean_anomaly(date))

    # Get the age of the Moon in degrees (elongation):
    d = get_elongation(date)

    # Get the phase angle of the Moon in degrees:
    PA = (
        180
        - d
        - (
            0.1468
            * ((1 - (0.0549 * sin(M))) / (1 - (0.0167 * sin(M))))
            * sin(radians(d))
        )
    )

    return PA


# **************************************************************************************


def get_illumination(date: datetime) -> float:
    """
    The total percentage illumination of the Moon as seen from Earth
    (i.e., the visible portion of the Moon), not to be confused with
    the total illumination of the Moon by the Sun which is always 50%.

    :param date: The datetime object to convert.
    :return: The visible portion illumination of the Moon (in unitless %)
    """
    # Get the phase angle:
    PA = get_phase_angle(date)

    # Get the total illuminated % fraction:
    return 50 * (1 + cos(radians(PA)))


# **************************************************************************************


def get_phase(date: datetime) -> Phase:
    """
    Get the human readable phase name, e.g., "New Moon" of the Moon.

    :param date: The datetime object to convert.
    :return: The phase of the Moon.
    """
    # Get the age of the Moon:
    d = get_age(date)

    # Get the age of the Moon in degrees:
    D = d["a"]

    if D >= 3.7 and D < 7.4:
        return Phase.WaxingCrescent

    if D >= 7.4 and D < 11.1:
        return Phase.FirstQuarter

    if D >= 11.1 and D < 14.6:
        return Phase.WaxingGibbous

    if D >= 14.6 and D < 15.0:
        return Phase.Full

    if D >= 15.0 and D < 22.1:
        return Phase.WaningGibbous

    if D >= 22.1 and D < 25.8:
        return Phase.LastQuarter

    if D >= 25.8 and D < 29.5:
        return Phase.WaningCrescent

    return Phase.New


# **************************************************************************************
