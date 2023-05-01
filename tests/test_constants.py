from src.celerity.constants import J1900, J2000


def test_J1900():
    assert J1900 == 2415020.0


def test_J2000():
    assert J2000 == 2451545.0
