# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import cos, radians, sin
from typing import Tuple

from .vector import Vector

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


def multiply_matrices(a: Matrix, b: Matrix) -> Matrix:
    """
    The product a·b of two matrices, which as rotations applies b first and then a.

    :param a: The matrix applied second.
    :param b: The matrix applied first.
    :return: The product matrix.
    """
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1],
            a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1],
            a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2],
        ),
        (
            a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0],
            a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1],
            a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2],
        ),
    )


# **************************************************************************************


def apply_matrix(matrix: Matrix, vector: Vector) -> Vector:
    """
    The product matrix·vector, giving the components of the vector in the rotated frame.

    :param matrix: The matrix to apply.
    :param vector: The vector to apply it to.
    :return: The transformed vector.
    """
    x, y, z = vector

    return (
        matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z,
        matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z,
        matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z,
    )


# **************************************************************************************
