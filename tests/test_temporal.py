from datetime import datetime

from src.celerity.temporal import (
    get_greenwhich_sidereal_time,
    get_julian_date,
    get_local_sidereal_time,
)

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094


def test_get_julian_date():
    assert get_julian_date(date) == 2459348.5


def test_get_greenwhich_sidereal_time():
    assert get_greenwhich_sidereal_time(date) == 15.463990399019053


def test_get_local_sidereal_time():
    assert (
        get_local_sidereal_time(
            date,
            longitude,
        )
        == 5.099450799019053
    )
