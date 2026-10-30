from datetime import datetime, timedelta, timezone

from math import isclose

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
    assert ε == 23.436499838724593


def test_get_parallactic_angle():
    target = betelgeuse
    q = get_parallactic_angle(date, observer, target)
    assert q == -42.628126462207035


# **************************************************************************************


def test_get_obliquity_of_the_ecliptic_matches_erfa():
    # The reference value is ERFA obl06 (pyerfa 2.0.1.5) for 2021-05-14 00:00:00 UTC:
    assert isclose(
        get_obliquity_of_the_ecliptic(date), 23.436499838724593, abs_tol=1e-12
    )


# **************************************************************************************


def test_get_obliquity_of_the_ecliptic_at_j2000():
    # At J2000.0 the mean obliquity is 84381.406 arcseconds:
    ε = get_obliquity_of_the_ecliptic(datetime(2000, 1, 1, 11, 58, 55, 816000))
    assert isclose(ε, 84381.406 / 3600, abs_tol=1e-9)


# **************************************************************************************


def test_get_obliquity_of_the_ecliptic_decreases_with_time():
    # The mean obliquity falls by about 46.8 arcseconds per century at present:
    earlier = get_obliquity_of_the_ecliptic(datetime(1950, 1, 1, 0, 0, 0, 0))
    later = get_obliquity_of_the_ecliptic(datetime(2050, 1, 1, 0, 0, 0, 0))
    assert 46.0 < (earlier - later) * 3600 < 47.5


# **************************************************************************************


def test_get_obliquity_of_the_ecliptic_treats_naive_datetime_as_utc():
    assert get_obliquity_of_the_ecliptic(
        datetime(2021, 5, 14, 0, 0, 0, 0)
    ) == get_obliquity_of_the_ecliptic(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    )


# **************************************************************************************
