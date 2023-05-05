from datetime import datetime

from src.celerity.epoch import get_number_of_fractional_days_since_j2000

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)


def test_get_number_of_fractional_days_since_j2000():
    d = get_number_of_fractional_days_since_j2000(date)
    assert d == 7803.5
