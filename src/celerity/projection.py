# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from typing import TypedDict

# **************************************************************************************


class PolarProjection(TypedDict):
    """
    :property radial_distance: The angular distance from the North Pole (co-latitude),
        in degrees, in the range [0°, 180°].
    :property polar_angle: The polar angle, in degrees, normalised to [0°, 360°),
        corresponding to the longitude measured eastward.
    """

    radial_distance: float
    polar_angle: float


# **************************************************************************************


def project_spherical_to_polar(
    longitude: float,
    latitude: float,
) -> PolarProjection:
    """
    Projects spherical sky coordinates (longitude, latitude) into a polar
    representation centred on the North Pole.

    Convention: the pole is the North Pole (latitude = +90°). The radial
    distance is the angular distance from the North Pole (co-latitude), ranging
    from 0° at the North Pole to 180° at the South Pole. The polar angle
    corresponds to the longitude measured eastward, normalised to [0°, 360°).

    Latitude is clamped to [-90°, 90°] and longitude is normalised to [0°, 360°)
    before conversion. At the poles, where the polar angle is geometrically
    undefined, it is returned as 0.0° by convention.

    :param longitude: The longitude in degrees (e.g. right ascension or ecliptic
        longitude). Normalised to [0°, 360°).
    :param latitude: The latitude in degrees (e.g. declination or ecliptic
        latitude). Clamped to [-90°, 90°].
    :return: A PolarProjection with radial_distance (co-latitude, in degrees)
        and polar_angle (longitude, in degrees, normalised to [0°, 360°)).
    """

    # Clamp latitude to the valid range [-90°, 90°]:
    latitude = max(-90.0, min(90.0, latitude))

    # Normalise longitude to [0°, 360°):
    longitude = longitude % 360.0

    # The radial distance is the co-latitude (angular distance from the North Pole):
    radial_distance = 90.0 - latitude

    # At the poles the polar angle is geometrically undefined; return 0.0 by convention:
    if radial_distance == 0.0 or radial_distance == 180.0:
        return {"radial_distance": radial_distance, "polar_angle": 0.0}

    return {"radial_distance": radial_distance, "polar_angle": longitude}


# **************************************************************************************
