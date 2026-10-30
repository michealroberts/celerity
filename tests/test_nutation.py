# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from math import acos, degrees, isclose

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.matrix import apply_matrix
from src.celerity.nutation import (
    get_correction_to_equatorial_for_nutation,
    get_nutation_in_longitude,
    get_nutation_in_obliquity,
    get_nutation_matrix,
)
from src.celerity.vector import (
    convert_equatorial_to_vector,
    convert_vector_to_equatorial,
)

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# **************************************************************************************

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# **************************************************************************************

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

# **************************************************************************************

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

# **************************************************************************************

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}

# **************************************************************************************


def test_get_nutation_in_longitude():
    Δψ = get_nutation_in_longitude(date)
    assert Δψ == -0.004863947727194747


# **************************************************************************************


def test_get_nutation_in_obliquity():
    Δε = get_nutation_in_obliquity(date)
    assert Δε == 0.0007474263655767607


# **************************************************************************************


def test_get_correction_to_equatorial_for_nutation():
    t = get_correction_to_equatorial_for_nutation(date, betelgeuse)
    ra = t["ra"] + betelgeuse["ra"]
    dec = t["dec"] + betelgeuse["dec"]
    assert ra == 88.78824212603895
    assert dec == 7.407770327786887


# **************************************************************************************


def test_get_nutation_matrix_matches_erfa():
    N = get_nutation_matrix(date)

    # The reference matrix is ERFA num06a (pyerfa 2.0.1.5) for 2021-05-14 00:00:00 UTC;
    # the tolerance admits the difference between the IAU 2000B series used here and the
    # IAU 2000A series used by ERFA:
    expected = (
        (0.9999999963969325, 7.788573970243065e-05, 3.3763093340898604e-05),
        (-7.78852992675054e-05, 0.9999999968818413, -1.3045981501096194e-05),
        (-3.3764109331539275e-05, 1.304335180547414e-05, 0.999999999344928),
    )
    for i in range(3):
        for j in range(3):
            assert isclose(N[i][j], expected[i][j], abs_tol=5e-9)


# **************************************************************************************


def test_get_nutation_matrix_is_close_to_identity():
    N = get_nutation_matrix(date)
    for i in range(3):
        for j in range(3):
            assert isclose(N[i][j], 1.0 if i == j else 0.0, abs_tol=1e-4)


# **************************************************************************************


def test_get_nutation_matrix_rotation_angle_is_about_the_nutation_in_longitude():
    # The rotation angle is dominated by the nutation in longitude, which on this date
    # is about 17.5 arcseconds:
    N = get_nutation_matrix(date)
    angle = degrees(acos((N[0][0] + N[1][1] + N[2][2] - 1.0) / 2.0)) * 3600
    assert 16.0 < angle < 19.0


# **************************************************************************************


def test_get_nutation_matrix_rows_are_orthonormal():
    N = get_nutation_matrix(date)
    for i in range(3):
        for j in range(3):
            dot = sum(N[i][k] * N[j][k] for k in range(3))
            assert isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-15)


# **************************************************************************************


def test_get_nutation_matrix_has_unit_determinant():
    N = get_nutation_matrix(date)
    determinant = (
        N[0][0] * (N[1][1] * N[2][2] - N[1][2] * N[2][1])
        - N[0][1] * (N[1][0] * N[2][2] - N[1][2] * N[2][0])
        + N[0][2] * (N[1][0] * N[2][1] - N[1][1] * N[2][0])
    )
    assert isclose(determinant, 1.0, rel_tol=1e-15)


# **************************************************************************************


def test_get_nutation_matrix_agrees_with_the_correction():
    # Rotating the direction cosines of Betelgeuse through the matrix gives the same
    # nutated place as the correction to floating point precision:
    nutated = convert_vector_to_equatorial(
        apply_matrix(
            get_nutation_matrix(date), convert_equatorial_to_vector(betelgeuse)
        )
    )
    correction = get_correction_to_equatorial_for_nutation(date, betelgeuse)
    assert isclose(nutated["ra"], betelgeuse["ra"] + correction["ra"], abs_tol=1e-12)
    assert isclose(nutated["dec"], betelgeuse["dec"] + correction["dec"], abs_tol=1e-12)


# **************************************************************************************


def test_get_nutation_matrix_treats_naive_datetime_as_utc():
    assert get_nutation_matrix(
        datetime(2021, 5, 14, 0, 0, 0, 0)
    ) == get_nutation_matrix(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    )


# **************************************************************************************


def test_get_nutation_matrix_returns_three_by_three_floats():
    N = get_nutation_matrix(date)
    assert isinstance(N, tuple)
    assert len(N) == 3
    for row in N:
        assert isinstance(row, tuple)
        assert len(row) == 3
        assert all(isinstance(component, float) for component in row)


# **************************************************************************************


def test_get_correction_to_equatorial_for_nutation_wraps_right_ascension():
    # A target just below 360 degrees may nutate through 0 degrees, and the correction
    # must be the small step rather than a full turn:
    correction = get_correction_to_equatorial_for_nutation(
        date, {"ra": 359.999, "dec": 0.0}
    )
    assert -1.0 < correction["ra"] < 1.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_nutation_near_the_pole():
    # Close to the celestial pole the correction stays finite and the nutated
    # declination stays within range:
    target: EquatorialCoordinate = {"ra": 37.9, "dec": 89.99}
    correction = get_correction_to_equatorial_for_nutation(date, target)
    assert -180.0 <= correction["ra"] < 180.0
    assert -90.0 <= target["dec"] + correction["dec"] <= 90.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_nutation_shift_is_about_17_arcseconds():
    # On this date the nutation in longitude is about -17.5 arcseconds, so the shift of
    # a target on the ecliptic is of that size:
    target: EquatorialCoordinate = {"ra": 0.0, "dec": 0.0}
    correction = get_correction_to_equatorial_for_nutation(date, target)
    shift = (correction["ra"] ** 2 + correction["dec"] ** 2) ** 0.5 * 3600
    assert 15.0 < shift < 19.0


# **************************************************************************************
