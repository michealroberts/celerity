# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timezone

from src.celerity.common import EquatorialCoordinate, GeographicCoordinate
from src.celerity.nutation import (
    get_correction_to_equatorial_for_nutation,
    get_nutation_in_longitude,
)

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# **************************************************************************************

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# **************************************************************************************

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

# **************************************************************************************

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

# **************************************************************************************

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}

# **************************************************************************************

def test_get_nutation_in_longitude():
    Δψ = get_nutation_in_longitude(date)
    assert Δψ == -0.004878239753472116

# **************************************************************************************

def test_get_correction_to_equatorial_for_nutation():
    t = get_correction_to_equatorial_for_nutation(date, betelgeuse)
    ra = t["ra"] + betelgeuse["ra"]
    dec = t["dec"] + betelgeuse["dec"]
    assert ra == 88.52194751991885
    assert dec == 7.448166948222143

# **************************************************************************************