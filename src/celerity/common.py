from typing import TypedDict


class EquatorialCoordinate(TypedDict):
    ra: float
    dec: float


class GeographicCoordinate(TypedDict):
    lat: float
    lon: float


class HorizontalCoordinate(TypedDict):
    alt: float
    az: float
