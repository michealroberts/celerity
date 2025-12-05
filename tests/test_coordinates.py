# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************


from datetime import datetime, timezone
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
    target = get_correction_to_equatorial(date, betelgeuse)
    assert target["ra"] == 88.53030813147811
    assert target["dec"] == 7.447242478781279


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
