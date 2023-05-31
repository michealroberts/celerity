from pytest import approx

from src.celerity.parallax import convert_parallax_to_metres, get_distance


def test_get_distance():
    # Test that the distance to Betelgeuse is within 1% of the expected value:
    parallax = get_distance(5.95 / 1000)
    assert parallax > 165 and parallax < 170
    assert parallax == approx(168.1, rel=0.01)


def test_convert_parallax_to_metres():
    # Test that the distance to Betelgeuse is within 1% of the expected value:
    parallax = get_distance(5.95 / 1000)
    metres = convert_parallax_to_metres(parallax)
    assert metres == 183597816086160.0
