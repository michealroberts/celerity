# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timezone
from math import isclose

from src.celerity.common import GeographicCoordinate
from src.celerity.temporal import Time

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# **************************************************************************************

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

# **************************************************************************************

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}

# **************************************************************************************

T = Time(date)

# **************************************************************************************


def test_is_datetime_instance():
    assert isinstance(T, datetime)
    assert isinstance(T, Time)


# **************************************************************************************


def test_isoformat():
    assert T.isoformat() == "2021-05-14T00:00:00+00:00"


# **************************************************************************************


def test_timezone():
    assert T.tzname() == "UTC"


# **************************************************************************************


def test_universal_time():
    # Assert UT is close to 0:
    assert isclose(T.UT, 0.0, abs_tol=0.0001)


# **************************************************************************************


def test_international_atomic_time():
    tai = T.TAI
    utc = T.when.astimezone(timezone.utc)
    difference = (tai.replace(tzinfo=None) - utc.replace(tzinfo=None)).total_seconds()
    assert isclose(difference, 37.0, abs_tol=1e-6)
    assert isclose((tai - utc).total_seconds(), 0.0, abs_tol=1e-6)


# **************************************************************************************
def test_get_julian_date():
    assert T.JD == 2459348.5


# **************************************************************************************


def test_get_modified_julian_date():
    assert T.MJD == 59348.0


# **************************************************************************************


def test_get_greenwich_sidereal_time():
    assert T.GST == 15.463990399019053


# **************************************************************************************


def test_get_local_sidereal_time():
    assert T.LST(longitude) == 5.099450799019053


# **************************************************************************************
