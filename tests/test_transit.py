from datetime import datetime

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.transit import get_does_object_rise_or_set

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

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
