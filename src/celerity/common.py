# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from math import cos, pow, radians
from typing import TypedDict

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


def get_F_orbital_parameter(ν: float, e: float) -> float:
    return (1 + (e * cos(radians(ν)))) / (1 - pow(e, 2))
