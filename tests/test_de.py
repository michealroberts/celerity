# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from src.celerity.de import Planet, PlanetDE442Series, get_de442_series

# **************************************************************************************


def test_earth_de442_series_loaded():
    earth = get_de442_series(Planet.EARTH)
    assert earth is not None
    assert len(earth.segments) > 0


# **************************************************************************************


def test_all_planets_de442_series_loaded():
    for p in Planet:
        s = get_de442_series(p)

        assert isinstance(s, PlanetDE442Series)
        assert len(s.segments) > 0


# **************************************************************************************
