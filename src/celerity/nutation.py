# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import cos, radians, sin, tan
from typing import Final, List, Tuple

from .astrometry import get_obliquity_of_the_ecliptic
from .common import EquatorialCoordinate
from .temporal import get_terrestrial_time_in_julian_centuries

# **************************************************************************************

# The luni-solar terms of the IAU 2000B nutation model (McCarthy & Luzum 2003, Celestial
# Mechanics and Dynamical Astronomy 85, 37), being the 77 largest terms of IAU 2000A.
# Each term holds, in order, the integer multipliers of the five Delaunay arguments l,
# l', F, D and Ω, followed by the longitude coefficients of sin(arg), t·sin(arg) and
# cos(arg), and the obliquity coefficients of cos(arg), t·cos(arg) and sin(arg), all in
# units of 0.1 microarcseconds, as tabulated in the IERS Conventions and SOFA nut00b:
IAU2000B_NUTATION_SERIES: Final[
    List[Tuple[int, int, int, int, int, float, float, float, float, float, float]]
] = [
    (0, 0, 0, 0, 1, -172064161, -174666, 33386, 92052331, 9086, 15377),
    (0, 0, 2, -2, 2, -13170906, -1675, -13696, 5730336, -3015, -4587),
    (0, 0, 2, 0, 2, -2276413, -234, 2796, 978459, -485, 1374),
    (0, 0, 0, 0, 2, 2074554, 207, -698, -897492, 470, -291),
    (0, 1, 0, 0, 0, 1475877, -3633, 11817, 73871, -184, -1924),
    (0, 1, 2, -2, 2, -516821, 1226, -524, 224386, -677, -174),
    (1, 0, 0, 0, 0, 711159, 73, -872, -6750, 0, 358),
    (0, 0, 2, 0, 1, -387298, -367, 380, 200728, 18, 318),
    (1, 0, 2, 0, 2, -301461, -36, 816, 129025, -63, 367),
    (0, -1, 2, -2, 2, 215829, -494, 111, -95929, 299, 132),
    (0, 0, 2, -2, 1, 128227, 137, 181, -68982, -9, 39),
    (-1, 0, 2, 0, 2, 123457, 11, 19, -53311, 32, -4),
    (-1, 0, 0, 2, 0, 156994, 10, -168, -1235, 0, 82),
    (1, 0, 0, 0, 1, 63110, 63, 27, -33228, 0, -9),
    (-1, 0, 0, 0, 1, -57976, -63, -189, 31429, 0, -75),
    (-1, 0, 2, 2, 2, -59641, -11, 149, 25543, -11, 66),
    (1, 0, 2, 0, 1, -51613, -42, 129, 26366, 0, 78),
    (-2, 0, 2, 0, 1, 45893, 50, 31, -24236, -10, 20),
    (0, 0, 0, 2, 0, 63384, 11, -150, -1220, 0, 29),
    (0, 0, 2, 2, 2, -38571, -1, 158, 16452, -11, 68),
    (0, -2, 2, -2, 2, 32481, 0, 0, -13870, 0, 0),
    (-2, 0, 0, 2, 0, -47722, 0, -18, 477, 0, -25),
    (2, 0, 2, 0, 2, -31046, -1, 131, 13238, -11, 59),
    (1, 0, 2, -2, 2, 28593, 0, -1, -12338, 10, -3),
    (-1, 0, 2, 0, 1, 20441, 21, 10, -10758, 0, -3),
    (2, 0, 0, 0, 0, 29243, 0, -74, -609, 0, 13),
    (0, 0, 2, 0, 0, 25887, 0, -66, -550, 0, 11),
    (0, 1, 0, 0, 1, -14053, -25, 79, 8551, -2, -45),
    (-1, 0, 0, 2, 1, 15164, 10, 11, -8001, 0, -1),
    (0, 2, 2, -2, 2, -15794, 72, -16, 6850, -42, -5),
    (0, 0, -2, 2, 0, 21783, 0, 13, -167, 0, 13),
    (1, 0, 0, -2, 1, -12873, -10, -37, 6953, 0, -14),
    (0, -1, 0, 0, 1, -12654, 11, 63, 6415, 0, 26),
    (-1, 0, 2, 2, 1, -10204, 0, 25, 5222, 0, 15),
    (0, 2, 0, 0, 0, 16707, -85, -10, 168, -1, 10),
    (1, 0, 2, 2, 2, -7691, 0, 44, 3268, 0, 19),
    (-2, 0, 2, 0, 0, -11024, 0, -14, 104, 0, 2),
    (0, 1, 2, 0, 2, 7566, -21, -11, -3250, 0, -5),
    (0, 0, 2, 2, 1, -6637, -11, 25, 3353, 0, 14),
    (0, -1, 2, 0, 2, -7141, 21, 8, 3070, 0, 4),
    (0, 0, 0, 2, 1, -6302, -11, 2, 3272, 0, 4),
    (1, 0, 2, -2, 1, 5800, 10, 2, -3045, 0, -1),
    (2, 0, 2, -2, 2, 6443, 0, -7, -2768, 0, -4),
    (-2, 0, 0, 2, 1, -5774, -11, -15, 3041, 0, -5),
    (2, 0, 2, 0, 1, -5350, 0, 21, 2695, 0, 12),
    (0, -1, 2, -2, 1, -4752, -11, -3, 2719, 0, -3),
    (0, 0, 0, -2, 1, -4940, -11, -21, 2720, 0, -9),
    (-1, -1, 0, 2, 0, 7350, 0, -8, -51, 0, 4),
    (2, 0, 0, -2, 1, 4065, 0, 6, -2206, 0, 1),
    (1, 0, 0, 2, 0, 6579, 0, -24, -199, 0, 2),
    (0, 1, 2, -2, 1, 3579, 0, 5, -1900, 0, 1),
    (1, -1, 0, 0, 0, 4725, 0, -6, -41, 0, 3),
    (-2, 0, 2, 0, 2, -3075, 0, -2, 1313, 0, -1),
    (3, 0, 2, 0, 2, -2904, 0, 15, 1233, 0, 7),
    (0, -1, 0, 2, 0, 4348, 0, -10, -81, 0, 2),
    (1, -1, 2, 0, 2, -2878, 0, 8, 1232, 0, 4),
    (0, 0, 0, 1, 0, -4230, 0, 5, -20, 0, -2),
    (-1, -1, 2, 2, 2, -2819, 0, 7, 1207, 0, 3),
    (-1, 0, 2, 0, 0, -4056, 0, 5, 40, 0, -2),
    (0, -1, 2, 2, 2, -2647, 0, 11, 1129, 0, 5),
    (-2, 0, 0, 0, 1, -2294, 0, -10, 1266, 0, -4),
    (1, 1, 2, 0, 2, 2481, 0, -7, -1062, 0, -3),
    (2, 0, 0, 0, 1, 2179, 0, -2, -1129, 0, -2),
    (-1, 1, 0, 1, 0, 3276, 0, 1, -9, 0, 0),
    (1, 1, 0, 0, 0, -3389, 0, 5, 35, 0, -2),
    (1, 0, 2, 0, 0, 3339, 0, -13, -107, 0, 1),
    (-1, 0, 2, -2, 1, -1987, 0, -6, 1073, 0, -2),
    (1, 0, 0, 0, 2, -1981, 0, 0, 854, 0, 0),
    (-1, 0, 0, 1, 0, 4026, 0, -353, -553, 0, -139),
    (0, 0, 2, 1, 2, 1660, 0, -5, -710, 0, -2),
    (-1, 0, 2, 4, 2, -1521, 0, 9, 647, 0, 4),
    (-1, 1, 0, 1, 1, 1314, 0, 0, -700, 0, 0),
    (0, -2, 2, -2, 1, -1283, 0, 0, 672, 0, 0),
    (1, 0, 2, 2, 1, -1331, 0, 8, 663, 0, 4),
    (-2, 0, 2, 2, 2, 1383, 0, -2, -594, 0, -2),
    (-1, 0, 0, 0, 2, 1405, 0, 4, -610, 0, 2),
    (1, 1, 2, -2, 2, 1290, 0, 0, -556, 0, 0),
]

