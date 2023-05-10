# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

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
