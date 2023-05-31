from pytest import approx

from src.celerity.parallax import get_distance


def test_get_distance():
    # Test that the distance to Betelgeuse is within 1% of the expected value:
    parallax = get_distance(5.95 / 1000)
    assert parallax > 165 and parallax < 170
    assert parallax == approx(168.1, rel=0.01)
