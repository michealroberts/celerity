from src.celerity.utilities import (
    convert_degree_to_dms,
    get_normalised_azimuthal_degree,
    get_normalised_inclination_degree,
)


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


def test_get_normalised_inclination_degree():
    degree = get_normalised_inclination_degree(91)
    assert degree == 89

    degree = get_normalised_inclination_degree(-91)
    assert degree == -89

    degree = get_normalised_inclination_degree(0)
    assert degree == 0

    degree = get_normalised_inclination_degree(90)
    assert degree == 90

    degree = get_normalised_inclination_degree(-90)
    assert degree == -90

    degree = get_normalised_inclination_degree(180)
    assert degree == 0

    degree = get_normalised_inclination_degree(-180)
    assert degree == 0

    degree = get_normalised_inclination_degree(270)
    assert degree == -90

    degree = get_normalised_inclination_degree(-270)
    assert degree == 90

    degree = get_normalised_inclination_degree(120)
    assert degree == 60

    degree = get_normalised_inclination_degree(-130)
    assert degree == -50


def test_convert_degree_to_dms():
    dms = convert_degree_to_dms(-11.1614)
    assert dms == {"deg": -11, "min": 9, "sec": 41.04}
    dms = convert_degree_to_dms(7.4070639)
    assert dms == {"deg": 7, "min": 24, "sec": 25.43}