# **************************************************************************************

# The fixed offset in longitude (in degrees) standing in for the planetary nutation terms
# omitted from the IAU 2000B model, equal to -0.135 milliarcseconds:
IAU2000B_PLANETARY_NUTATION_IN_LONGITUDE: Final[float] = -0.135 / 3600000

# **************************************************************************************

# The fixed offset in obliquity (in degrees) standing in for the planetary nutation terms
# omitted from the IAU 2000B model, equal to +0.388 milliarcseconds:
IAU2000B_PLANETARY_NUTATION_IN_OBLIQUITY: Final[float] = 0.388 / 3600000

# **************************************************************************************


def get_delaunay_arguments(T: float) -> Tuple[float, float, float, float, float]:
    """
    Gets the five Delaunay arguments of the IAU 2000B nutation model for a particular
    epoch, in radians.

    The arguments are the Simon et al. (1994) expressions truncated to their linear
    terms in T, which is how the IAU 2000B model is specified (McCarthy & Luzum 2003)
    and how SOFA and ERFA evaluate it in nut00b. The quadratic and higher terms are
    omitted deliberately rather than by oversight: their effect on the summed 77-term
    series is below 0.6 milliarcseconds over 1900 to 2100, well inside the accuracy of
    the truncated series, and including them would break the exact agreement with the
    reference implementation without bringing the result closer to IAU 2000A.

    :param T: The Julian centuries of TT since J2000.0.
    :return: The mean anomaly of the Moon l, the mean anomaly of the Sun l', the mean
        argument of the latitude of the Moon F, the mean elongation of the Moon from the
        Sun D and the mean longitude of the ascending node of the Moon Ω, in radians.
    """
    # The mean anomaly of the Moon, l, converted from arcseconds to radians:
    l_moon = radians((485868.249036 + 1717915923.2178 * T) / 3600)

    # The mean anomaly of the Sun, l', converted from arcseconds to radians:
    l_sun = radians((1287104.79305 + 129596581.0481 * T) / 3600)

    # The mean argument of the latitude of the Moon, F, converted from arcseconds to
    # radians:
    F = radians((335779.526232 + 1739527262.8478 * T) / 3600)

    # The mean elongation of the Moon from the Sun, D, converted from arcseconds to
    # radians:
    D = radians((1072260.70369 + 1602961601.2090 * T) / 3600)

    # The mean longitude of the ascending node of the Moon, Ω, converted from arcseconds
    # to radians:
    Ω = radians((450160.398036 - 6962890.5431 * T) / 3600)

    return l_moon, l_sun, F, D, Ω


