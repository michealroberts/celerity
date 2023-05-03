from datetime import datetime
from typing import TypedDict


class EquatorialCoordinate(TypedDict):
    ra: float
    dec: float


from src.celerity.astrometry import get_hour_angle

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}


def test_get_hour_angle():
    ha = get_hour_angle(date, betelgeuse["ra"], longitude)
    assert ha == 347.6988036852858
