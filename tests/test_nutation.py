from datetime import datetime

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.nutation import get_correction_to_equatorial_for_nutation

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}


def test_get_correction_to_equatorial_for_nutation():
    t = get_correction_to_equatorial_for_nutation(date, betelgeuse)
    ra = t["ra"] + betelgeuse["ra"]
    dec = t["dec"] + betelgeuse["dec"]
    assert ra == 88.52194751991885
    assert dec == 7.448166948222143
