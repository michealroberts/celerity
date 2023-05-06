from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.moon import get_mean_ecliptic_longitude_of_the_ascending_node

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}


def test_get_mean_ecliptic_longitude_of_the_ascending_node():
    Ω = get_mean_ecliptic_longitude_of_the_ascending_node(date, longitude)
    assert Ω == 71.69457220767262