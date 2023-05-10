from math import cos, radians, sin, tan
from typing import Literal, TypedDict, Union

from .common import EquatorialCoordinate, GeographicCoordinate


class TransitParameters(TypedDict):
    Ar: float
    H1: float


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
