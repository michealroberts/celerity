# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import isclose

from src.celerity.common import SphericalCoordinate
from src.celerity.projection import project_spherical_to_polar

# **************************************************************************************


def test_project_spherical_to_polar_equator_prime_meridian():
    # At the equator and prime meridian:
    target: SphericalCoordinate = {"longitude": 0.0, "latitude": 0.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 90.0)
    assert isclose(result["polar_angle"], 0.0)


# **************************************************************************************


def test_project_spherical_to_polar_north_pole():
    # At the north pole the radial distance is 0° and the polar angle is undefined (0°):
    target: SphericalCoordinate = {"longitude": 45.0, "latitude": 90.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 0.0)
    assert isclose(result["polar_angle"], 0.0)


# **************************************************************************************


def test_project_spherical_to_polar_south_pole():
    # At the south pole the radial distance is 180° and the polar angle is undefined (0°):
    target: SphericalCoordinate = {"longitude": 120.0, "latitude": -90.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 180.0)
    assert isclose(result["polar_angle"], 0.0)


# **************************************************************************************


def test_project_spherical_to_polar_northern_hemisphere():
    # A point in the northern hemisphere:
    target: SphericalCoordinate = {"longitude": 90.0, "latitude": 45.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 45.0)
    assert isclose(result["polar_angle"], 90.0)


# **************************************************************************************


def test_project_spherical_to_polar_southern_hemisphere():
    # A point in the southern hemisphere:
    target: SphericalCoordinate = {"longitude": 270.0, "latitude": -45.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 135.0)
    assert isclose(result["polar_angle"], 270.0)


# **************************************************************************************


def test_project_spherical_to_polar_longitude_normalisation_positive():
    # Longitude beyond 360° should be normalised to [0°, 360°):
    target: SphericalCoordinate = {"longitude": 400.0, "latitude": 30.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 60.0)
    assert isclose(result["polar_angle"], 40.0)


# **************************************************************************************


def test_project_spherical_to_polar_longitude_normalisation_negative():
    # Negative longitude should be normalised to [0°, 360°):
    target: SphericalCoordinate = {"longitude": -90.0, "latitude": 30.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 60.0)
    assert isclose(result["polar_angle"], 270.0)


# **************************************************************************************


def test_project_spherical_to_polar_longitude_wrap_360():
    # Longitude of exactly 360° should normalise to 0°:
    target: SphericalCoordinate = {"longitude": 360.0, "latitude": 0.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 90.0)
    assert isclose(result["polar_angle"], 0.0)


# **************************************************************************************


def test_project_spherical_to_polar_latitude_clamping_high():
    # Latitude above 90° should be clamped to 90°:
    target: SphericalCoordinate = {"longitude": 0.0, "latitude": 100.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 0.0)
    assert isclose(result["polar_angle"], 0.0)


# **************************************************************************************


def test_project_spherical_to_polar_latitude_clamping_low():
    # Latitude below -90° should be clamped to -90°:
    target: SphericalCoordinate = {"longitude": 180.0, "latitude": -100.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 180.0)
    assert isclose(result["polar_angle"], 0.0)


# **************************************************************************************


def test_project_spherical_to_polar_near_north_pole():
    # A point very close to the north pole:
    target: SphericalCoordinate = {"longitude": 60.0, "latitude": 89.9}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 0.1, rel_tol=1e-9)
    assert isclose(result["polar_angle"], 60.0)


# **************************************************************************************


def test_project_spherical_to_polar_near_south_pole():
    # A point very close to the south pole:
    target: SphericalCoordinate = {"longitude": 200.0, "latitude": -89.9}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 179.9, rel_tol=1e-9)
    assert isclose(result["polar_angle"], 200.0)


# **************************************************************************************


def test_project_spherical_to_polar_180_longitude():
    # Longitude of 180° (anti-meridian):
    target: SphericalCoordinate = {"longitude": 180.0, "latitude": 60.0}
    result = project_spherical_to_polar(target)
    assert isclose(result["radial_distance"], 30.0)
    assert isclose(result["polar_angle"], 180.0)


# **************************************************************************************


def test_project_spherical_to_polar_returns_typed_dict_keys():
    # The return value must contain exactly the expected keys:
    target: SphericalCoordinate = {"longitude": 30.0, "latitude": 15.0}
    result = project_spherical_to_polar(target)
    assert "radial_distance" in result
    assert "polar_angle" in result


# **************************************************************************************