# **************************************************************************************


def get_nutation_in_longitude(date: datetime) -> float:
    """
    Gets the nutation in longitude for a particular datetime.

    The nutation is evaluated with the IAU 2000B model, which sums the 77 largest
    luni-solar terms of IAU 2000A and adds a fixed offset for the planetary terms. It
    agrees with IAU 2000A to about a milliarcsecond over 1995 to 2050.

    :param date: The datetime object to convert.
    :return: The nutation in longitude in degrees.
    """
    # Get the Julian centuries of TT since J2000.0:
    T = get_terrestrial_time_in_julian_centuries(date)

    # Get the Delaunay arguments (in radians):
    l_moon, l_sun, F, D, Ω = get_delaunay_arguments(T)

    # Sum the luni-solar series (in units of 0.1 microarcseconds):
    Δψ = 0.0

    for nl, nlp, nF, nD, nΩ, ps, pst, pc, _, _, _ in IAU2000B_NUTATION_SERIES:
        argument = nl * l_moon + nlp * l_sun + nF * F + nD * D + nΩ * Ω

        Δψ += (ps + pst * T) * sin(argument) + pc * cos(argument)

    # Convert from 0.1 microarcseconds to degrees and add the planetary offset:
    return Δψ / 36000000000 + IAU2000B_PLANETARY_NUTATION_IN_LONGITUDE


# **************************************************************************************


def get_nutation_in_obliquity(date: datetime) -> float:
    """
    Gets the nutation in obliquity for a particular datetime.

    The nutation is evaluated with the IAU 2000B model, which sums the 77 largest
    luni-solar terms of IAU 2000A and adds a fixed offset for the planetary terms. It
    agrees with IAU 2000A to about a milliarcsecond over 1995 to 2050.

    :param date: The datetime object to convert.
    :return: The nutation in obliquity in degrees.
    """
    # Get the Julian centuries of TT since J2000.0:
    T = get_terrestrial_time_in_julian_centuries(date)

    # Get the Delaunay arguments (in radians):
    l_moon, l_sun, F, D, Ω = get_delaunay_arguments(T)

    # Sum the luni-solar series (in units of 0.1 microarcseconds):
    Δε = 0.0

    for nl, nlp, nF, nD, nΩ, _, _, _, ec, ect, es in IAU2000B_NUTATION_SERIES:
        argument = nl * l_moon + nlp * l_sun + nF * F + nD * D + nΩ * Ω

        Δε += (ec + ect * T) * cos(argument) + es * sin(argument)

    # Convert from 0.1 microarcseconds to degrees and add the planetary offset:
    return Δε / 36000000000 + IAU2000B_PLANETARY_NUTATION_IN_OBLIQUITY


# **************************************************************************************


def get_correction_to_equatorial_for_nutation(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for nutation in longitude and obliquity.

    :param date: The datetime object to convert.
    :param longitude: The longitude of the observer in degrees.
    :param target: The equatorial coordinates of the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    # Get the nutation in longitude (in degrees)
    Δψ = get_nutation_in_longitude(date)

    # Get the nutation in obliquity (in degrees)
    Δε = get_nutation_in_obliquity(date)

    # Get the true obliquity of the ecliptic (in degrees):
    ε = radians(get_obliquity_of_the_ecliptic(date) + Δε)

    # The trigonometric factors are dimensionless, and Δψ and Δε are already in
    # degrees, so no further unit conversion is applied here.

    # Calculate the nutation correction in right ascension (in degrees)
    Δra = (cos(ε) + sin(ε) * sin(ra) * tan(dec)) * Δψ - cos(ra) * tan(dec) * Δε

    # Calculate the nutation correction in declination (in degrees)
    Δdec = sin(ε) * cos(ra) * Δψ + sin(ra) * Δε

    return {"ra": Δra, "dec": Δdec}


# **************************************************************************************
