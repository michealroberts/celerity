from datetime import datetime

from src.celerity.temporal import get_julian_date

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)


def test_get_julian_date():
    assert get_julian_date(date) == 2459348.5
