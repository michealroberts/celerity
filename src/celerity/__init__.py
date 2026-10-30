# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

"""
Celerity is a lightweight, zero-dependency and type-safe
Python library for astronomical calculations.
"""

# **************************************************************************************

__version__ = "0.46.0"

# **************************************************************************************

from . import (
    aberration,
    astrometry,
    common,
    constants,
    constraints,
    coordinates,
    cosmology,
    deflection,
    earth,
    ecliptic,
    equinox,
    humanize,
    light,
    matrix,
    moon,
    night,
    nutation,
    parallax,
    photometry,
    planet,
    planets,
    precession,
    projection,
    refraction,
    seeing,
    solstice,
    sun,
    tai,
    temporal,
    transit,
    utilities,
    vector,
)
from .temporal import Time

# **************************************************************************************

__all__: list[str] = [
    "aberration",
    "astrometry",
    "common",
    "constants",
    "constraints",
    "coordinates",
    "cosmology",
    "deflection",
    "earth",
    "ecliptic",
    "equinox",
    "humanize",
    "light",
    "matrix",
    "moon",
    "night",
    "nutation",
    "parallax",
    "photometry",
    "planet",
    "planets",
    "precession",
    "projection",
    "refraction",
    "seeing",
    "solstice",
    "sun",
    "tai",
    "temporal",
    "transit",
    "utilities",
    "vector",
    "Time",
]

# **************************************************************************************
