from datetime import datetime

from src.celerity.earth import get_eccentricity_of_orbit

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)


def test_get_eccentricity_of_orbit():
    e = get_eccentricity_of_orbit(date)
    assert e == 0.016699647287906946
