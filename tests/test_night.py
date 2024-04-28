from datetime import datetime, timezone

from src.celerity.common import GeographicCoordinate
from src.celerity.night import (
    NightPhase,
    get_night,
    get_night_phase,
    get_solar_transit,
    is_night,
)

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# For testing, we will fix the latitude to be the Isles of Scilly, Cornwall, UK.
latitude: float = 49.914425

# For testing, we will fix the longitude to be the Isles of Scilly, Cornwall, UK.
longitude: float = -6.315165

observer: GeographicCoordinate = {"lat": latitude, "lon": longitude}


def test_get_solar_transit():
    d = get_solar_transit(date, observer)
    # Rise, in UTC (BST is UTC+1 and we're expecting it to rise around 5am BST)
    assert d[0] == datetime(2021, 5, 14, 4, 46, 0, 0, tzinfo=timezone.utc)
    # Transit, in UTC:
    assert d[1] == datetime(2021, 5, 14, 12, 20, 0, 0, tzinfo=timezone.utc)
    # Set, in UTC (BST is UTC+1 and we're expecting it to set around 9pm BST)
    assert d[2] == datetime(2021, 5, 14, 19, 56, 0, 0, tzinfo=timezone.utc)

    # Civil twilight is when the Sun is 6 degrees below the horizon:
    d = get_solar_transit(date, observer, -6)
    # Rise, in UTC (BST is UTC+1 and we're expecting it to rise around 5am BST)
    assert d[0] == datetime(2021, 5, 14, 4, 1, 0, 0, tzinfo=timezone.utc)
    # Transit, in UTC:
    assert d[1] == datetime(2021, 5, 14, 12, 20, 0, 0, tzinfo=timezone.utc)
    # Set, in UTC (BST is UTC+1 and we're expecting it to set around 9pm BST)
    assert d[2] == datetime(2021, 5, 14, 20, 41, 0, 0, tzinfo=timezone.utc)

    # Astronomical twilight is when the Sun is 18 degrees below the horizon:
    d = get_solar_transit(date, observer, -18)
    # Rise, in UTC (BST is UTC+1 and we're expecting it to rise around 5am BST)
    assert d[0] == datetime(2021, 5, 14, 2, 1, 0, 0, tzinfo=timezone.utc)
    # Transit, in UTC:
    assert d[1] == datetime(2021, 5, 14, 12, 20, 0, 0, tzinfo=timezone.utc)
    # Set, in UTC (BST is UTC+1 and we're expecting it to set around 9pm BST)
    assert d[2] == datetime(2021, 5, 14, 22, 43, 0, 0, tzinfo=timezone.utc)


def test_get_night():
    d = get_night(date, observer)
    assert d["start"] == datetime(2021, 5, 14, 19, 56, 0, 0, tzinfo=timezone.utc)
    assert d["end"] == datetime(2021, 5, 15, 4, 45, 0, 0, tzinfo=timezone.utc)


def test_is_night():
    # At 2am UTC on the specified date, it should be night:
    date = datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone.utc)
    n = is_night(date, observer)
    assert n is True

    # At 9am UTC on the specified date, it should be day:
    date = datetime(2021, 5, 14, 9, 0, 0, 0, tzinfo=timezone.utc)
    n = is_night(date, observer)
    assert n is False

    # At 6pm UTC on the specified date, it should be day:
    date = datetime(2021, 5, 14, 18, 0, 0, 0, tzinfo=timezone.utc)
    n = is_night(date, observer)
    assert n is False

    # At 10pm UTC on the specified date, it should be night:
    date = datetime(2021, 5, 14, 22, 0, 0, 0, tzinfo=timezone.utc)
    n = is_night(date, observer)
    assert n is True


def test_get_night_phase():
    # If the Sun's altitude is less than -18 degrees, then it is night:
    altitude = -18
    n = get_night_phase(altitude)
    assert n == NightPhase.NIGHT

    # If the Sun's altitude is between -18 and -12 degrees, then it is
    # astronomical twilight:
    altitude = -12
    n = get_night_phase(altitude)
    assert n == NightPhase.ASTRONOMICAL_TWILIGHT

    # If the Sun's altitude is between -12 and -6 degrees, then it is nautical twilight:
    altitude = -6
    n = get_night_phase(altitude)
    assert n == NightPhase.NAUTICAL_TWILIGHT

    # If the Sun's altitude is between -6 and 0 degrees, then it is civil twilight:
    altitude = 0
    n = get_night_phase(altitude)
    assert n == NightPhase.CIVIL_TWILIGHT

    # If the Sun's altitude is greater than 0 degrees, then it is day:
    altitude = 1
    n = get_night_phase(altitude)
