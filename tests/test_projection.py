# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from math import isclose, radians

from src.celerity.common import GeographicPole, SphericalCoordinate
from src.celerity.projection import (
    project_spherical_to_polar,
    project_spherical_to_polar_stereographic,
)

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


def test_project_spherical_to_polar_stereographic_equator_zero_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 0.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 2.0, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_equator_90_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 90.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], 2.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_equator_180_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 180.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], -2.0, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_equator_270_longitude():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 270.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], -2.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_northern_hemisphere():
    target: SphericalCoordinate = {"φ": 45.0, "θ": 90.0}
    result = project_spherical_to_polar_stereographic(target)
    # r = 45°, R = 2*tan(22.5°) = 2*(√2−1)
    from math import tan
    R = 2.0 * tan(radians(45.0) / 2.0)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], R, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_southern_hemisphere():
    target: SphericalCoordinate = {"φ": -45.0, "θ": 180.0}
    result = project_spherical_to_polar_stereographic(target)
    # r = 135°, R = 2*tan(67.5°) = 2*(√2+1)
    from math import tan
    R = 2.0 * tan(radians(135.0) / 2.0)
    assert isclose(result["x"], -R, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_north_pole():
    target: SphericalCoordinate = {"φ": 90.0, "θ": 42.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_south_pole():
    # The south pole is at infinity in a north-pole-centred stereographic projection
    from math import isinf
    target: SphericalCoordinate = {"φ": -90.0, "θ": 42.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isinf(result["x"])
    assert isinf(result["y"])


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_longitude_normalisation_above_360():
    # 450° should normalise to 90°
    target: SphericalCoordinate = {"φ": 0.0, "θ": 450.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], 2.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_longitude_normalisation_negative():
    # -90° should normalise to 270°
    target: SphericalCoordinate = {"φ": 0.0, "θ": -90.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], -2.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_longitude_wrap_360():
    # 360° should normalise to 0°
    target: SphericalCoordinate = {"φ": 0.0, "θ": 360.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 2.0, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_latitude_clamp_above_90():
    # Latitude above +90° should be clamped to +90°
    target: SphericalCoordinate = {"φ": 95.0, "θ": 0.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_latitude_clamp_below_minus_90():
    # Latitude below -90° should be clamped to -90° → projects to infinity
    from math import isinf
    target: SphericalCoordinate = {"φ": -95.0, "θ": 0.0}
    result = project_spherical_to_polar_stereographic(target)
    assert isinf(result["x"])
    assert isinf(result["y"])


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_near_north_pole():
    target: SphericalCoordinate = {"φ": 89.0, "θ": 45.0}
    result = project_spherical_to_polar_stereographic(target)
    from math import cos, radians, sin, tan

    R = 2.0 * tan(radians(1.0) / 2.0)
    assert isclose(result["x"], R * cos(radians(45.0)), abs_tol=1e-9)
    assert isclose(result["y"], R * sin(radians(45.0)), abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_near_south_pole():
    target: SphericalCoordinate = {"φ": -89.0, "θ": 135.0}
    result = project_spherical_to_polar_stereographic(target)
    from math import cos, radians, sin, tan

    R = 2.0 * tan(radians(179.0) / 2.0)
    assert isclose(result["x"], R * cos(radians(135.0)), abs_tol=1e-9)
    assert isclose(result["y"], R * sin(radians(135.0)), abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_cartesian_distance_equals_r():
    # The Euclidean distance from origin should equal the stereographic radius R = 2·tan(c/2)
    from math import isinf, sqrt, tan

    for lat in range(-90, 91, 15):
        for lon in range(0, 360, 45):
            target: SphericalCoordinate = {"φ": float(lat), "θ": float(lon)}
            polar = project_spherical_to_polar(target)
            cart = project_spherical_to_polar_stereographic(target)
            if polar["r"] == 180.0:
                # Opposite pole projects to infinity
                assert isinf(cart["x"]) and isinf(cart["y"])
            else:
                R = 2.0 * tan(radians(polar["r"]) / 2.0)
                distance = sqrt(cart["x"] ** 2 + cart["y"] ** 2)
                assert isclose(distance, R, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_south_pole_centered_south_pole():
    # South pole is r=0 when centred on south pole
    target: SphericalCoordinate = {"φ": -90.0, "θ": 42.0}
    result = project_spherical_to_polar(target, GeographicPole.SOUTH)
    assert result["r"] == 0.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_south_pole_centered_north_pole():
    # North pole is r=180 when centred on south pole
    target: SphericalCoordinate = {"φ": 90.0, "θ": 42.0}
    result = project_spherical_to_polar(target, GeographicPole.SOUTH)
    assert result["r"] == 180.0
    assert result["θ"] == 0.0


# **************************************************************************************


def test_project_spherical_to_polar_south_pole_centered_equator():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 90.0}
    result = project_spherical_to_polar(target, GeographicPole.SOUTH)
    assert result["r"] == 90.0
    assert result["θ"] == 90.0


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_south_pole_centered_south_pole():
    # South pole projects to origin when centred on south pole
    target: SphericalCoordinate = {"φ": -90.0, "θ": 42.0}
    result = project_spherical_to_polar_stereographic(target, GeographicPole.SOUTH)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], 0.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_south_pole_centered_equator_90():
    target: SphericalCoordinate = {"φ": 0.0, "θ": 90.0}
    result = project_spherical_to_polar_stereographic(target, GeographicPole.SOUTH)
    assert isclose(result["x"], 0.0, abs_tol=1e-9)
    assert isclose(result["y"], 2.0, abs_tol=1e-9)


# **************************************************************************************


def test_project_spherical_to_polar_stereographic_south_pole_centered_distance_equals_r():
    # Euclidean distance equals stereographic radius R = 2·tan(c/2) for south-pole-centred projection
    from math import isinf, sqrt, tan

    for lat in range(-90, 91, 15):
        for lon in range(0, 360, 45):
            target: SphericalCoordinate = {"φ": float(lat), "θ": float(lon)}
            polar = project_spherical_to_polar(target, GeographicPole.SOUTH)
            cart = project_spherical_to_polar_stereographic(target, GeographicPole.SOUTH)
            if polar["r"] == 180.0:
                assert isinf(cart["x"]) and isinf(cart["y"])
            else:
                R = 2.0 * tan(radians(polar["r"]) / 2.0)
                distance = sqrt(cart["x"] ** 2 + cart["y"] ** 2)
                assert isclose(distance, R, abs_tol=1e-9)


# **************************************************************************************
