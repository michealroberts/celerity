from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.moon import (
    get_annual_equation_correction,
    get_avection_correction,
    get_mean_anomaly,
    get_mean_ecliptic_longitude,
    get_mean_ecliptic_longitude_of_the_ascending_node,
    get_mean_geometric_longitude,
)

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}


def test_get_annual_equation_correction():
    Ae = get_annual_equation_correction(date)
    assert Ae == 0.1450832102519408


def test_get_avection_correction():
    Ev = get_avection_correction(date)
    assert Ev == -0.5580522629166632


def test_get_mean_anomaly():
    M = get_mean_anomaly(date)
    assert M == 207.63633585681964


def test_get_mean_geometric_longitude():
    l = get_mean_geometric_longitude(date)
    assert l == 80.32626508452813


def test_get_mean_ecliptic_longitude_of_the_ascending_node():
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date)
    assert Ω == 71.6938262475226


def test_get_mean_ecliptic_longitude():
    λ = get_mean_ecliptic_longitude(date)
    assert λ == 79.88317358099448
