from src.celerity.constants import J1900, J1970, J2000


def test_J1900():
    assert J1900 == 2415020.0


def test_J1970():
    assert J1970 == 2440587.5


def test_J2000():
    assert J2000 == 2451545.0
