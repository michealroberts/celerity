# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timedelta
from math import degrees
from typing import Sequence

from .common import HeliocentricSphericalCoordinate
from .planet import Planet
from .tai import get_tt_utc_offset
from .temporal import get_julian_millennia
from .vsop87 import VSOP87Term, get_vsop87_series

# **************************************************************************************


def _evaluate_vsop_series(
    date: datetime,
    series: Sequence[Sequence[VSOP87Term]],
) -> float:
    TT = get_tt_utc_offset(date)

    tt = date + timedelta(seconds=TT)

    τ = get_julian_millennia(tt)

    v = 0.0

    τn = 1.0

    for n, s in enumerate(series):
        u = 0.0
        for term in s:
            u += term.at(date)

        if n == 0:
            v += u
        else:
            τn *= τ
            v += u * τn

    return v


# **************************************************************************************


def get_planetary_heliocentric_coordinate(
    date: datetime,
    planet: Planet,
) -> HeliocentricSphericalCoordinate:
    """
    Calculate the heliocentric spherical coordinates (λ, β, r) for a specified planet
    at a given date and time using the VSOP87 theory.

    :param date: The datetime of observation.
    :param planet: The planet, e.g., Planet.MERCURY, Planet.VENUS, etc.
    :return: A heliocentric coordinate (λ, β, r) for the specified planet.
    """
    # Retrieve the VSOP87 series for the specified planet:
    series = get_vsop87_series(planet)

    # Calculate the heliocentric longitude (λ):
    λ = (
        degrees(
            _evaluate_vsop_series(
                date=date,
                series=series.λ,
            )
        )
        % 360.0
    )

    # Calculate the heliocentric latitude (β):
    β = degrees(
        _evaluate_vsop_series(
            date=date,
            series=series.β,
        )
    )

    # Calculate the heliocentric radius (r):
    r = _evaluate_vsop_series(
        date=date,
        series=series.r,
    )

    return HeliocentricSphericalCoordinate(
        λ=λ,
        β=β,
        r=r,
    )


# **************************************************************************************
