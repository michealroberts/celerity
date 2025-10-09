from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.coordinates import convert_equatorial_to_horizontal
from src.celerity.sun import (
    get_angular_diameter,
    get_distance,
    get_ecliptic_longitude,
    get_equation_of_center,
    get_equatorial_coordinate,
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

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}


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


def test_get_ecliptic_longitude():
    date = datetime(2015, 2, 5, 12, 0, 0, 0, tzinfo=timezone.utc)
    λ = get_ecliptic_longitude(date)
    assert λ == 316.10388080739784


def test_get_equatorial_coordinate():
    date = datetime(2015, 2, 5, 12, 0, 0, 0, tzinfo=timezone.utc)
    eq = get_equatorial_coordinate(date)
    assert eq["ra"] == 318.5617376411268
    assert eq["dec"] == -16.008394691469505

    hz = convert_equatorial_to_horizontal(date, observer, eq)

    assert hz["alt"] == -69.40209879395105
    assert hz["az"] == 82.77542830157664

    # Add one hour to the date:
    date = datetime(2015, 2, 5, 13, 0, 0, 0, tzinfo=timezone.utc)

    eq = get_equatorial_coordinate(date)

    assert eq["ra"] == 318.60368091333004
    assert eq["dec"] == -15.995795336804742

    hz = convert_equatorial_to_horizontal(date, observer, eq)

    assert hz["alt"] == -55.32225076978145
    assert hz["az"] == 89.64913544932578


def test_get_angular_diameter():
    date = datetime(2015, 2, 15, 0, 0, 0, 0, tzinfo=timezone.utc)
    θ = get_angular_diameter(date)
    assert θ == 0.5398164296031396


def test_get_distance():
    date = datetime(2015, 2, 15, 0, 0, 0, 0, tzinfo=timezone.utc)
    d = get_distance(date)
    assert d == 147744945752.45538
