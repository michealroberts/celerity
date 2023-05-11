from datetime import datetime

from src.celerity.aberration import get_correction_to_equatorial_for_aberration
from src.celerity.common import EquatorialCoordinate, GeographicCoordinate

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}


def test_get_correction_to_equatorial_for_aberration():
    t = get_correction_to_equatorial_for_aberration(date, betelgeuse)
    ra = t["ra"] + betelgeuse["ra"]
    dec = t["dec"] + betelgeuse["dec"]
    assert ra == 88.78837512114575
    assert dec == 7.406109156062398
