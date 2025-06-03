# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import acos, atan2, cos, degrees, inf, pow, radians, sin, tan
from typing import Union, overload

from .common import (
    EquatorialCoordinate,
    GeographicCoordinate,
    HorizontalCoordinate,
    is_equatorial_coordinate,
    is_horizontal_coordinate,
)
from .temporal import get_julian_date, get_local_sidereal_time

# **************************************************************************************


@overload
def get_angular_separation(
    A: EquatorialCoordinate, B: EquatorialCoordinate
) -> float: ...
@overload
def get_angular_separation(
    A: HorizontalCoordinate, B: HorizontalCoordinate
) -> float: ...
def get_angular_separation(
    A: Union[EquatorialCoordinate, HorizontalCoordinate],
    B: Union[EquatorialCoordinate, HorizontalCoordinate],
) -> float:
    """
    The angular separation between two objects in the sky is the angle between
    the two objects as seen by an observer on Earth.

    :param A: The equatorial coordinate of the observed object.
    :param B: The equatorial coordinate of the observed object.
    :return The angular separation in degrees between target A and target B.
    :raises TypeError: If A and B are not both EquatorialCoordinate or HorizontalCoordinate.
    """
    θ = inf

    # Calculate the angular separation between A and B (in degrees):
    α = is_equatorial_coordinate(A)
    β = is_equatorial_coordinate(B)

    if α is not None and β is not None:
        θ = (
            degrees(
                acos(
                    sin(radians(α["dec"])) * sin(radians(β["dec"]))
                    + cos(radians(α["dec"]))
                    * cos(radians(β["dec"]))
                    * cos(radians(α["ra"] - β["ra"]))
                )
            )
            % 360
        )

    a = is_horizontal_coordinate(A)
    b = is_horizontal_coordinate(B)

    if a is not None and b is not None:
        θ = (
            degrees(
                acos(
                    sin(radians(a["alt"])) * sin(radians(b["alt"]))
                    + cos(radians(a["alt"]))
                    * cos(radians(b["alt"]))
                    * cos(radians(a["az"] - b["az"]))
                )
            )
            % 360
        )

    # Correct for negative angles:
    if θ < 0:
        θ += 360

    return θ


# **************************************************************************************


def get_hour_angle(date: datetime, ra: float, longitude: float) -> float:
    """
    Gets the hour angle for a particular object for a particular observer
    at a given datetime

    :param date: The datetime object to convert.
    :param ra: The right ascension of the observed object's equatorial coordinate.
    :param longitude: The longitude of the observer in degrees.
    :return The hour angle in degrees.
    """
    LST = get_local_sidereal_time(date, longitude)

    ha = LST * 15 - ra

    # If the hour angle is less than zero, ensure we rotate by 2π radians (360 degrees)
    if ha < 0:
        ha += 360

    return ha


# **************************************************************************************


def get_obliquity_of_the_ecliptic(date: datetime) -> float:
    """
    Gets the obliquity of the ecliptic for a particular datetime

    The obliquity of the ecliptic is the angle between the ecliptic and the celestial
    equator, and is used to convert between ecliptic and equatorial coordinates.

    :param date: The datetime object to convert.
    :return The obliquity of the ecliptic in degrees.
    """
    # Get the Julian date:
    JD = get_julian_date(date)

    # Calculate the number of centuries since J2000.0:
    T = (JD - 2451545.0) / 36525

    # Calculate the obliquity of the ecliptic:
    return 23.439292 - (46.845 * T + 0.00059 * pow(T, 2) + 0.001813 * pow(T, 3)) / 3600


# **************************************************************************************


def get_parallactic_angle(
    date: datetime,
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
) -> float:
    """
    Gets the parallactic angle for a particular object for a particular observer
    at a given datetime

    :param date: The datetime object to convert.
    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :return The parallactic angle in degrees.
    """
    lat, lon = radians(observer["lat"]), observer["lon"]

    dec = radians(target["dec"])

    # Get the hour angle for the target:
    ha = radians(get_hour_angle(date, target["ra"], lon))

    # Calculate the parallactic angle and return in degrees:
    return degrees(
        atan2(
            sin(ha),
            tan(lat) * cos(dec) - sin(dec) * cos(ha),
        )
    )


# **************************************************************************************
