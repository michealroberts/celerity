from src.celerity.solstice import get_summer_solstice, get_winter_solstice


def test_get_summer_solstice():
    e = get_summer_solstice(2004)
    assert e.year == 2004
    assert e.month == 6
    assert e.day == 21
    assert e.hour == 0
    assert e.minute == 49
    assert e.second == 40


def test_get_winter_solstice():
    e = get_winter_solstice(2004)
    assert e.year == 2004
    assert e.month == 12
    assert e.day == 21
    assert e.hour == 12
    assert e.minute == 44
    assert e.second == 21
