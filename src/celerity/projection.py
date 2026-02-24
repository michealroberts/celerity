# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import cos, radians, sin, tan

from .common import CartesianCoordinate, GeographicPole, PolarCoordinate, SphericalCoordinate

# **************************************************************************************


def project_spherical_to_polar(
    target: SphericalCoordinate,
    pole: GeographicPole = GeographicPole.NORTH,
) -> PolarCoordinate:
    """
    Projects spherical sky coordinates into a polar representation centred on
    the specified pole.

    Convention: the radial distance r is the angular distance from the chosen
    pole, ranging from 0° at the centred pole to 180° at the opposite pole.
    The polar angle θ corresponds to the longitude measured eastward, normalised
    to [0°, 360°).

    For the North Pole (default): r = 90° − φ (co-latitude from north).
    For the South Pole: r = 90° + φ (co-latitude from south).

    The latitude (φ) is clamped to [-90°, 90°] and the longitude (θ) is
    normalised to [0°, 360°) before conversion. At the poles, where the polar
    angle is geometrically undefined, it is returned as 0.0° by convention.

    :param target: A SphericalCoordinate with φ (latitude, in degrees, clamped
        to [-90°, 90°]) and θ (longitude, in degrees, normalised to [0°, 360°)).
    :param pole: The pole to centre the projection on (default: GeographicPole.NORTH).
    :return: A PolarCoordinate with r (co-latitude from the chosen pole, in degrees)
        and θ (longitude, in degrees, normalised to [0°, 360°)).
    """
    # Clamp the latitude φ to the valid range [-90°, 90°]:
    latitude = max(-90.0, min(90.0, target["φ"]))

    # Normalise the longitude θ to [0°, 360°):
    theta = target["θ"] % 360.0

    # The radial distance is the angular distance from the chosen pole:
    r = 90.0 - latitude if pole == GeographicPole.NORTH else 90.0 + latitude

    # At the poles the polar angle is geometrically undefined; return 0.0 by convention:
    if r == 0.0 or r == 180.0:
        return PolarCoordinate(
            {
                "r": r,
                "θ": 0.0,
            }
        )

    return PolarCoordinate(
        {
            "r": r,
            "θ": theta,
        }
    )


# **************************************************************************************


def project_spherical_to_polar_stereographic(
    target: SphericalCoordinate,
    pole: GeographicPole = GeographicPole.NORTH,
) -> CartesianCoordinate:
    """
    Projects spherical sky coordinates into a polar stereographic Cartesian
    representation centred on the specified pole.

    This is the standard polar stereographic projection onto a unit sphere:
    the sphere is projected from the opposite pole onto the tangent plane at the
    chosen pole. The Cartesian radius is R = 2·tan(c/2), where c is the angular
    distance from the chosen pole. The x-axis points toward θ = 0° and the
    y-axis points toward θ = 90°. Coordinates are dimensionless (unit-sphere),
    so they can be mapped to any canvas by multiplying x and y by a scale factor
    (e.g. scale = canvas_half_size / R_max).

    The latitude (φ) is clamped to [-90°, 90°] and the longitude (θ) is
    normalised to [0°, 360°) before conversion. At the chosen pole (c = 0)
    both x and y are 0. The opposite pole (c = 180°) lies at infinity and is
    returned as (float("inf"), float("inf")).

    :param target: A SphericalCoordinate with φ (latitude, in degrees, clamped
        to [-90°, 90°]) and θ (longitude, in degrees, normalised to [0°, 360°)).
    :param pole: The pole to centre the projection on (default: GeographicPole.NORTH).
    :return: A CartesianCoordinate with dimensionless x and y on a unit sphere.
    """
    polar = project_spherical_to_polar(target, pole)

    # The opposite pole (angular distance = 180°) projects to infinity:
    if polar["r"] == 180.0:
        return CartesianCoordinate({"x": float("inf"), "y": float("inf")})

    # True polar stereographic projection onto a unit sphere:
    # R = 2 * tan(c/2), where c is the angular distance from the chosen pole.
    R = 2.0 * tan(radians(polar["r"]) / 2.0)

    return CartesianCoordinate(
        {
            "x": R * cos(radians(polar["θ"])),
            "y": R * sin(radians(polar["θ"])),
        }
    )


# **************************************************************************************
