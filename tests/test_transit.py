from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.transit import (
    get_does_object_rise_or_set,
    get_next_rise,
    get_next_set,
    get_transit,
    is_object_below_horizon,
    is_object_circumpolar,
    is_object_never_visible,
)

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

polaris: EquatorialCoordinate = {"ra": 37.952659, "dec": 89.264108}

LMC: EquatorialCoordinate = {"ra": 80.8941667, "dec": -69.7561111}

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}


def test_get_does_object_rise_or_set():
    d = get_does_object_rise_or_set(observer, betelgeuse)
    assert d["Ar"] == 0.13703602843777568
    assert d["H1"] == 0.04685668397579211

    d = get_does_object_rise_or_set({"lat": 80, "lon": 0}, betelgeuse)
    assert d["Ar"] == 0.7424083500051002
    assert d["H1"] == 0.7372819131688116

    d = get_does_object_rise_or_set({"lat": -85, "lon": 0}, betelgeuse)
    assert d == False


def test_is_object_never_visible():
    d = is_object_never_visible(observer, polaris, 0)
    assert d == False

    d = is_object_never_visible({"lat": -85, "lon": 0}, polaris, 0)
    assert d == True

    d = is_object_never_visible(observer, betelgeuse, 0)
    assert d == False

    d = is_object_never_visible({"lat": -50, "lon": 0}, betelgeuse, 0)
    assert d == True

    d = is_object_never_visible({"lat": -85, "lon": 0}, betelgeuse, 0)
    assert d == True


def test_is_object_circumpolar():
    p = is_object_circumpolar(observer, polaris, 0)
    assert p == True

    so = is_object_circumpolar(
        {"lat": -85, "lon": 0}, {"ra": 317.398, "dec": -88.956}, 0
    )
    assert so == True


def test_is_object_below_horizon():
    # Polaris should be above the horizon on May 14, 2021:
    p = is_object_below_horizon(date, observer, polaris, 0)
    assert p == False

    # Betelgeuse should be below the horizon at 3am on July 14, 2021:
    b = is_object_below_horizon(
        datetime(2021, 7, 14, 3, 0, 0, tzinfo=timezone.utc), observer, betelgeuse, 0
    )
    assert b == True


def test_get_transit():
    T = get_transit(observer, betelgeuse)
    assert T["LSTr"] == 23.740485646638913
    assert T["LSTs"] == 12.098575460027751
    assert T["R"] == 82.12362992591511
    assert T["S"] == 277.8763700740849


def test_get_next_rise():
    # By 9pm on May 14, 2021, Betelgeuse should have already risen:
    date = datetime(2021, 5, 14, 21, 0, 0, 0)
    # Therefore the next rise should be on May 15, 2021:
    r = get_next_rise(date, observer, betelgeuse, 0)
    assert r["LST"] == 23.740485646638913
    assert r["GST"] == 10.105025246638917
    assert r["az"] == 82.12362992591511
    assert r["date"] == datetime(2021, 5, 15, 18, 31, 28, 716561, tzinfo=timezone.utc)

    # Test where we know the object is circumpolar for the observer:
    r = get_next_rise(date, observer, polaris, 0)
    assert r == True

    # Test where we known the object only rises at specific times of the year:
    date = datetime(2021, 1, 12, 0, 0, 0, 0)
    r = get_next_rise(date, {"lat": 20.2437, "lon": observer["lon"]}, LMC, 0)
    assert r["date"] == datetime(2021, 1, 12, 8, 16, 12, 950867, tzinfo=timezone.utc)
    assert r["LST"] == 5.375729797576824
    assert r["GST"] == 15.740269397576824
    assert r["az"] == 179.91065185064514


def test_get_next_set():
    # By 7am on May 14, 2021, Betelgeuse should have already set:
    date = datetime(2021, 5, 14, 7, 0, 0, 0)
    s = get_next_set(date, observer, betelgeuse, 0)
    assert s["LST"] == 12.098575460027751
    assert s["GST"] == 22.463115060027754
    assert s["az"] == 277.8763700740849
    assert s["date"] == datetime(2021, 5, 15, 6, 54, 52, 256582, tzinfo=timezone.utc)

    # Test where we know the object is circumpolar for the observer:
    s = get_next_set(date, observer, polaris, 0)
    assert s == False

    # Test where we known the object only rises at specific times of the year:
    date = datetime(2021, 1, 12, 0, 0, 0, 0)
    s = get_next_set(date, {"lat": 20.2437, "lon": observer["lon"]}, LMC, 0)
    assert s["date"] == datetime(2021, 1, 12, 8, 18, 16, 557970, tzinfo=timezone.utc)
    assert s["LST"] == 5.410159095756511
    assert s["GST"] == 15.774698695756513
    assert s["az"] == 180.08934814935486
