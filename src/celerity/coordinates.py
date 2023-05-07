from datetime import datetime
from math import acos, asin, cos, degrees, radians, sin

from .astrometry import get_hour_angle
from .common import EquatorialCoordinate, GeographicCoordinate, HorizontalCoordinate


def convert_equatorial_to_horizontal(
    date: datetime,
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
) -> HorizontalCoordinate:
    """
    Converts an equatorial coordinate to a horizontal coordinate.

    :param date: The datetime object to convert.
    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :return The horizontal coordinate of the observed object.
    """
    lat, lon = radians(observer["lat"]), observer["lon"]

    dec = radians(target["dec"])

    # Divide-by-zero errors can occur when we have cos(90), and sin(0)/sin(180) etc
    # cosine: multiples of π/2
    # sine: 0, and multiples of π.
    if cos(lat) == 0:
        return {"az": -1, "alt": -1}

    # Get the hour angle for the target:
    ha = radians(get_hour_angle(date, target["ra"], lon))

    alt = asin(sin(dec) * sin(lat) + cos(dec) * cos(lat) * cos(ha))

    az = acos((sin(dec) - sin(alt) * sin(lat)) / (cos(alt) * cos(lat)))

    return {
        "az": 360 - degrees(az) if sin(ha) > 0 else degrees(az),
        "alt": degrees(alt),
    }
