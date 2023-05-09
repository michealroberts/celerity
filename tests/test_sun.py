from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.sun import (
    get_equation_of_center,
    get_mean_anomaly,
    get_mean_geometric_longitude,
    get_true_anomaly,
    get_true_geometric_longitude,
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


def test_get_mean_anomaly():
    M = get_mean_anomaly(date)
    assert M == 128.66090142411576


def test_get_mean_geometric_longitude():
    L = get_mean_geometric_longitude(date)
    assert L == 51.96564888161811


def test_get_equation_of_center():
    C = get_equation_of_center(date)
    assert C == 1.4754839423594455


def test_get_true_anomaly():
    ν = get_true_anomaly(date)
    assert ν == 130.1363853664752


def test_get_true_geometric_longitude():
    L = get_true_geometric_longitude(date)
    assert L == 53.441132823977554
