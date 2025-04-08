# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from math import acos, cos, degrees, radians, sin, tan
from typing import Literal, TypedDict, Union

from .common import (
    EquatorialCoordinate,
    GeographicCoordinate,
    HorizontalCoordinate,
    is_equatorial_coordinate,
    is_horizontal_coordinate,
)
from .coordinates import convert_equatorial_to_horizontal
from .temporal import (
    convert_greenwich_sidereal_time_to_universal_coordinate_time,
    convert_local_sidereal_time_to_greenwich_sidereal_time,
)

# **************************************************************************************


class Transit(TypedDict):
    """
    :property LSTr: The local sidereal time of rise.
    :property LSTs: The local sidereal time of set.
    :property R: The azimuthal angle (in degrees) of the object at rise.
    :property S: The azimuthal angle (in degrees) of the object at set.
    """

    LSTr: float
    LSTs: float
    R: float
    S: float


# **************************************************************************************


class Rise(TypedDict):
    """
    :property date: The date of rise.
    :property LSTr: The local sidereal time of rise.
    :property R: The azimuthal angle (in degrees) of the object at rise.
    """

    date: datetime
    LST: float
    GST: float
    az: float


# **************************************************************************************


class Set(TypedDict):
    """
    :property date: The date of set.
    :property LSTr: The local sidereal time of set.
    :property R: The azimuthal angle (in degrees) of the object at set.
    """

    date: datetime
    LST: float
    GST: float
    az: float


# **************************************************************************************


class TransitParameters(TypedDict):
    Ar: float
    H1: float


# **************************************************************************************


def is_object_circumpolar(
    observer: GeographicCoordinate, target: EquatorialCoordinate, horizon: float
) -> bool:
    """
    An object is considered circumpolar if it is always above the observer's
    horizon and never sets. This is true when the object's declination is
    greater than 90 degrees minus the observer's latitude.

    :param target: The equatorial coordinate of the observed object.
    :param observer: The geographic coordinate of the observer.
    :param horizon: The observer's horizon (in degrees).
    :return: True if the object is circumpolar, False otherwise.
    """
    # We only need the declination of the target object:
    dec = target["dec"]

    # We only need the latitude of the observer:
    lat = observer["lat"]

    # If the object's declination is greater than 90 degrees minus the observer's latitude,
    # then the object is circumpolar (always above the observer's horizon and never sets).
    return dec > (90 - lat - horizon) if lat > 0 else dec < (90 - lat - horizon)


# **************************************************************************************


def is_object_never_visible(
    observer: GeographicCoordinate, target: EquatorialCoordinate, horizon: float
) -> bool:
    """
    An object is never visible if it is always below the observer's horizon and never
    rises.

    This is true when the object's declination is less than the observer's
    latitude minus 90 degrees.

    :param target: The equatorial coordinate of the observed object.
    :param observer: The geographic coordinate of the observer.
    :param horizon: The observer's horizon (in degrees).
    :return: True if the object is never visible, False otherwise.
    """
    # We only need the declination of the target object:
    dec = target["dec"]

    # We only need the latitude of the observer:
    lat = observer["lat"]

    # If the object's declination is less than the observer's latitude
    # minus 90 degrees, then the object is never visible (always below the
    # observer's horizon and never rises).
    return dec < (lat - 90 + horizon) if lat > 0 else dec > (lat - 90 + horizon)


# **************************************************************************************


def is_object_below_horizon(
    date: datetime,
    observer: GeographicCoordinate,
    target: EquatorialCoordinate | HorizontalCoordinate,
    horizon: float,
) -> bool:
    """
    An object is never visible if it is always below the observer's horizon
    and never rises.

    This is true when the object's declination is less than the observer's
    latitude minus 90 degrees.

    :param target: The equatorial or horizontal coordinate of the observed object.
    :param observer: The geographic coordinate of the observer.
    :param horizon: The observer's horizon (in degrees).
    :return: True if the object is never visible, False otherwise.
    """
    # Attempt to type narrow the target coordinate as an equatorial coordinate:
    eq = is_equatorial_coordinate(target)

    if eq:
        # Convert the target's equatorial coordinate to horizontal coordinates:
        target = convert_equatorial_to_horizontal(date, observer, eq)

    hz = is_horizontal_coordinate(target)
    assert hz is not None

    # If the object's horizontal altitude local to some observer is less than the
    # observer's horizon, then the object is never visible (always below the
    # observer's horizon).
    return hz["alt"] < 0 + horizon


# **************************************************************************************


