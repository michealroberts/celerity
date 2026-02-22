# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from .common import PolarCoordinate, SphericalCoordinate

# **************************************************************************************


def project_spherical_to_polar(target: SphericalCoordinate) -> PolarCoordinate:
    """
    Converts spherical sky coordinates into a polar-space representation.

    The convention used is:
    - The radial distance is the angular separation from the north celestial pole,
      measured in degrees (i.e., the co-latitude), ranging from 0° at the north
      pole to 180° at the south pole.
    - The polar angle is the longitude measured eastward from the reference
      direction, normalised to the range [0°, 360°).
    - Latitude is clamped to the valid range [-90°, 90°].
    - At the poles (radial distance = 0° or 180°) the polar angle is
      undefined and is returned as 0°.

    :param target: The spherical coordinate with longitude and latitude in degrees.
    :return: The corresponding polar coordinate with radial_distance and polar_angle
             in degrees.
    """
    # Clamp latitude to the valid range of [-90, 90] degrees:
    latitude = max(-90.0, min(90.0, target["latitude"]))

    # Normalise longitude to [0°, 360°):
    longitude = target["longitude"] % 360.0

    # The radial distance is the co-latitude (angular distance from the north pole):
    radial_distance = 90.0 - latitude

    # At the poles the polar angle is geometrically undefined; return 0°:
    if radial_distance == 0.0 or radial_distance == 180.0:
        return PolarCoordinate({"radial_distance": radial_distance, "polar_angle": 0.0})

    return PolarCoordinate(
        {"radial_distance": radial_distance, "polar_angle": longitude}
    )


# **************************************************************************************
