# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import acos, asin, cos, degrees, radians, sin, atan2

from .aberration import get_correction_to_equatorial_for_aberration
from .astrometry import get_hour_angle
from .common import EquatorialCoordinate, GeographicCoordinate, HorizontalCoordinate
from .nutation import get_correction_to_equatorial_for_nutation
from .precession import get_correction_to_equatorial_for_precession_of_equinoxes
from .temporal import get_local_sidereal_time

# **************************************************************************************


def get_correction_to_equatorial(
    date: datetime, target: EquatorialCoordinate
) -> EquatorialCoordinate:
    """
    Apply all corrections to the equatorial coordinate of a target for a
    particular datetime

    Due to various factors, the equatorial coordinate as quoted for a target
    at epoch J2000.0 will not be accurate for a given datetime. This function
    applies all corrections to the equatorial coordinate of a target for a
    particular datetime.

    :param date: The datetime object to convert.
    :param target: The equatorial coordinate of the observed object at epoch J2000.0.
    """

    # Correction to the equatorial coordinate of our target for nutation:
    corr = get_correction_to_equatorial_for_nutation(date, target)

    # Apply the correction to the target's equatorial coordinate:
    target["ra"] += corr["ra"]
    target["dec"] += corr["dec"]

    # Correction to the equatorial coordinate of our target for aberration:
    corr = get_correction_to_equatorial_for_aberration(date, target)

    # Apply the correction to the target's equatorial coordinate:
    target["ra"] += corr["ra"]
    target["dec"] += corr["dec"]

    # Correction to the equatorial coordinate of our target for precession:
    corr = get_correction_to_equatorial_for_precession_of_equinoxes(date, target)

    # Apply the correction to the target's equatorial coordinate:
    target["ra"] += corr["ra"]
    target["dec"] += corr["dec"]

    return target


# **************************************************************************************


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


# **************************************************************************************


def convert_horizontal_to_equatorial(
    date: datetime,
    observer: GeographicCoordinate,
    target: HorizontalCoordinate,
) -> EquatorialCoordinate:
    """
    Converts horizontal coordinates (azimuth, altitude) back to equatorial
    coordinates (right ascension, declination) for a given observer and datetime.

    The azimuth is assumed to be measured from north toward east.

    :param date: The datetime of observation.
    :param observer: The geographic coordinate of the observer.
    :param target: The horizontal coordinate of the observed object.
    :return: The equatorial coordinate (RA and Dec) of the object.
    """
    # Convert the latitude to radians:
    latitude = radians(observer["lat"])

    # Convert the altitude to radians:
    a = radians(target["alt"])

    # Convert the azimuth to radians:
    A = radians(target["az"])

    # Compute the declination:
    dec = asin(sin(a) * sin(latitude) + cos(a) * cos(latitude) * cos(A))

    # Compute the cosine of declination:
    cos_dec = cos(dec)

    # Protect against division by zero (object near the pole)
    if abs(cos_dec) < 1e-10:
        raise ValueError("cos(dec) is too small; hour angle is indeterminate.")

    sin_H = -cos(a) * sin(A) / cos_dec
    cos_H = (sin(a) - sin(latitude) * sin(dec)) / (cos(latitude) * cos_dec)

    # Compute the hour angle in radians:
    ha = atan2(sin_H, cos_H)

    # Compute Local Sidereal Time (LST) in degrees, and convert to radians:
    LST = get_local_sidereal_time(date, observer["lon"])

    # Right Ascension (RA) is given by LST - the hour angle:
    ra = ((LST * 15) - degrees(ha)) % 360

    return {
        "ra": ra,
        "dec": degrees(dec),
    }


# **************************************************************************************
