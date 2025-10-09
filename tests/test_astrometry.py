from datetime import datetime

from src.celerity.astrometry import (
    get_angular_separation,
    get_hour_angle,
    get_obliquity_of_the_ecliptic,
    get_parallactic_angle,
)
from src.celerity.common import EquatorialCoordinate, GeographicCoordinate

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

arcturus: EquatorialCoordinate = {"ra": 213.9153, "dec": 19.182409}

spica: EquatorialCoordinate = {"ra": 201.2983, "dec": -11.1614}

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}


def test_get_angular_separation():
    θ = get_angular_separation(arcturus, spica)
    assert θ == 32.79290589269233


def test_get_hour_angle():
    ha = get_hour_angle(date, betelgeuse["ra"], longitude)
    assert ha == 347.6988036852858


def test_get_obliquity_of_the_ecliptic():
    ε = get_obliquity_of_the_ecliptic(date)
    assert ε == 23.436511890585354


def test_get_parallactic_angle():
    target = betelgeuse
    q = get_parallactic_angle(date, observer, target)
    assert q == -42.628126462207035
