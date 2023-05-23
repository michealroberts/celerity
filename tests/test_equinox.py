from src.celerity.equinox import get_spring_equinox


def test_get_spring_equinox():
    e = get_spring_equinox(2004)
    assert e.year == 2004
    assert e.month == 3
    assert e.day == 20
    assert e.hour == 6
    assert e.minute == 42
    assert e.second == 35
