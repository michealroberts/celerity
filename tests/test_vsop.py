# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from src.celerity.vsop87 import Planet, PlanetVSOP87Series, get_vsop87_series

# **************************************************************************************


def test_earth_vsop87_series_loaded():
    earth = get_vsop87_series(Planet.EARTH)
    assert earth is not None
    assert len(earth.λ) > 0
    assert len(earth.β) > 0
    assert len(earth.r) > 0


# **************************************************************************************


def test_all_planets_vsop87_series_loaded():
    for p in Planet:
        s = get_vsop87_series(p)

        assert isinstance(s, PlanetVSOP87Series)
        assert len(s.λ) > 0
        assert len(s.β) > 0
        assert len(s.r) > 0


# **************************************************************************************
