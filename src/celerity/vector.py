# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import atan2, cos, degrees, hypot, radians, sin
from typing import Tuple

from .common import EquatorialCoordinate

# **************************************************************************************

# A three-dimensional Cartesian vector, as (x, y, z) components:
Vector = Tuple[float, float, float]

# **************************************************************************************


def convert_equatorial_to_vector(target: EquatorialCoordinate) -> Vector:
    """
    The unit vector of direction cosines of an equatorial coordinate.

    :param target: The equatorial coordinate of the target.
    :return: The unit vector pointing toward the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    return (cos(dec) * cos(ra), cos(dec) * sin(ra), sin(dec))


# **************************************************************************************


def convert_vector_to_equatorial(vector: Vector) -> EquatorialCoordinate:
    """
    The equatorial coordinate of a direction vector, which need not be of unit length.

    :param vector: The vector pointing toward the target.
    :return: The equatorial coordinate of the target, with right ascension in [0, 360).
    """
    x, y, z = vector

    # Calculate the right ascension (in degrees), normalised to the range [0, 360):
    ra = degrees(atan2(y, x)) % 360

    # Calculate the declination (in degrees), using atan2 rather than asin so that the
    # result remains well conditioned close to the celestial poles:
    dec = degrees(atan2(z, hypot(x, y)))

    return {"ra": ra, "dec": dec}


# **************************************************************************************
