from datetime import datetime

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.coordinates import convert_equatorial_to_horizontal
from src.celerity.refraction import get_correction_to_horizontal_for_refraction

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}


def test_get_correction_to_horizontal_for_refraction():
    t = convert_equatorial_to_horizontal(date, observer, betelgeuse)
    assert t["az"] == 134.44877920325158
    assert t["alt"] == 72.78539444063765
    t = get_correction_to_horizontal_for_refraction(t)
    assert t["az"] == 134.44877920325158
    assert t["alt"] >= 72.79061860032508
    assert t["alt"] <= 73.0
