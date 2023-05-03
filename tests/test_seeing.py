import math

from src.celerity.seeing import (
    get_airmass,
    get_airmass_karstenyoung,
    get_airmass_pickering,
)


def test_get_airmass():
    X = get_airmass(0)
    assert math.isclose(X, 38.75, rel_tol=0.01)

    X = get_airmass_pickering(72.78539444063767)
    assert X == 1.0466433379575284


def test_get_airmass_pickering():
    X = get_airmass_pickering(0)
    assert math.isclose(X, 38.75, rel_tol=0.01)

    X = get_airmass_pickering(72.78539444063767)
    assert X == 1.0466433379575284


def test_get_airmass_karstenyoung():
    X = get_airmass_karstenyoung(0)
    assert math.isclose(X, 37.92, rel_tol=0.01)

    X = get_airmass_karstenyoung(72.78539444063767)
    assert X == 1.046461951842933
