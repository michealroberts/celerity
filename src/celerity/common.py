# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from math import cos, pow, radians
from typing import Any, TypedDict

# *****************************************************************************************************************


class Age(TypedDict):
    a: float
    A: float


# *****************************************************************************************************************


class EquatorialCoordinate(TypedDict):
    ra: float
    dec: float


# *****************************************************************************************************************


class GeographicCoordinate(TypedDict):
    lat: float
    lon: float


# *****************************************************************************************************************


class HorizontalCoordinate(TypedDict):
    alt: float
    az: float


# *****************************************************************************************************************


def is_equatorial_coordinate(coordinate: Any) -> EquatorialCoordinate | None:
    if type(coordinate) is not dict:
        return None

    return (
        EquatorialCoordinate({"ra": coordinate["ra"], "dec": coordinate["dec"]})
        if "ra" in coordinate and "dec" in coordinate
        else None
    )


# *****************************************************************************************************************


def is_horizontal_coordinate(coordinate: Any) -> HorizontalCoordinate | None:
    if type(coordinate) is not dict:
        return None

    return (
        HorizontalCoordinate({"alt": coordinate["alt"], "az": coordinate["az"]})
        if "az" in coordinate and "alt" in coordinate
        else None
    )


# *****************************************************************************************************************


def get_F_orbital_parameter(ν: float, e: float) -> float:
    return (1 + (e * cos(radians(ν)))) / (1 - pow(e, 2))


# *****************************************************************************************************************
