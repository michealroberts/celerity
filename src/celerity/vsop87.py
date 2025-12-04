# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import cos
from typing import Sequence

from .tai import get_tt_utc_offset
from .temporal import get_julian_millennia

# **************************************************************************************


@dataclass(frozen=True)
class VSOP87Term:
    """
    A single VSOP87 term: A * cos(B + C * τ)
    """

    # A: amplitude (dimension depends on series; typically radians or AU):
    amplitude: float

    # B: phase angle (in radians):
    phase: float

    # C: frequency (in radians per Julian millennia):
    frequency: float

    def at(self, date: datetime) -> float:
        """
        Evaluate this VSOP87 term at a particular datetime.

        :param date: The datetime object to evaluate the term at.
        :return: The value of the term at the given datetime.
        """
        # Get the offset between Terrestrial Time (TT) and UTC for the given date:
        TT = get_tt_utc_offset(date)

        # Apply the TT offset to get the Terrestrial Time (TT) datetime:
        when: datetime = date + timedelta(seconds=TT)

        # Calculate Julian millennia since J2000.0 for the given datetime
        # in Terrestrial Time (TT):
        τ = get_julian_millennia(when)

        return self.amplitude * cos(self.phase + self.frequency * τ)


# **************************************************************************************


@dataclass(frozen=True)
class PlanetVSOP87Series:
    """
    Complete VSOP87 series for a planet in spherical ecliptic coordinates.
    """

    λ: Sequence[Sequence[VSOP87Term]]
    β: Sequence[Sequence[VSOP87Term]]
    r: Sequence[Sequence[VSOP87Term]]


# **************************************************************************************