def get_does_object_rise_or_set(
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
) -> Union[Literal[False], TransitParameters]:
    """
    Determines whether an object rises or sets for an observer.

    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :return either false when the object does not rise or set or the transit parameters.
    """
    lat = radians(observer["lat"])

    dec = radians(target["dec"])

    # If |Ar| > 1, the object will never rise or set for the observer.
    Ar = sin(dec) / cos(lat)

    if abs(Ar) > 1:
        return False

    # If |H1| > 1, the object will never rise or set for the observer.
    H1 = tan(lat) * tan(dec)

    if abs(H1) > 1:
        return False

    return {"Ar": Ar, "H1": H1}


# **************************************************************************************


def get_transit(
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
) -> Transit | Literal[None]:
    """
    Determines the local sidereal time and azimuthal angle of rise
    and set for an object.

    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :return either None when the object does not rise or set or the transit timings.
    """
    # Convert the right ascension to hours:
    ra = target["ra"] / 15

    # Get the transit parameters:
    obj = get_does_object_rise_or_set(observer, target)

    if not obj:
        return None

    H1 = obj["H1"]

    H2 = degrees(acos(-H1)) / 15

    # Get the azimuthal angle of rise:
    R = degrees(acos(obj["Ar"]))

    # Get the azimuthal angle of set:
    S = 360 - R

    # The local sidereal time of rise:
    LSTr = 24 + ra - H2

    if LSTr > 24:
        LSTr -= 24

    LSTs = ra + H2

    if LSTs > 24:
        LSTs -= 24

    return {"LSTr": LSTr, "LSTs": LSTs, "R": R, "S": S}


# **************************************************************************************


def get_next_rise(
    date: datetime,
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
    horizon: float = 0,
) -> Rise | bool:
    """
    Determines the next rise time for an object, if at all.

    :param date: The date to start searching for the next rise.
    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :param horizon: The observer's horizon (in degrees).

    :return: The next rise time or False if the object never rises,
    or True if the object is always above the horizon (circumpolar)
    for the observer.
    """
    now = date

    # If the object is circumpolar, it never rises:
    if is_object_circumpolar(observer, target, horizon):
        return True

    # # If the object is never visible, it never rises:
    if is_object_never_visible(observer, target, horizon):
        return False

    # Get the transit parameters:
    transit = get_transit(observer, target)

    if not transit:
        return get_next_rise(
            date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            observer,
            target,
            horizon,
        )

    LSTr = transit["LSTr"]

    # Convert the local sidereal time of rise to Greenwich sidereal time:
    GSTr = convert_local_sidereal_time_to_greenwich_sidereal_time(LSTr, observer)

    # Convert the Greenwich sidereal time to universal coordinate time for the
    # date specified:
    rise = convert_greenwich_sidereal_time_to_universal_coordinate_time(date, GSTr)

    # If the rise is before the current time, then we know the next rise is tomorrow:
    if rise < now.astimezone(tz=timezone.utc):
        return get_next_rise(
            date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            observer,
            target,
            horizon,
        )

    return {
        "date": rise,
        "LST": transit["LSTr"],
        "GST": GSTr,
        "az": transit["R"],
    }


# **************************************************************************************


def get_next_set(
    date: datetime,
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
    horizon: float = 0,
) -> Rise | bool:
    """
    Determines the next set time for an object, if at all.

    :param date: The date to start searching for the next set.
    :param observer: The geographic coordinate of the observer.
    :param target: The equatorial coordinate of the observed object.
    :param horizon: The observer's horizon (in degrees).

    :return: The next set time or True if the object never sets,
    or False if the object is always above the horizon (circumpolar)
    for the observer.
    """
    now = date

    # If the object is circumpolar, it never rises:
    if is_object_circumpolar(observer, target, horizon):
        return False

    # # If the object is never visible, it never rises:
    if is_object_never_visible(observer, target, horizon):
        return True

    # Get the transit parameters:
    transit = get_transit(observer, target)

    if not transit:
        return get_next_set(
            date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            observer,
            target,
            horizon,
        )

    LSTs = transit["LSTs"]

    # Convert the local sidereal time of rise to Greenwich sidereal time:
    GSTs = convert_local_sidereal_time_to_greenwich_sidereal_time(LSTs, observer)

    # Convert the Greenwich sidereal time to universal coordinate time for
    # the date specified:
    set = convert_greenwich_sidereal_time_to_universal_coordinate_time(date, GSTs)

    # If the set is before the current time, then we know the next rise is tomorrow:
    if set < now.astimezone(tz=timezone.utc):
        return get_next_set(
            date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            observer,
            target,
            horizon,
        )

    return {
        "date": set,
        "LST": transit["LSTs"],
        "GST": GSTs,
        "az": transit["S"],
    }


# **************************************************************************************
