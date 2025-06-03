# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import cos, pow, radians
from typing import Any, NotRequired, TypedDict

# **************************************************************************************


class Age(TypedDict):
    a: float
    A: float


# **************************************************************************************


class Angle(TypedDict):
    deg: float
    min: float
    sec: float


# **************************************************************************************


class HourAngle(TypedDict):
    hour: float
    min: float
    sec: float


# **************************************************************************************


class EquatorialCoordinate(TypedDict):
    ra: float
    dec: float


# **************************************************************************************


class GeographicCoordinate(TypedDict):
    lat: float
    lon: float
    el: NotRequired[float]


# **************************************************************************************


class HorizontalCoordinate(TypedDict):
    alt: float
    az: float


# **************************************************************************************


class Measurement(TypedDict):
    """
    Represents a measurement with an associated value and optional uncertainty.

    Attributes:
        value (float): The measured value.
        uncertainty (Optional[float]): The uncertainty of the measurement, if available.
    """

    value: float
    uncertainty: NotRequired[float]


# **************************************************************************************


def is_equatorial_coordinate(coordinate: Any) -> EquatorialCoordinate | None:
    if not isinstance(coordinate, dict):
        return None

    return (
        EquatorialCoordinate({"ra": coordinate["ra"], "dec": coordinate["dec"]})
        if "ra" in coordinate and "dec" in coordinate
        else None
    )


# **************************************************************************************


def is_horizontal_coordinate(coordinate: Any) -> HorizontalCoordinate | None:
    if not isinstance(coordinate, dict):
        return None

    return (
        HorizontalCoordinate({"alt": coordinate["alt"], "az": coordinate["az"]})
        if "az" in coordinate and "alt" in coordinate
        else None
    )


# **************************************************************************************


def get_F_orbital_parameter(ν: float, e: float) -> float:
    return (1 + (e * cos(radians(ν)))) / (1 - pow(e, 2))


# **************************************************************************************
