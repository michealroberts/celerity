from src.celerity.utilities import get_normalised_azimuthal_degree


def test_get_normalised_azimuthal_degree():
    degree = get_normalised_azimuthal_degree(361)
    assert degree == 1

    degree = get_normalised_azimuthal_degree(-1)
    assert degree == 359

    degree = get_normalised_azimuthal_degree(0)
    assert degree == 0

    degree = get_normalised_azimuthal_degree(360)
    assert degree == 0

    degree = get_normalised_azimuthal_degree(720)
    assert degree == 0

    degree = get_normalised_azimuthal_degree(-360)
    assert degree == 0

    degree = get_normalised_azimuthal_degree(-720)
    assert degree == 0

    degree = get_normalised_azimuthal_degree(540)
    assert degree == 180

    degree = get_normalised_azimuthal_degree(-540)
    assert degree == 180

    degree = get_normalised_azimuthal_degree(180)
    assert degree == 180

    degree = get_normalised_azimuthal_degree(390)
    assert degree == 30
