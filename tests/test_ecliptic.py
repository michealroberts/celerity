# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime

from src.celerity.ecliptic import get_true_obliquity_of_the_ecliptic

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0)

# **************************************************************************************


def test_get_true_obliquity_of_the_ecliptic():
    ε = get_true_obliquity_of_the_ecliptic(date)
    assert ε == 23.437270315275185


# **************************************************************************************
