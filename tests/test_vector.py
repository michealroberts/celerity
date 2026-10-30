# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import isclose

from src.celerity.common import EquatorialCoordinate
from src.celerity.vector import (
    convert_equatorial_to_vector,
    convert_vector_to_equatorial,
)

# **************************************************************************************

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

# **************************************************************************************

canopus: EquatorialCoordinate = {"ra": 95.9879496, "dec": -52.6956994}

# **************************************************************************************


def test_convert_equatorial_to_vector_betelgeuse():
    x, y, z = convert_equatorial_to_vector(betelgeuse)
    assert x == 0.02088950955632836
    assert y == 0.9914352296144991
    assert z == 0.1289178570630983


# **************************************************************************************


def test_convert_equatorial_to_vector_canopus():
    # A southern target has a negative z component:
    x, y, z = convert_equatorial_to_vector(canopus)
    assert x == -0.0632225105710946
    assert y == 0.6027414218001659
    assert z == -0.7954279933491166


# **************************************************************************************


def test_convert_equatorial_to_vector_is_unit_length():
    for target in (betelgeuse, canopus, {"ra": 360.0, "dec": 7.4070639}):
        x, y, z = convert_equatorial_to_vector(target)
        assert isclose(x**2 + y**2 + z**2, 1.0, rel_tol=1e-12)


# **************************************************************************************


def test_convert_equatorial_to_vector_vernal_equinox():
    # The origin of right ascension on the equator lies along the x axis:
    assert convert_equatorial_to_vector({"ra": 0.0, "dec": 0.0}) == (1.0, 0.0, 0.0)


# **************************************************************************************


def test_convert_equatorial_to_vector_right_ascension_90_degrees():
    # Six hours of right ascension on the equator lies along the y axis:
    x, y, z = convert_equatorial_to_vector({"ra": 90.0, "dec": 0.0})
    assert isclose(x, 0.0, abs_tol=1e-15)
    assert y == 1.0
    assert z == 0.0


# **************************************************************************************


def test_convert_equatorial_to_vector_right_ascension_180_degrees():
    # Twelve hours of right ascension on the equator lies along the negative x axis:
    x, y, z = convert_equatorial_to_vector({"ra": 180.0, "dec": 0.0})
    assert x == -1.0
    assert isclose(y, 0.0, abs_tol=1e-15)
    assert z == 0.0


# **************************************************************************************


def test_convert_equatorial_to_vector_north_celestial_pole():
    x, y, z = convert_equatorial_to_vector({"ra": 0.0, "dec": 90.0})
    assert isclose(x, 0.0, abs_tol=1e-15)
    assert y == 0.0
    assert z == 1.0


# **************************************************************************************


def test_convert_equatorial_to_vector_south_celestial_pole():
    x, y, z = convert_equatorial_to_vector({"ra": 0.0, "dec": -90.0})
    assert isclose(x, 0.0, abs_tol=1e-15)
    assert y == 0.0
    assert z == -1.0


# **************************************************************************************


def test_convert_equatorial_to_vector_right_ascension_wraps():
    # A right ascension of 360 degrees is the same direction as 0 degrees:
    a = convert_equatorial_to_vector({"ra": 360.0, "dec": betelgeuse["dec"]})
    b = convert_equatorial_to_vector({"ra": 0.0, "dec": betelgeuse["dec"]})
    for i in range(3):
        assert isclose(a[i], b[i], abs_tol=1e-15)

    # A negative right ascension is the same direction as its positive equivalent:
    a = convert_equatorial_to_vector({"ra": -90.0, "dec": 0.0})
    b = convert_equatorial_to_vector({"ra": 270.0, "dec": 0.0})
    for i in range(3):
        assert isclose(a[i], b[i], abs_tol=1e-15)


# **************************************************************************************


def test_convert_equatorial_to_vector_returns_three_floats():
    vector = convert_equatorial_to_vector(betelgeuse)
    assert isinstance(vector, tuple)
    assert len(vector) == 3
    assert all(isinstance(component, float) for component in vector)


# **************************************************************************************


def test_convert_vector_to_equatorial_betelgeuse():
    # The conversion inverts convert_equatorial_to_vector to floating point precision:
    target = convert_vector_to_equatorial(convert_equatorial_to_vector(betelgeuse))
    assert target["ra"] == 88.7929583
    assert isclose(target["dec"], 7.4070639, rel_tol=1e-12)


# **************************************************************************************


def test_convert_vector_to_equatorial_canopus():
    # A southern target round trips with a negative declination:
    target = convert_vector_to_equatorial(convert_equatorial_to_vector(canopus))
    assert target["ra"] == 95.9879496
    assert target["dec"] == -52.6956994


# **************************************************************************************


def test_convert_vector_to_equatorial_x_axis():
    # The x axis is the origin of right ascension on the equator:
    assert convert_vector_to_equatorial((1.0, 0.0, 0.0)) == {"ra": 0.0, "dec": 0.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_y_axis():
    # The y axis is six hours of right ascension on the equator:
    assert convert_vector_to_equatorial((0.0, 1.0, 0.0)) == {"ra": 90.0, "dec": 0.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_negative_x_axis():
    # The negative x axis is twelve hours of right ascension on the equator:
    assert convert_vector_to_equatorial((-1.0, 0.0, 0.0)) == {"ra": 180.0, "dec": 0.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_negative_y_axis():
    # The negative y axis is eighteen hours of right ascension, reported as 270 degrees
    # rather than -90 degrees:
    assert convert_vector_to_equatorial((0.0, -1.0, 0.0)) == {"ra": 270.0, "dec": 0.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_north_celestial_pole():
    assert convert_vector_to_equatorial((0.0, 0.0, 1.0)) == {"ra": 0.0, "dec": 90.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_south_celestial_pole():
    assert convert_vector_to_equatorial((0.0, 0.0, -1.0)) == {"ra": 0.0, "dec": -90.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_non_unit_vector():
    # The vector need not be of unit length:
    assert convert_vector_to_equatorial((2.0, -2.0, 0.0)) == {"ra": 315.0, "dec": 0.0}
    assert convert_vector_to_equatorial((1.0, 1.0, 2**0.5)) == {"ra": 45.0, "dec": 45.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_is_independent_of_scale():
    x, y, z = convert_equatorial_to_vector(betelgeuse)
    target = convert_vector_to_equatorial((3.0 * x, 3.0 * y, 3.0 * z))
    assert target["ra"] == 88.7929583
    assert isclose(target["dec"], 7.4070639, rel_tol=1e-12)


# **************************************************************************************


def test_convert_vector_to_equatorial_right_ascension_range():
    # The right ascension is always reported in the range [0, 360):
    for vector in (
        (1.0, -1.0, 0.0),
        (-1.0, -1.0, 0.0),
        (-1.0, 1.0, 0.0),
        (0.0, -1.0, 1.0),
    ):
        target = convert_vector_to_equatorial(vector)
        assert 0.0 <= target["ra"] < 360.0


# **************************************************************************************


def test_convert_vector_to_equatorial_zero_vector():
    # A zero vector has no direction and maps to the origin of both angles:
    assert convert_vector_to_equatorial((0.0, 0.0, 0.0)) == {"ra": 0.0, "dec": 0.0}


# **************************************************************************************


def test_convert_vector_to_equatorial_returns_equatorial_coordinate():
    target = convert_vector_to_equatorial((1.0, 1.0, 1.0))
    assert isinstance(target, dict)
    assert set(target.keys()) == {"ra", "dec"}
    assert isinstance(target["ra"], float)
    assert isinstance(target["dec"], float)


# **************************************************************************************
