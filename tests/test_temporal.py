# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime, timezone

from src.celerity.common import GeographicCoordinate
from src.celerity.temporal import (
    convert_greenwich_sidereal_time_to_universal_coordinate_time,
    convert_local_sidereal_time_to_greenwich_sidereal_time,
    get_greenwich_sidereal_time,
    get_julian_date,
    get_local_sidereal_time,
    get_modified_julian_date,
    get_modified_julian_date_as_parts,
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

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}

# **************************************************************************************


def test_get_julian_date():
    assert get_julian_date(date) == 2459348.5


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
    assert get_universal_time(date) == 0.000028334646537240785


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
