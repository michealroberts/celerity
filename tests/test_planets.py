# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timezone

from src.celerity.planet import Planet
from src.celerity.planets import get_planetary_heliocentric_coordinate

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# **************************************************************************************


def test_mercury_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.MERCURY)
    assert round(heliocentric["λ"], 6) == 170.864498
    assert round(heliocentric["β"], 6) == 5.931069
    assert round(heliocentric["r"], 6) == 0.374603


# **************************************************************************************


def test_venus_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.VENUS)
    assert round(heliocentric["λ"], 6) == 83.916163
    assert round(heliocentric["β"], 6) == 0.416697
    assert round(heliocentric["r"], 6) == 0.720040


# **************************************************************************************


def test_earth_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.EARTH)
    assert round(heliocentric["λ"], 6) == 233.440761
    assert round(heliocentric["β"], 6) == -0.000122
    assert round(heliocentric["r"], 6) == 1.01065


# **************************************************************************************


def test_mars_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.MARS)
    assert round(heliocentric["λ"], 6) == 130.095132
    assert round(heliocentric["β"], 6) == 1.823494
    assert round(heliocentric["r"], 6) == 1.648289


# **************************************************************************************


def test_jupiter_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.JUPITER)
    assert round(heliocentric["λ"], 6) == 318.552721
    assert round(heliocentric["β"], 6) == -0.799595
    assert round(heliocentric["r"], 6) == 5.052915


# **************************************************************************************


def test_saturn_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.SATURN)
    assert round(heliocentric["λ"], 6) == 307.718115
    assert round(heliocentric["β"], 6) == -0.596501
    assert round(heliocentric["r"], 6) == 9.964734


# **************************************************************************************


def test_uranus_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.URANUS)
    assert round(heliocentric["λ"], 6) == 40.838694
    assert round(heliocentric["β"], 6) == -0.42383
    assert round(heliocentric["r"], 6) == 19.754559


# **************************************************************************************


def test_neptune_heliocentric_coordinate():
    heliocentric = get_planetary_heliocentric_coordinate(date, Planet.NEPTUNE)
    assert round(heliocentric["λ"], 6) == 351.034035
    assert round(heliocentric["β"], 6) == -1.113431
    assert round(heliocentric["r"], 6) == 29.924546


# **************************************************************************************
