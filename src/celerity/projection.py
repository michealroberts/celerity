# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import cos, radians, sin

from .common import CartesianCoordinate, PolarCoordinate, SphericalCoordinate

# **************************************************************************************


def project_spherical_to_polar(target: SphericalCoordinate) -> PolarCoordinate:
    """
    Converts spherical sky coordinates into a polar-space representation.

    The convention used is:
    - The radial distance is the angular separation from the north celestial pole,
      measured in degrees (i.e., the co-latitude), ranging from 0° at the north
      pole to 180° at the south pole.
    - The polar angle is φ (longitude) measured eastward from the reference
      direction, normalised to the range [0°, 360°).
    - θ (latitude) is clamped to the valid range [-90°, 90°].
    - At the poles (radial distance = 0° or 180°) the polar angle is
      undefined and is returned as 0°.

    :param target: The spherical coordinate with φ (longitude) and θ (latitude)
                   in degrees.
    :return: The corresponding polar coordinate with radial_distance and polar_angle
             in degrees.
    """
    # Clamp θ (latitude) to the valid range of [-90, 90] degrees:
    θ = max(-90.0, min(90.0, target["θ"]))

    # Normalise φ (longitude) to [0°, 360°):
    φ = target["φ"] % 360.0

    # The radial distance is the co-latitude (angular distance from the north pole):
    radial_distance = 90.0 - θ

    # At the poles the polar angle is geometrically undefined; return 0°:
    if radial_distance == 0.0 or radial_distance == 180.0:
        return PolarCoordinate({"radial_distance": radial_distance, "polar_angle": 0.0})

    return PolarCoordinate(
        {"radial_distance": radial_distance, "polar_angle": φ}
    )


# **************************************************************************************


def project_polar_to_cartesian(target: PolarCoordinate) -> CartesianCoordinate:
    """
    Converts a polar coordinate into a Cartesian 2D representation suitable for
    use in a polar plot.

    The convention used is:
    - The x-axis points in the direction of polar_angle = 0°.
    - The y-axis points in the direction of polar_angle = 90°.
    - The polar_angle is measured counter-clockwise from the positive x-axis.
    - The radial_distance is the distance from the origin (pole).

    :param target: The polar coordinate with radial_distance and polar_angle in degrees.
    :return: The corresponding Cartesian coordinate with x and y components.
    """
    r = target["radial_distance"]
    θ = radians(target["polar_angle"])

    return CartesianCoordinate({"x": r * cos(θ), "y": r * sin(θ)})


# **************************************************************************************
