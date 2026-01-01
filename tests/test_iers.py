# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from datetime import datetime, timedelta, timezone

from celerity.temporal import get_ut1_utc_offset

# **************************************************************************************


class TestGetUT1UTCOffset(unittest.TestCase):
    """
    Test the get_ut1_utc_offset function.
    """

    def test_get_ut1_utc_offset(self) -> None:
        when = datetime(2023, 5, 15, 0, 0, 0, tzinfo=timezone.utc)
        dut1 = get_ut1_utc_offset(when)
        self.assertAlmostEqual(dut1, -41.767 * 0.001, places=3)

    def test_get_ut1_utc_offset_seconds_of_day(self) -> None:
        when = datetime(2023, 5, 15, 12, 30, 30, tzinfo=timezone.utc)
        dut1 = get_ut1_utc_offset(when)
        self.assertAlmostEqual(dut1, -41.767 * 0.001, places=3)

    def test_get_ut1_utc_offset_older_date(self) -> None:
        when = datetime(2000, 5, 15, 12, 0, 0, tzinfo=timezone.utc)
        dut1 = get_ut1_utc_offset(when)
        self.assertAlmostEqual(dut1, 0.2281735, places=3)

    def test_get_ut1_utc_offset_future_date_invalid(self) -> None:
        now = datetime.now(timezone.utc)
        # Assuming the DUT1 value for 10 years in the future is similar to current values:
        when = now + timedelta(days=365 * 10)

        # A date in the future will always throw a ValueError:
        with self.assertRaises(ValueError):
            get_ut1_utc_offset(when)

    def test_get_ut1_utc_offset_invalid_date(self) -> None:
        # An invalid date (e.g., before the IERS data starts) will throw a ValueError:
        with self.assertRaises(ValueError):
            get_ut1_utc_offset(datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc))


# **************************************************************************************
