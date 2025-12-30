# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from dataclasses import dataclass

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
