# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from .common import PolarCoordinate, SphericalCoordinate

# **************************************************************************************


def project_spherical_to_polar(
    target: SphericalCoordinate,
) -> PolarCoordinate:
    """
    Projects spherical sky coordinates into a polar representation centred on
    the North Pole.

    Convention: the pole is the North Pole (φ = +90°). The radial distance r
    is the angular distance from the North Pole (co-latitude), ranging from 0°
    at the North Pole to 180° at the South Pole. The polar angle θ corresponds
    to the longitude (φ) measured eastward, normalised to [0°, 360°).

    The latitude (φ) is clamped to [-90°, 90°] and the longitude (θ) is
    normalised to [0°, 360°) before conversion. At the poles, where the polar
    angle is geometrically undefined, it is returned as 0.0° by convention.

    :param target: A SphericalCoordinate with φ (latitude, in degrees, clamped
        to [-90°, 90°]) and θ (longitude, in degrees, normalised to [0°, 360°)).
    :return: A PolarCoordinate with r (co-latitude, in degrees) and θ (longitude,
        in degrees, normalised to [0°, 360°)).
    """
    # Clamp the latitude φ to the valid range [-90°, 90°]:
    latitude = max(-90.0, min(90.0, target["φ"]))

    # Normalise the longitude θ to [0°, 360°):
    theta = target["θ"] % 360.0

    # The radial distance is the co-latitude (angular distance from the North Pole):
    r = 90.0 - latitude

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
