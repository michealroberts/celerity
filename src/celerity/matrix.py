# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import cos, radians, sin
from typing import Tuple

# **************************************************************************************

# A three-by-three matrix, as three row tuples:
Matrix = Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    Tuple[float, float, float],
]

# **************************************************************************************


def get_rotation_matrix_about_x(angle: float) -> Matrix:
    """
    The matrix that rotates the reference frame about the x axis.

    The convention follows SOFA, where a positive angle rotates the frame anticlockwise
    as seen from the positive end of the axis, so that applying the matrix to a vector
    gives its components in the rotated frame.

    :param angle: The angle to rotate the frame through (in degrees).
    :return: The rotation matrix.
    """
    # Get the cosine of the angle (dimensionless):
    c = cos(radians(angle))

    # Get the sine of the angle (dimensionless):
    s = sin(radians(angle))

    return ((1.0, 0.0, 0.0), (0.0, c, s), (0.0, -s, c))


# **************************************************************************************


def get_rotation_matrix_about_y(angle: float) -> Matrix:
    """
    The matrix that rotates the reference frame about the y axis.

    The convention follows SOFA, where a positive angle rotates the frame anticlockwise
    as seen from the positive end of the axis, so that applying the matrix to a vector
    gives its components in the rotated frame.

    :param angle: The angle to rotate the frame through (in degrees).
    :return: The rotation matrix.
    """
    # Get the cosine of the angle (dimensionless):
    c = cos(radians(angle))

    # Get the sine of the angle (dimensionless):
    s = sin(radians(angle))

    return ((c, 0.0, -s), (0.0, 1.0, 0.0), (s, 0.0, c))


# **************************************************************************************


def get_rotation_matrix_about_z(angle: float) -> Matrix:
    """
    The matrix that rotates the reference frame about the z axis.

    The convention follows SOFA, where a positive angle rotates the frame anticlockwise
    as seen from the positive end of the axis, so that applying the matrix to a vector
    gives its components in the rotated frame.

    :param angle: The angle to rotate the frame through (in degrees).
    :return: The rotation matrix.
    """
    # Get the cosine of the angle (dimensionless):
    c = cos(radians(angle))

    # Get the sine of the angle (dimensionless):
    s = sin(radians(angle))

    return ((c, s, 0.0), (-s, c, 0.0), (0.0, 0.0, 1.0))


# **************************************************************************************
