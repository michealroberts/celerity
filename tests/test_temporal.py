# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone

import pytest

from src.celerity.common import GeographicCoordinate
from src.celerity.constants import J2000
from src.celerity.temporal import (
    convert_greenwich_sidereal_time_to_universal_coordinate_time,
    convert_local_sidereal_time_to_greenwich_sidereal_time,
    get_greenwich_sidereal_time,
    get_julian_centuries,
    get_julian_date,
    get_julian_millennia,
    get_local_sidereal_time,
    get_modified_julian_date,
    get_delta_t,
    get_modified_julian_date_as_parts,
    get_terrestrial_time_in_julian_centuries,
    get_universal_time,
)

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# **************************************************************************************

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# **************************************************************************************

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

# **************************************************************************************

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}

# **************************************************************************************


def test_get_julian_date():
    assert get_julian_date(date) == 2459348.5


# **************************************************************************************


def test_get_julian_centuries():
    T = get_julian_centuries(date)
    assert T == (2459348.5 - J2000) / 36525.0


# **************************************************************************************


def test_get_delta_t():
    # Reference values from the Espenak & Meeus (2006) table of ΔT (in seconds):
    assert get_delta_t(datetime(1900, 1, 1)) == pytest.approx(-2.7, abs=0.1)
    assert get_delta_t(datetime(1950, 1, 1)) == pytest.approx(29.1, abs=0.1)
    assert get_delta_t(datetime(2000, 1, 1)) == pytest.approx(63.8, abs=0.1)

    # In the leap second era ΔT must agree with TT-UTC to within the sub-second
    # difference between UT1 and UTC, and the fit error of the polynomial:
    assert get_delta_t(datetime(1970, 1, 1)) == pytest.approx(40.18, abs=0.1)

    # A naive datetime is treated as UTC, so it must agree with the same instant given in
    # an explicit non-UTC timezone:
    assert get_delta_t(datetime(1970, 1, 1, 0, 0, 0, 0)) == get_delta_t(
        datetime(1970, 1, 1, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    )

    # An aware datetime whose local year differs from its UTC year must be evaluated in
    # the UTC year, here 1959 rather than 1960:
    assert get_delta_t(
        datetime(1960, 1, 1, 5, 0, 0, 0, tzinfo=timezone(timedelta(hours=14)))
    ) == get_delta_t(datetime(1959, 12, 31, 15, 0, 0, 0, tzinfo=timezone.utc))

    # An aware datetime whose local month straddles a polynomial segment boundary must be
    # evaluated in the UTC month, here December 1960 (the 1941-1961 segment) rather than
    # January 1961 (the 1961-1986 segment):
    assert get_delta_t(
        datetime(1961, 1, 1, 0, 30, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    ) == get_delta_t(datetime(1960, 12, 31, 22, 30, 0, 0, tzinfo=timezone.utc))
    assert get_delta_t(
        datetime(1961, 1, 1, 0, 30, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    ) == get_delta_t(datetime(1960, 12, 1, 0, 0, 0, 0))

    # The fit is continuous across the segment boundaries to within a second:
    for year in (500, 1600, 1700, 1800, 1860, 1900, 1920, 1941, 1961, 1986, 2005, 2050):
        assert get_delta_t(datetime(year, 1, 1)) == pytest.approx(
            get_delta_t(datetime(year - 1, 12, 1)), abs=1.0
        )


# **************************************************************************************


def test_get_terrestrial_time_in_julian_centuries():
    # On 2021-05-14 TAI-UTC is 37 seconds, so TT-UTC is 37 + 32.184 = 69.184 seconds:
    T = get_terrestrial_time_in_julian_centuries(date)
    assert T == (2459348.5 + 69.184 / 86400.0 - J2000) / 36525.0

    # TT must always run ahead of UTC, compared for the same instant given explicitly in
    # UTC so the comparison does not depend on the host's local timezone:
    assert T > get_julian_centuries(
        datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)
    )

    # Before 1972 the TAI-UTC offset is not an integer number of leap seconds, so the
    # conversion falls back to ΔT (TT-UT) rather than a zero offset:
    T = get_terrestrial_time_in_julian_centuries(datetime(1970, 1, 1, 0, 0, 0, 0))
    assert (
        T == (2440587.5 + get_delta_t(datetime(1970, 1, 1)) / 86400.0 - J2000) / 36525.0
    )

    # The first instant of 1972 is accepted, with TAI-UTC at its initial 10 seconds:
    T = get_terrestrial_time_in_julian_centuries(datetime(1972, 1, 1, 0, 0, 0, 0))
    assert T == (2441317.5 + 42.184 / 86400.0 - J2000) / 36525.0

    # A naive datetime is treated as UTC, so it must agree with the same instant given
    # in an explicit non-UTC timezone:
    T = get_terrestrial_time_in_julian_centuries(date)
    assert T == get_terrestrial_time_in_julian_centuries(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    )


# **************************************************************************************


def test_get_julian_millennia():
    T = get_julian_centuries(date)
    assert get_julian_millennia(date) == T / 10.0


# **************************************************************************************


def test_get_modified_julian_date():
    assert get_modified_julian_date(date) == 59348.0


# **************************************************************************************


def test_get_modified_julian_date_as_parts():
    MJD, seconds_of_day = get_modified_julian_date_as_parts(date)
    assert MJD == 59348.0
    assert seconds_of_day == 0.0

    MJD, seconds_of_day = get_modified_julian_date_as_parts(
        datetime(2021, 5, 14, 12, 0, 0, 0, tzinfo=timezone.utc)
    )
    assert MJD == 59348.0
    assert seconds_of_day == 43200.0


# **************************************************************************************


def test_get_greenwich_sidereal_time():
    assert get_greenwich_sidereal_time(date) == 15.463990399019053
    assert get_greenwich_sidereal_time(date, 1.0) == 15.464268937327109


# **************************************************************************************


def test_get_local_sidereal_time():
    assert (
        get_local_sidereal_time(
            date,
            longitude,
        )
        == 5.099450799019053
    )


# **************************************************************************************


def test_universal_time():
    assert get_universal_time(date) == 0.000029055041041305996


# **************************************************************************************


def test_convert_local_sidereal_time_to_greenwich_sidereal_time():
    LST = get_local_sidereal_time(date, longitude)
    GST = convert_local_sidereal_time_to_greenwich_sidereal_time(LST, observer)
    assert GST == 15.463990399019053


# **************************************************************************************


def test_convert_greenwich_sidereal_time_to_universal_time():
    d = datetime(2021, 5, 14, 23, 30, 0, 0)
    GST = get_greenwich_sidereal_time(d)
    UTC = convert_greenwich_sidereal_time_to_universal_coordinate_time(d, GST)
    assert UTC.year == d.year
    assert UTC.month == d.month
    assert UTC.day == d.day
    assert UTC.hour == d.hour
    assert UTC.minute == d.minute
    assert UTC.second == d.second


# **************************************************************************************
