# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime

from src.celerity.equinox import (
    get_autumn_equinox,
    get_equation_of_the_equinoxes,
    get_spring_equinox,
)

# **************************************************************************************


def test_get_spring_equinox():
    e = get_spring_equinox(2004)
    assert e.year == 2004
    assert e.month == 3
    assert e.day == 20
    assert e.hour == 6
    assert e.minute == 42
    assert e.second == 35


# **************************************************************************************


def test_get_autumn_equinox():
    e = get_autumn_equinox(2004)
    assert e.year == 2004
    assert e.month == 9
    assert e.day == 22
    assert e.hour == 16
    assert e.minute == 27
    assert e.second == 20


# **************************************************************************************


def test_get_equation_of_the_equinoxes():
    date = datetime(2021, 5, 14, 0, 0, 0, 0)
    E = get_equation_of_the_equinoxes(date)
    assert E == -0.004475059246864763


# **************************************************************************************
