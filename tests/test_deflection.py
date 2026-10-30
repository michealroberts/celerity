# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from math import cos, radians

from src.celerity.common import EquatorialCoordinate
from src.celerity.deflection import (
    LIGHT_DEFLECTION_LIMIT,
    get_correction_to_equatorial_for_light_deflection,
)

# **************************************************************************************

# For testing we need to specify a date because most calculations are differential
# w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# **************************************************************************************

# On the test date the Sun is at about 50.7 degrees right ascension and 18.5 degrees
# declination, so the anti-solar point is at about 230.7 degrees and -18.5 degrees:
sun: EquatorialCoordinate = {"ra": 50.68, "dec": 18.54}

# **************************************************************************************

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

# **************************************************************************************


def get_shift_in_arcseconds(
    target: EquatorialCoordinate, correction: EquatorialCoordinate
) -> float:
    # The shift on the sky scales the right ascension component by cos(dec):
    return (
        (correction["ra"] * cos(radians(target["dec"]))) ** 2 + correction["dec"] ** 2
    ) ** 0.5 * 3600


# **************************************************************************************


def test_light_deflection_limit():
    assert LIGHT_DEFLECTION_LIMIT == 1e-6


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_betelgeuse():
    correction = get_correction_to_equatorial_for_light_deflection(date, betelgeuse)
    assert correction["ra"] == 3.0342090155954793e-06
    assert correction["dec"] == -1.1422177408348944e-06


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_vanishes_at_the_anti_solar_point():
    target: EquatorialCoordinate = {"ra": sun["ra"] + 180.0, "dec": -sun["dec"]}
    correction = get_correction_to_equatorial_for_light_deflection(date, target)
    assert get_shift_in_arcseconds(target, correction) < 0.0001


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_is_about_4_mas_at_90_degrees():
    # At 90 degrees from the Sun the deflection is the Schwarzschild radius of the Sun
    # over the Earth's distance, about 4.07 milliarcseconds at one astronomical unit:
    target: EquatorialCoordinate = {"ra": sun["ra"] + 90.0, "dec": 0.0}
    correction = get_correction_to_equatorial_for_light_deflection(date, target)
    assert 0.0038 < get_shift_in_arcseconds(target, correction) < 0.0044


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_grows_toward_the_sun():
    # The deflection scales as the cotangent of half the elongation, so a target 20
    # degrees from the Sun is deflected about 23 milliarcseconds:
    target: EquatorialCoordinate = {"ra": sun["ra"] + 20.0, "dec": sun["dec"]}
    correction = get_correction_to_equatorial_for_light_deflection(date, target)
    assert 0.020 < get_shift_in_arcseconds(target, correction) < 0.026


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_is_away_from_the_sun():
    # A target east of the Sun on the equator is pushed further east:
    target: EquatorialCoordinate = {"ra": sun["ra"] + 30.0, "dec": sun["dec"]}
    correction = get_correction_to_equatorial_for_light_deflection(date, target)
    assert correction["ra"] > 0.0

    # And a target west of the Sun is pushed further west:
    target = {"ra": sun["ra"] - 30.0, "dec": sun["dec"]}
    correction = get_correction_to_equatorial_for_light_deflection(date, target)
    assert correction["ra"] < 0.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_is_finite_at_the_sun():
    # A target in the direction of the Sun is held at the limiting deflection rather
    # than diverging:
    correction = get_correction_to_equatorial_for_light_deflection(date, sun)
    assert get_shift_in_arcseconds(sun, correction) < 10.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_wraps_right_ascension():
    correction = get_correction_to_equatorial_for_light_deflection(
        date, {"ra": 359.999999, "dec": 0.0}
    )
    assert -1.0 < correction["ra"] < 1.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_near_the_pole():
    target: EquatorialCoordinate = {"ra": 37.9, "dec": 89.99}
    correction = get_correction_to_equatorial_for_light_deflection(date, target)
    assert -180.0 <= correction["ra"] < 180.0
    assert -90.0 <= target["dec"] + correction["dec"] <= 90.0


# **************************************************************************************


def test_get_correction_to_equatorial_for_light_deflection_treats_naive_datetime_as_utc():
    assert get_correction_to_equatorial_for_light_deflection(
        datetime(2021, 5, 14, 0, 0, 0, 0), betelgeuse
    ) == get_correction_to_equatorial_for_light_deflection(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2))),
        betelgeuse,
    )


# **************************************************************************************
