from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.moon import (
    Phase,
    get_age,
    get_angular_diameter,
    get_annual_equation_correction,
    get_corrected_ecliptic_longitude_of_the_ascending_node,
    get_distance,
    get_ecliptic_latitude,
    get_ecliptic_longitude,
    get_elongation,
    get_equatorial_coordinate,
    get_evection_correction,
    get_illumination,
    get_mean_anomaly,
    get_mean_anomaly_correction,
    get_mean_ecliptic_longitude,
    get_mean_ecliptic_longitude_of_the_ascending_node,
    get_mean_geometric_longitude,
    get_phase,
    get_phase_angle,
    get_true_anomaly,
    get_true_ecliptic_longitude,
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
    Ev = get_evection_correction(date)
    assert Ev == -0.5580522629166632


def test_get_mean_anomaly():
    M = get_mean_anomaly(date)
    assert M == 207.63633585681964


def test_get_mean_anomaly_correction():
    Ca = get_mean_anomaly_correction(date)
    assert Ca == 206.64428333417192


def test_get_mean_geometric_longitude():
    l = get_mean_geometric_longitude(date)
    assert l == 80.32626508452813


def test_get_mean_ecliptic_longitude_of_the_ascending_node():
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date)
    assert Ω == 71.6938262475226


def test_get_mean_ecliptic_longitude():
    λ = get_mean_ecliptic_longitude(date)
    assert λ == 79.88317358099448


def test_get_true_anomaly():
    ν = get_true_anomaly(date)
    assert ν == 357.3514315617634


def test_get_true_ecliptic_longitude():
    λt = get_true_ecliptic_longitude(date)
    assert λt == 77.01224128076132


def test_get_corrected_ecliptic_longitude_of_the_ascending_node():
    Ω = get_corrected_ecliptic_longitude_of_the_ascending_node(date)
    assert Ω == 71.56888914504515


def test_get_ecliptic_longitude():
    λ = get_ecliptic_longitude(date)
    assert λ == 76.99043727540315


def test_get_ecliptic_latitude():
    β = get_ecliptic_latitude(date)
    assert β == 0.4874504338736112


def test_get_equatorial_coordinate():
    date = datetime(2015, 1, 2, 3, 0, 0, 0, tzinfo=timezone.utc)
    eq = get_equatorial_coordinate(date)
    assert eq["ra"] == 63.854089783072595
    assert eq["dec"] == 17.246094608898062


def test_get_elongation():
    date = datetime(2015, 1, 2, 3, 0, 0, 0, tzinfo=timezone.utc)
    elongation = get_elongation(date)
    assert elongation == 143.73394864456367


def test_get_angular_diameter():
    date = datetime(2015, 1, 2, 3, 0, 0, 0, tzinfo=timezone.utc)
    d = get_angular_diameter(date)
    assert d == 0.5480234986129843


def test_get_distance():
    date = datetime(2015, 1, 2, 3, 0, 0, 0, tzinfo=timezone.utc)
    d = get_distance(date)
    assert d - 363410767 < 0.1


def test_get_age():
    date = datetime(2015, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    age = get_age(date)
    assert age["A"] == 130.40251122256336
    assert age["a"] == 10.696845549747305


def test_get_phase_angle():
    date = datetime(2015, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    PA = get_phase_angle(date)
    assert PA == 49.66441438659977


def test_get_illumination():
    date = datetime(2015, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    K = get_illumination(date)
    assert K == 82.36316687224799


def test_get_phase():
    date = datetime(2015, 1, 2, 2, 0, 0, 0, tzinfo=timezone.utc)
    phase = get_phase(date)
    assert phase == Phase.WaxingGibbous

    date = datetime(2015, 1, 5, 7, 0, 0, 0, tzinfo=timezone.utc)
    phase = get_phase(date)
    assert phase == Phase.Full

    date = datetime(2015, 1, 7, 23, 0, 0, 0, tzinfo=timezone.utc)
    phase = get_phase(date)
    assert phase == Phase.WaningGibbous

    date = datetime(2015, 2, 12, 17, 0, 0, 0, tzinfo=timezone.utc)
    phase = get_phase(date)
    assert phase == Phase.LastQuarter
