from datetime import datetime
from math import acos, degrees, isclose

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.precession import (
    FRAME_BIAS_IN_LONGITUDE,
    FRAME_BIAS_IN_OBLIQUITY,
    FRAME_BIAS_IN_RIGHT_ASCENSION,
    OBLIQUITY_AT_J2000,
    get_correction_to_equatorial_for_precession_of_equinoxes,
    get_frame_bias_matrix,
)

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}


def test_get_correction_to_equatorial_for_precession_of_equinoxes():
    t = get_correction_to_equatorial_for_precession_of_equinoxes(date, betelgeuse)
    ra = t["ra"] + betelgeuse["ra"]
    dec = t["dec"] + betelgeuse["dec"]
    assert ra == 89.08215441916796
    assert dec == 7.4092677155992055


# **************************************************************************************


def test_frame_bias_constants():
    assert FRAME_BIAS_IN_LONGITUDE == -0.041775
    assert FRAME_BIAS_IN_OBLIQUITY == -0.0068192
    assert FRAME_BIAS_IN_RIGHT_ASCENSION == -0.0146
    assert OBLIQUITY_AT_J2000 == 84381.448


# **************************************************************************************


def test_get_frame_bias_matrix_matches_erfa():
    B = get_frame_bias_matrix()

    # The reference matrix is the rb matrix of ERFA bp06 (pyerfa 2.0.1.5):
    expected = (
        (0.9999999999999941, -7.078368960971559e-08, 8.056213977613186e-08),
        (7.078368694637678e-08, 0.9999999999999969, 3.305943738009795e-08),
        (-8.056214211620057e-08, -3.305943169468331e-08, 0.9999999999999962),
    )
    for i in range(3):
        for j in range(3):
            assert isclose(B[i][j], expected[i][j], abs_tol=1e-12)


# **************************************************************************************


def test_get_frame_bias_matrix_is_close_to_identity():
    B = get_frame_bias_matrix()
    for i in range(3):
        for j in range(3):
            assert isclose(B[i][j], 1.0 if i == j else 0.0, abs_tol=1e-7)


# **************************************************************************************


def test_get_frame_bias_matrix_rotation_is_about_23_milliarcseconds():
    B = get_frame_bias_matrix()
    # The rotation angle follows from the trace of a rotation matrix:
    angle = degrees(acos((B[0][0] + B[1][1] + B[2][2] - 1.0) / 2.0)) * 3600000
    assert 22.0 < angle < 24.0


# **************************************************************************************


def test_get_frame_bias_matrix_rows_are_orthonormal():
    B = get_frame_bias_matrix()
    for i in range(3):
        for j in range(3):
            dot = sum(B[i][k] * B[j][k] for k in range(3))
            assert isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_frame_bias_matrix_has_unit_determinant():
    B = get_frame_bias_matrix()
    determinant = (
        B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1])
        - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
        + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0])
    )
    assert isclose(determinant, 1.0, rel_tol=1e-15)


# **************************************************************************************


def test_get_frame_bias_matrix_is_constant():
    assert get_frame_bias_matrix() == get_frame_bias_matrix()


# **************************************************************************************


def test_get_frame_bias_matrix_returns_three_by_three_floats():
    B = get_frame_bias_matrix()
    assert isinstance(B, tuple)
    assert len(B) == 3
    for row in B:
        assert isinstance(row, tuple)
        assert len(row) == 3
        assert all(isinstance(component, float) for component in row)


# **************************************************************************************
