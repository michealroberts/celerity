from datetime import datetime, timedelta, timezone
from math import cos, radians

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

observer: GeographicCoordinate = {"latitude": latitude, "longitude": longitude}


def test_get_correction_to_equatorial_for_aberration():
    t = get_correction_to_equatorial_for_aberration(date, betelgeuse)
    ra = t["ra"] + betelgeuse["ra"]
    dec = t["dec"] + betelgeuse["dec"]
    assert ra == 88.78837273584286
    assert dec == 7.4061086762102715


# **************************************************************************************


def test_get_correction_to_equatorial_for_aberration_is_at_most_the_constant_of_aberration():
    # Annual aberration never exceeds the constant of aberration, about 20.5 arcseconds:
    for target in (betelgeuse, {"ra": 0.0, "dec": 0.0}, {"ra": 180.0, "dec": -60.0}):
        correction = get_correction_to_equatorial_for_aberration(date, target)
        # The shift on the sky scales the right ascension component by cos(dec):
        shift = (
            (correction["ra"] * cos(radians(target["dec"]))) ** 2
            + correction["dec"] ** 2
        ) ** 0.5 * 3600
        assert 0.0 < shift < 20.6


# **************************************************************************************


def test_get_correction_to_equatorial_for_aberration_wraps_right_ascension():
    # A target just below 360 degrees may be displaced through 0 degrees, and the
    # correction must be the small step rather than a full turn:
    correction = get_correction_to_equatorial_for_aberration(
        date, {"ra": 359.999, "dec": 0.0}
    )
    assert -1.0 < correction["ra"] < 1.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_aberration_near_the_pole():
    # Close to the celestial pole the correction stays finite and the displaced
    # declination stays within range:
    target: EquatorialCoordinate = {"ra": 37.9, "dec": 89.99}
    correction = get_correction_to_equatorial_for_aberration(date, target)
    assert -180.0 <= correction["ra"] < 180.0
    assert -90.0 <= target["dec"] + correction["dec"] <= 90.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_aberration_treats_naive_datetime_as_utc():
    assert get_correction_to_equatorial_for_aberration(
        date, betelgeuse
    ) == get_correction_to_equatorial_for_aberration(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2))),
        betelgeuse,
    )


# **************************************************************************************
