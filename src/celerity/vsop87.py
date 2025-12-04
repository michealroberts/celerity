# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from importlib import resources
from json import loads
from math import cos
from typing import Dict, Sequence

from .planet import Planet
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


def _compute_terms(d: dict, k: str) -> Sequence[Sequence[VSOP87Term]]:
    S: list[list[VSOP87Term]] = []
    for terms in d[k]:
        s: list[VSOP87Term] = []
        for term in terms:
            s.append(
                VSOP87Term(
                    amplitude=float(term["A"]),
                    phase=float(term["B"]),
                    frequency=float(term["C"]),
                )
            )
        S.append(s)
    return S


# **************************************************************************************


@lru_cache(maxsize=1)
def _load_vsop() -> Dict[Planet, PlanetVSOP87Series]:
    uri = resources.files("celerity.data").joinpath("vsop87d.json")
    table = loads(uri.read_text(encoding="utf-8"))

    raw = table["planets"]

    planets: Dict[Planet, PlanetVSOP87Series] = {}

    for name, d in raw.items():
        planet = Planet(name)
        planets[planet] = PlanetVSOP87Series(
            λ=_compute_terms(d, "λ"),
            β=_compute_terms(d, "β"),
            r=_compute_terms(d, "r"),
        )

    return planets


# **************************************************************************************


def get_vsop87_series(planet: Planet) -> PlanetVSOP87Series:
    """
    Retrieve the VSOP87 series for a specified planet.

    :param planet: The planet to retrieve the VSOP87 series for.
    :return: The VSOP87 series terms for the specified planet.
    """
    return _load_vsop()[planet]


# **************************************************************************************

if __name__ == "__main__":
    # Run as uv run python -m celerity.vsop87 to test loading the VSOP87 data:
    earth = get_vsop87_series(Planet.EARTH)
    print(f"Earth VSOP87 Series: {earth}")

# **************************************************************************************
