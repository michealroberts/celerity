from src.celerity.common import get_F_orbital_parameter


def test_get_F_orbital_parameter():
    # Test for the Sun:
    F = get_F_orbital_parameter(43.025813, 0.016708)
    assert F == 1.012496968671173

    # Test for the Moon:
    F = get_F_orbital_parameter(6.086312, 0.0549)
    assert F == 1.0577787008793529
