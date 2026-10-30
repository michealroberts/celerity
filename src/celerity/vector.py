# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import cos, radians, sin
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
