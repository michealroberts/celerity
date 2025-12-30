# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from dataclasses import dataclass
from typing import Sequence, Tuple

# **************************************************************************************


@dataclass(frozen=True)
class DETerm:
    """
    A single scalar coefficient in a Chebyshev polynomial series from the DE ephemeris
    (e.g. DE442).

    This represents one term of a Chebyshev series, consisting of a coefficient
    multiplied by a Chebyshev polynomial of a given degree.

    The term is typically used with a normalized time argument x in [-1, 1].
    """

    coefficient: float


# **************************************************************************************


@dataclass(frozen=True)
class DESegment:
    """
    A single DE ephemeris segment containing Chebyshev coefficients for a body's
    barycentric position over a fixed time interval.

    A segment corresponds to one contiguous time span in the development ephemeris.

    Within this interval, the position of a body is represented by three independent
    Chebyshev series (x, y, z), each defined by a set of coefficients.
    """

    # Start epoch (Julian days, TDB):
    start: float

    # End epoch (Julian days, TDB):
    end: float

    # Chebyshev coefficients for x:
    x: Tuple[float, ...]

    # Chebyshev coefficients for y:
    y: Tuple[float, ...]

    # Chebyshev coefficients for z:
    z: Tuple[float, ...]


# **************************************************************************************


@dataclass(frozen=True)
class PlanetDE442Series:
    """
    Complete DE442 ephemeris series for a planet relative to the Solar System Barycenter.
    """

    segments: Sequence[DESegment]


# **************************************************************************************
