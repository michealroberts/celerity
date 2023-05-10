# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from math import acos, cos, degrees, radians, sin, tan
from typing import Literal, TypedDict, Union

from .common import EquatorialCoordinate, GeographicCoordinate

# *****************************************************************************************************************


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


# *****************************************************************************************************************


class TransitParameters(TypedDict):
    Ar: float
    H1: float


# *****************************************************************************************************************


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


# *****************************************************************************************************************


def get_transit(
    observer: GeographicCoordinate,
    target: EquatorialCoordinate,
) -> Transit | Literal[None]:
    """
    Determines the local sidereal time and azimuthal angle of rise and set for an object.

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


# *****************************************************************************************************************
