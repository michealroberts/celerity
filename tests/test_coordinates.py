# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************


from datetime import datetime, timedelta, timezone
from math import isclose

from src.celerity.common import (
    EquatorialCoordinate,
    GeographicCoordinate,
    HeliocentricSphericalCoordinate,
)
from src.celerity.coordinates import (
    convert_equatorial_to_horizontal,
    convert_heliocentric_to_equatorial,
    convert_horizontal_to_equatorial,
    get_apparent_equatorial_coordinate,
    get_correction_to_equatorial,
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

betelgeuse: EquatorialCoordinate = {
    "ra": 88.7929583,
    "dec": 7.4070639,
}

# **************************************************************************************

observer: GeographicCoordinate = {
    "latitude": latitude,
    "longitude": longitude,
}

# **************************************************************************************


def test_convert_equatorial_to_horizontal():
    horizontal = convert_equatorial_to_horizontal(date, observer, betelgeuse)
    assert horizontal["alt"] == 72.78539444063765
    assert horizontal["az"] == 134.44877920325158


# **************************************************************************************


def test_convert_horizontal_to_equatorial():
    horizontal = convert_equatorial_to_horizontal(date, observer, betelgeuse)
    equatorial = convert_horizontal_to_equatorial(date, observer, horizontal)
    assert isclose(equatorial["ra"], betelgeuse["ra"], rel_tol=1e-9)
    assert isclose(equatorial["dec"], betelgeuse["dec"], rel_tol=1e-9)


# **************************************************************************************


def test_get_correction_to_equatorial():
    # get_correction_to_equatorial mutates its input, so pass a copy to keep the
    # shared fixture intact for the other tests:
    target = get_correction_to_equatorial(
        date, EquatorialCoordinate(ra=betelgeuse["ra"], dec=betelgeuse["dec"])
    )
    assert target["ra"] == 89.07287477398826
    assert target["dec"] == 7.409028695505812


# **************************************************************************************


def test_get_apparent_equatorial_coordinate():
    j2000 = EquatorialCoordinate(ra=betelgeuse["ra"], dec=betelgeuse["dec"])

    apparent = get_apparent_equatorial_coordinate(date, j2000)
    assert apparent["ra"] == 89.07287477398826
    assert apparent["dec"] == 7.409028695505812

    # The alias must not mutate the coordinate it was given:
    assert j2000["ra"] == betelgeuse["ra"]
    assert j2000["dec"] == betelgeuse["dec"]
    assert apparent is not j2000


def test_get_correction_to_equatorial_treats_naive_datetime_as_utc():
    naive = get_correction_to_equatorial(
        datetime(2021, 5, 14, 0, 0, 0, 0),
        EquatorialCoordinate(ra=betelgeuse["ra"], dec=betelgeuse["dec"]),
    )
    aware = get_correction_to_equatorial(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2))),
        EquatorialCoordinate(ra=betelgeuse["ra"], dec=betelgeuse["dec"]),
    )
    assert naive == aware


# **************************************************************************************


def test_get_correction_to_equatorial_near_the_pole():
    # Close to the celestial pole the apparent place stays finite and within range:
    apparent = get_correction_to_equatorial(
        date, EquatorialCoordinate(ra=37.9, dec=89.99)
    )
    assert 0.0 <= apparent["ra"] < 360.0
    assert -90.0 <= apparent["dec"] <= 90.0


# **************************************************************************************


# **************************************************************************************


def test_convert_heliocentric_to_equatorial() -> None:
    venus: HeliocentricSphericalCoordinate = {
        "λ": 245.79403406596947,
        "β": 1.8937944394473665,
        "r": 0.720040,
    }

    equatorial = convert_heliocentric_to_equatorial(date, venus)

    assert isclose(equatorial["ra"], 244.248100, rel_tol=1e-6)
    assert isclose(equatorial["dec"], -19.405047, rel_tol=1e-6)


# **************************************************************************************
