from src.celerity.common import (
    EquatorialCoordinate,
    get_F_orbital_parameter,
    is_equatorial_coordinate,
    is_horizontal_coordinate,
)

# For testing, we will define the star Betelgeuse:
betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}


def test_is_equatorial_coordinate():
    target = is_equatorial_coordinate(betelgeuse)
    assert target is not None
    assert target["ra"] == 88.7929583
    assert target["dec"] == 7.4070639

    target = is_equatorial_coordinate({"alt": 88.7929583, "az": 7.4070639})
    assert target is None


def test_is_horizontal_coordinate():
    target = is_horizontal_coordinate(betelgeuse)
    assert target is None

    target = is_horizontal_coordinate({"alt": 88.7929583, "az": 7.4070639})
    assert target is not None
    assert target["alt"] == 88.7929583
    assert target["az"] == 7.4070639


def test_get_F_orbital_parameter():
    # Test for the Sun:
    F = get_F_orbital_parameter(43.025813, 0.016708)
    assert F == 1.012496968671173

    # Test for the Moon:
    F = get_F_orbital_parameter(6.086312, 0.0549)
    assert F == 1.0577787008793529
