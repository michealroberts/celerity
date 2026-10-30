# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import isclose
from typing import get_args

from src.celerity.matrix import (
    Matrix,
    get_rotation_matrix_about_x,
    get_rotation_matrix_about_y,
    get_rotation_matrix_about_z,
)

# **************************************************************************************


def test_matrix_has_three_rows():
    assert len(get_args(Matrix)) == 3


# **************************************************************************************


def test_matrix_rows_have_three_float_components():
    for row in get_args(Matrix):
        assert get_args(row) == (float, float, float)


# **************************************************************************************


def test_matrix_accepts_a_three_by_three_tuple():
    identity: Matrix = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    assert len(identity) == 3
    assert all(len(row) == 3 for row in identity)


# **************************************************************************************


def test_get_rotation_matrix_about_x_zero_angle_is_identity():
    assert get_rotation_matrix_about_x(0.0) == (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


# **************************************************************************************


def test_get_rotation_matrix_about_x_30_degrees():
    r = get_rotation_matrix_about_x(30.0)
    assert r[0] == (1.0, 0.0, 0.0)
    assert r[1] == (0.0, 0.8660254037844387, 0.49999999999999994)
    assert r[2] == (0.0, -0.49999999999999994, 0.8660254037844387)


# **************************************************************************************


def test_get_rotation_matrix_about_x_90_degrees():
    # A 90 degree frame rotation carries the frame's y axis onto the old z axis and its
    # z axis onto the old negative y axis:
    r = get_rotation_matrix_about_x(90.0)
    assert r[0] == (1.0, 0.0, 0.0)
    assert isclose(r[1][1], 0.0, abs_tol=1e-15)
    assert r[1][2] == 1.0
    assert r[2][1] == -1.0
    assert isclose(r[2][2], 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_x_180_degrees():
    r = get_rotation_matrix_about_x(180.0)
    assert r[0] == (1.0, 0.0, 0.0)
    assert r[1][1] == -1.0
    assert isclose(r[1][2], 0.0, abs_tol=1e-15)
    assert isclose(r[2][1], 0.0, abs_tol=1e-15)
    assert r[2][2] == -1.0


# **************************************************************************************


def test_get_rotation_matrix_about_x_360_degrees_is_identity():
    r = get_rotation_matrix_about_x(360.0)
    for i in range(3):
        for j in range(3):
            assert isclose(r[i][j], 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_x_negative_angle_is_the_transpose():
    # Rotating back through the negative angle gives the inverse, which for a rotation
    # is the transpose:
    r = get_rotation_matrix_about_x(37.5)
    t = get_rotation_matrix_about_x(-37.5)
    for i in range(3):
        for j in range(3):
            assert t[i][j] == r[j][i]


# **************************************************************************************


def test_get_rotation_matrix_about_x_leaves_the_x_axis_fixed():
    for angle in (-120.0, -1.0, 12.5, 45.0, 210.0):
        assert get_rotation_matrix_about_x(angle)[0] == (1.0, 0.0, 0.0)


# **************************************************************************************


def test_get_rotation_matrix_about_x_rows_are_orthonormal():
    r = get_rotation_matrix_about_x(63.4)
    for i in range(3):
        for j in range(3):
            dot = sum(r[i][k] * r[j][k] for k in range(3))
            assert isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_x_has_unit_determinant():
    r = get_rotation_matrix_about_x(-77.0)
    determinant = (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )
    assert isclose(determinant, 1.0, rel_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_x_returns_three_by_three_floats():
    r = get_rotation_matrix_about_x(12.0)
    assert isinstance(r, tuple)
    assert len(r) == 3
    for row in r:
        assert isinstance(row, tuple)
        assert len(row) == 3
        assert all(isinstance(component, float) for component in row)


# **************************************************************************************


def test_get_rotation_matrix_about_y_zero_angle_is_identity():
    assert get_rotation_matrix_about_y(0.0) == (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


# **************************************************************************************


def test_get_rotation_matrix_about_y_30_degrees():
    r = get_rotation_matrix_about_y(30.0)
    assert r[0] == (0.8660254037844387, 0.0, -0.49999999999999994)
    assert r[1] == (0.0, 1.0, 0.0)
    assert r[2] == (0.49999999999999994, 0.0, 0.8660254037844387)


# **************************************************************************************


def test_get_rotation_matrix_about_y_90_degrees():
    # A 90 degree frame rotation carries the frame's z axis onto the old x axis and its
    # x axis onto the old negative z axis:
    r = get_rotation_matrix_about_y(90.0)
    assert isclose(r[0][0], 0.0, abs_tol=1e-15)
    assert r[0][2] == -1.0
    assert r[1] == (0.0, 1.0, 0.0)
    assert r[2][0] == 1.0
    assert isclose(r[2][2], 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_y_180_degrees():
    r = get_rotation_matrix_about_y(180.0)
    assert r[0][0] == -1.0
    assert isclose(r[0][2], 0.0, abs_tol=1e-15)
    assert r[1] == (0.0, 1.0, 0.0)
    assert isclose(r[2][0], 0.0, abs_tol=1e-15)
    assert r[2][2] == -1.0


# **************************************************************************************


def test_get_rotation_matrix_about_y_360_degrees_is_identity():
    r = get_rotation_matrix_about_y(360.0)
    for i in range(3):
        for j in range(3):
            assert isclose(r[i][j], 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_y_negative_angle_is_the_transpose():
    # Rotating back through the negative angle gives the inverse, which for a rotation
    # is the transpose:
    r = get_rotation_matrix_about_y(37.5)
    t = get_rotation_matrix_about_y(-37.5)
    for i in range(3):
        for j in range(3):
            assert t[i][j] == r[j][i]


# **************************************************************************************


def test_get_rotation_matrix_about_y_leaves_the_y_axis_fixed():
    for angle in (-120.0, -1.0, 12.5, 45.0, 210.0):
        assert get_rotation_matrix_about_y(angle)[1] == (0.0, 1.0, 0.0)


# **************************************************************************************


def test_get_rotation_matrix_about_y_rows_are_orthonormal():
    r = get_rotation_matrix_about_y(63.4)
    for i in range(3):
        for j in range(3):
            dot = sum(r[i][k] * r[j][k] for k in range(3))
            assert isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_y_has_unit_determinant():
    r = get_rotation_matrix_about_y(-77.0)
    determinant = (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )
    assert isclose(determinant, 1.0, rel_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_y_returns_three_by_three_floats():
    r = get_rotation_matrix_about_y(12.0)
    assert isinstance(r, tuple)
    assert len(r) == 3
    for row in r:
        assert isinstance(row, tuple)
        assert len(row) == 3
        assert all(isinstance(component, float) for component in row)


# **************************************************************************************


def test_get_rotation_matrix_about_z_zero_angle_is_identity():
    assert get_rotation_matrix_about_z(0.0) == (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


# **************************************************************************************


def test_get_rotation_matrix_about_z_30_degrees():
    r = get_rotation_matrix_about_z(30.0)
    assert r[0] == (0.8660254037844387, 0.49999999999999994, 0.0)
    assert r[1] == (-0.49999999999999994, 0.8660254037844387, 0.0)
    assert r[2] == (0.0, 0.0, 1.0)


# **************************************************************************************


def test_get_rotation_matrix_about_z_90_degrees():
    # A 90 degree frame rotation carries the frame's x axis onto the old y axis and its
    # y axis onto the old negative x axis:
    r = get_rotation_matrix_about_z(90.0)
    assert isclose(r[0][0], 0.0, abs_tol=1e-15)
    assert r[0][1] == 1.0
    assert r[1][0] == -1.0
    assert isclose(r[1][1], 0.0, abs_tol=1e-15)
    assert r[2] == (0.0, 0.0, 1.0)


# **************************************************************************************


def test_get_rotation_matrix_about_z_180_degrees():
    r = get_rotation_matrix_about_z(180.0)
    assert r[0][0] == -1.0
    assert isclose(r[0][1], 0.0, abs_tol=1e-15)
    assert isclose(r[1][0], 0.0, abs_tol=1e-15)
    assert r[1][1] == -1.0
    assert r[2] == (0.0, 0.0, 1.0)


# **************************************************************************************


def test_get_rotation_matrix_about_z_360_degrees_is_identity():
    r = get_rotation_matrix_about_z(360.0)
    for i in range(3):
        for j in range(3):
            assert isclose(r[i][j], 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_z_negative_angle_is_the_transpose():
    # Rotating back through the negative angle gives the inverse, which for a rotation
    # is the transpose:
    r = get_rotation_matrix_about_z(37.5)
    t = get_rotation_matrix_about_z(-37.5)
    for i in range(3):
        for j in range(3):
            assert t[i][j] == r[j][i]


# **************************************************************************************


def test_get_rotation_matrix_about_z_leaves_the_z_axis_fixed():
    for angle in (-120.0, -1.0, 12.5, 45.0, 210.0):
        assert get_rotation_matrix_about_z(angle)[2] == (0.0, 0.0, 1.0)


# **************************************************************************************


def test_get_rotation_matrix_about_z_rows_are_orthonormal():
    r = get_rotation_matrix_about_z(63.4)
    for i in range(3):
        for j in range(3):
            dot = sum(r[i][k] * r[j][k] for k in range(3))
            assert isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_z_has_unit_determinant():
    r = get_rotation_matrix_about_z(-77.0)
    determinant = (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )
    assert isclose(determinant, 1.0, rel_tol=1e-15)


# **************************************************************************************


def test_get_rotation_matrix_about_z_returns_three_by_three_floats():
    r = get_rotation_matrix_about_z(12.0)
    assert isinstance(r, tuple)
    assert len(r) == 3
    for row in r:
        assert isinstance(row, tuple)
        assert len(row) == 3
        assert all(isinstance(component, float) for component in row)


# **************************************************************************************
