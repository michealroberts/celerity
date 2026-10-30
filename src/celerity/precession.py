# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import atan2, cos, degrees, hypot, radians, sin

from .common import EquatorialCoordinate
from .matrix import (
    Matrix,
    get_rotation_matrix_about_x,
    get_rotation_matrix_about_y,
    get_rotation_matrix_about_z,
    multiply_matrices,
)
from .temporal import get_terrestrial_time_in_julian_centuries

# **************************************************************************************

# The frame bias in longitude between the ICRS and the mean equator and equinox of
# J2000.0 (in arcseconds), from the IAU 2000 precession-nutation model:
FRAME_BIAS_IN_LONGITUDE: float = -0.041775

# **************************************************************************************

# The frame bias in obliquity between the ICRS and the mean equator and equinox of
# J2000.0 (in arcseconds), from the IAU 2000 precession-nutation model:
FRAME_BIAS_IN_OBLIQUITY: float = -0.0068192

# **************************************************************************************

# The ICRS right ascension of the J2000.0 mean equinox (in arcseconds), from the IAU
# 2000 precession-nutation model:
FRAME_BIAS_IN_RIGHT_ASCENSION: float = -0.0146

# **************************************************************************************

# The mean obliquity of the ecliptic at J2000.0 (in arcseconds) of the IAU 1976 system,
# in which the frame bias offsets are expressed:
OBLIQUITY_AT_J2000: float = 84381.448

# **************************************************************************************


def get_frame_bias_matrix() -> Matrix:
    """
    The matrix that rotates a direction from the International Celestial Reference
    System (ICRS) to the mean equator and equinox of J2000.0.

    The bias is a fixed rotation of about 23 milliarcseconds (IERS Conventions 2003,
    chapter 5), formed from the ICRS right ascension of the J2000.0 mean equinox and the
    offsets of the J2000.0 mean pole in longitude and obliquity.

    :return: The frame bias rotation matrix.
    """
    # Get the rotation about the z axis through the right ascension offset (in degrees):
    rz = get_rotation_matrix_about_z(FRAME_BIAS_IN_RIGHT_ASCENSION / 3600)

    # Get the rotation about the y axis through the pole offset in longitude projected
    # onto the equator by the obliquity (in degrees):
    ry = get_rotation_matrix_about_y(
        FRAME_BIAS_IN_LONGITUDE * sin(radians(OBLIQUITY_AT_J2000 / 3600)) / 3600
    )

    # Get the rotation about the x axis through the pole offset in obliquity (in degrees):
    rx = get_rotation_matrix_about_x(-FRAME_BIAS_IN_OBLIQUITY / 3600)

    return multiply_matrices(rx, multiply_matrices(ry, rz))


# **************************************************************************************


def get_precession_matrix(date: datetime) -> Matrix:
    """
    The matrix that rotates a direction from the mean equator and equinox of J2000.0 to
    the mean equator and equinox of date.

    The rotation follows the IAU 2006 precession model (Capitaine, Wallace & Chapront
    2003, A&A 412, 567, eq. 40, the P03 solution adopted by IAU 2006 Resolution B1),
    with the equatorial precession angles ζ, z and θ evaluated in Terrestrial Time (TT).

    :param date: The date to form the precession matrix for.
    :return: The precession rotation matrix.
    """
    # Get the Julian centuries of TT since J2000.0:
    T = get_terrestrial_time_in_julian_centuries(date)

    # The IAU 2006 equatorial precession angle ζ (in arcseconds):
    ζ = (
        2.650545
        + 2306.083227 * T
        + 0.2988499 * T**2
        + 0.01801828 * T**3
        - 0.000005971 * T**4
        - 0.0000003173 * T**5
    )

    # The IAU 2006 equatorial precession angle z (in arcseconds):
    z = (
        -2.650545
        + 2306.077181 * T
        + 1.0927348 * T**2
        + 0.01826837 * T**3
        - 0.000028596 * T**4
        - 0.0000002904 * T**5
    )

    # The IAU 2006 equatorial precession angle θ (in arcseconds):
    θ = (
        2004.191903 * T
        - 0.4294934 * T**2
        - 0.04182264 * T**3
        - 0.000007089 * T**4
        - 0.0000001274 * T**5
    )

    # Get the rotation about the z axis through -ζ (in degrees):
    rζ = get_rotation_matrix_about_z(-ζ / 3600)

    # Get the rotation about the y axis through θ (in degrees):
    rθ = get_rotation_matrix_about_y(θ / 3600)

    # Get the rotation about the z axis through -z (in degrees):
    rz = get_rotation_matrix_about_z(-z / 3600)

    return multiply_matrices(rz, multiply_matrices(rθ, rζ))


# **************************************************************************************


def get_correction_to_equatorial_for_precession_of_equinoxes(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for the precession of the equinoxes.

    The correction is the difference between the mean place of date and the mean place
    at J2000.0, following the IAU 2006 precession model (Capitaine, Wallace & Chapront
    2003, A&A 412, 567, eq. 40, the P03 solution adopted by IAU 2006 Resolution B1).
    The equatorial precession angles ζ, z and θ are evaluated in Terrestrial Time (TT)
    and the J2000.0 coordinate is rotated through them.

    :param date: The date to correct the equatorial coordinates for.
    :param target: The equatorial J2000 coordinates of the target.
    :return: The corrected equatorial coordinates of the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    # Get the Julian centuries of TT since J2000.0:
    T = get_terrestrial_time_in_julian_centuries(date)

    # The IAU 2006 equatorial precession angle ζ (in arcseconds):
    ζ = (
        2.650545
        + 2306.083227 * T
        + 0.2988499 * T**2
        + 0.01801828 * T**3
        - 0.000005971 * T**4
        - 0.0000003173 * T**5
    )

    # The IAU 2006 equatorial precession angle z (in arcseconds):
    z = (
        -2.650545
        + 2306.077181 * T
        + 1.0927348 * T**2
        + 0.01826837 * T**3
        - 0.000028596 * T**4
        - 0.0000002904 * T**5
    )

    # The IAU 2006 equatorial precession angle θ (in arcseconds):
    θ = (
        2004.191903 * T
        - 0.4294934 * T**2
        - 0.04182264 * T**3
        - 0.000007089 * T**4
        - 0.0000001274 * T**5
    )

    # Convert the precession angles from arcseconds to radians:
    ζ, z, θ = radians(ζ / 3600), radians(z / 3600), radians(θ / 3600)

    # Rotate the J2000.0 direction cosines through the precession angles (Meeus,
    # Astronomical Algorithms, 21.4), where A and B give the precessed right ascension
    # and C the precessed declination:
    A = cos(dec) * sin(ra + ζ)

    B = cos(θ) * cos(dec) * cos(ra + ζ) - sin(θ) * sin(dec)

    C = sin(θ) * cos(dec) * cos(ra + ζ) + cos(θ) * sin(dec)

    # The precessed right ascension (in degrees):
    α = degrees(atan2(A, B) + z)

    # The precessed declination (in degrees), using atan2 rather than asin so that the
    # result remains well conditioned close to the celestial poles:
    δ = degrees(atan2(C, hypot(A, B)))

    # The correction in right ascension, normalised to the range [-180, 180) degrees so
    # that a wrap of the precessed right ascension through 0 or 360 does not appear as
    # a full-circle correction:
    Δra = (α - target["ra"] + 180) % 360 - 180

    # The correction in declination (in degrees):
    Δdec = δ - target["dec"]

    return {"ra": Δra, "dec": Δdec}


# **************************************************************************************
