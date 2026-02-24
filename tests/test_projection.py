# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from src.celerity.common import SphericalCoordinate
from src.celerity.projection import project_spherical_to_polar

# **************************************************************************************


def test_project_spherical_to_polar_equator_zero_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 0.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_equator_90_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 90.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 90.0


# **************************************************************************************


def test_project_spherical_to_polar_equator_180_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 180.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 180.0


# **************************************************************************************


def test_project_spherical_to_polar_equator_270_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 270.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 270.0


# **************************************************************************************


def test_project_spherical_to_polar_northern_hemisphere():
    target: SphericalCoordinate = {"φ": 45.0, "θ": 90.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 45.0
    assert result["θ"] == 90.0


# **************************************************************************************


def test_project_spherical_to_polar_southern_hemisphere():
    target: SphericalCoordinate = {"φ": -45.0, "θ": 180.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 135.0
    assert result["θ"] == 180.0


# **************************************************************************************


def test_project_spherical_to_polar_north_pole():
    target: SphericalCoordinate = {"φ": 90.0, "θ": 42.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 0.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_south_pole():
    target: SphericalCoordinate = {"φ": -90.0, "θ": 42.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 180.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_longitude_normalisation_above_360():
    # 450° should normalise to 90°
    target: SphericalCoordinate = {"φ": 0.0, "θ": 450.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 90.0


# **************************************************************************************


def test_project_spherical_to_polar_longitude_normalisation_negative():
    # -90° should normalise to 270°
    target: SphericalCoordinate = {"φ": 0.0, "θ": -90.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 270.0


# **************************************************************************************


def test_project_spherical_to_polar_longitude_wrap_360():
    # 360° should normalise to 0°
    target: SphericalCoordinate = {"φ": 0.0, "θ": 360.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 90.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_latitude_clamp_above_90():
    # Latitude above +90° should be clamped to +90°
    target: SphericalCoordinate = {"φ": 95.0, "θ": 0.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 0.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_latitude_clamp_below_minus_90():
    # Latitude below -90° should be clamped to -90°
    target: SphericalCoordinate = {"φ": -95.0, "θ": 0.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 180.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_near_north_pole():
    target: SphericalCoordinate = {"φ": 89.0, "θ": 45.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 1.0
    assert result["θ"] == 45.0


# **************************************************************************************


def test_project_spherical_to_polar_near_south_pole():
    target: SphericalCoordinate = {"φ": -89.0, "θ": 135.0}
    result = project_spherical_to_polar(target)
    assert result["r"] == 179.0
    assert result["θ"] == 135.0


# **************************************************************************************


def test_project_spherical_to_polar_radial_distance_range():
    # Radial distance should always be in [0°, 180°]
    for lat in range(-90, 91, 15):
        target: SphericalCoordinate = {"φ": float(lat), "θ": 0.0}
        result = project_spherical_to_polar(target)
        assert 0.0 <= result["r"] <= 180.0


# **************************************************************************************


def test_project_spherical_to_polar_polar_angle_range():
    # Polar angle should always be in [0°, 360°)
    for lon in range(-360, 721, 45):
        target: SphericalCoordinate = {"φ": 30.0, "θ": float(lon)}
        result = project_spherical_to_polar(target)
        assert 0.0 <= result["θ"] < 360.0


# **************************************************************************************
