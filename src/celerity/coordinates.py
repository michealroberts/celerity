import math
from datetime import datetime

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
    lat, lon = observer["lat"], observer["lon"]

    ra, dec = target["ra"], target["dec"]

    # Divide-by-zero errors can occur when we have cos(90), and sin(0)/sin(180) etc
    # cosine: multiples of π/2
    # sine: 0, and multiples of π.
    if math.cos(math.radians(lat)) == 0:
        return {az: -1, alt: -1}

    # Get the hour angle for the target:
    ha = get_hour_angle(date, ra, lon)

    alt = math.asin(
        math.sin(math.radians(dec)) * math.sin(math.radians(lat))
        + math.cos(math.radians(dec))
        * math.cos(math.radians(lat))
        * math.cos(math.radians(ha))
    )

    az = math.acos(
        (
            math.sin(math.radians(dec))
            - math.sin(math.radians(alt)) * math.sin(math.radians(lat))
        )
        / (math.cos(math.radians(alt)) * math.cos(math.radians(lat)))
    )

    return {
        "az": 360 - math.degrees(az)
        if math.sin(math.radians(ha)) > 0
        else math.degrees(az),
        "alt": math.degrees(alt),
    }
