# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timedelta, timezone

import pytest

from src.celerity.earth import get_eccentricity_of_orbit, get_heliocentric_velocity

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)


# **************************************************************************************


def test_get_eccentricity_of_orbit():
    e = get_eccentricity_of_orbit(date)
    assert e == 0.016699647287906946


# **************************************************************************************


def test_get_heliocentric_velocity():
    v = get_heliocentric_velocity(date)

    # The reference velocity (in metres per second) is the heliocentric velocity of the
    # Earth from ERFA epv00 (pyerfa 2.0.1.5), rotated from the ICRS to the mean equator
    # and equinox of date with the rp matrix of bp06, for 2021-05-14 00:00:00 UTC:
    assert v["x"] == pytest.approx(23454.07861725801, abs=0.2)
    assert v["y"] == pytest.approx(-16386.698562063568, abs=0.2)
    assert v["z"] == pytest.approx(-7104.714572506208, abs=0.2)

    # A naive datetime is treated as UTC, so it must agree with the same instant given in
    # an explicit non-UTC timezone:
    assert v == get_heliocentric_velocity(
        datetime(2021, 5, 14, 2, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
    )


# **************************************************************************************
