# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from datetime import datetime, timezone

from celerity.tai import IERS_LEAP_SECONDS, get_tai_utc_offset, get_tt_utc_offset

# **************************************************************************************


class TestIERSLeapSeconds(unittest.TestCase):
    def test_leap_seconds_count(self) -> None:
        # There are 27 leap second adjustments known as of June 2025 (as per IERS):
        self.assertEqual(len(IERS_LEAP_SECONDS), 27)

    def test_leap_seconds_ordered(self) -> None:
        # Ensure the leap seconds are ordered by date:
        for i in range(1, len(IERS_LEAP_SECONDS)):
            self.assertLess(
                IERS_LEAP_SECONDS[i - 1]["at"],
                IERS_LEAP_SECONDS[i]["at"],
            )

    def test_leap_seconds_at_january_july(self) -> None:
        # Also test that the datetime is either a January 1st or July 1st:
        for i in range(1, len(IERS_LEAP_SECONDS)):
            self.assertIn(
                IERS_LEAP_SECONDS[i]["at"].month,
                [1, 7],
                f"Leap second at {IERS_LEAP_SECONDS[i]['at']} is not in January or July",
            )


# **************************************************************************************


class TestTAIUTCOffset(unittest.TestCase):
    def test_before_1972(self) -> None:
        when = datetime(1970, 1, 1, 0, 0, 0)
        self.assertEqual(get_tai_utc_offset(when), 0.0)

    def test_at_introduction_1972(self) -> None:
        when = datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 10.0)

    def test_just_before_first_leap(self) -> None:
        # 1972-06-30 23:59:59 UTC: still offset 10:
        when = datetime(1972, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 10.0)

    def test_at_first_leap_effective(self) -> None:
        # 1972-07-01 00:00:00 UTC: offset becomes 11:
        when = datetime(1972, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 11.0)

    def test_after_several_leaps(self) -> None:
        # 1999-06-01 12:00 UTC should have offset 31:
        when = datetime(1999, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 31.0)

    def test_exact_entry_boundaries(self) -> None:
        for entry in IERS_LEAP_SECONDS:
            when = entry["at"]
            self.assertEqual(get_tai_utc_offset(when), entry["offset"])

    def test_naive_datetime(self) -> None:
        # naive datetime treated as UTC
        when = datetime(2012, 7, 1, 0, 0, 0)
        self.assertEqual(get_tai_utc_offset(when), 34.0)

    def test_post_2016(self) -> None:
        # After last known leap insertion
        when = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 37.0)


# **************************************************************************************


class TestTTUTCOffset(unittest.TestCase):
    def test_before_1972(self) -> None:
        when = datetime(1970, 1, 1, 0, 0, 0)
        self.assertEqual(get_tt_utc_offset(when), 0.0 + 32.184)

    def test_at_introduction_1972(self) -> None:
        when = datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 10.0 + 32.184)

    def test_just_before_first_leap(self) -> None:
        when = datetime(1972, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 10.0 + 32.184)

    def test_at_first_leap_effective(self) -> None:
        when = datetime(1972, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 11.0 + 32.184)

    def test_after_several_leaps(self) -> None:
        when = datetime(1999, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 31.0 + 32.184)

    def test_exact_entry_boundaries(self) -> None:
        for entry in IERS_LEAP_SECONDS:
            when = entry["at"]
            self.assertEqual(get_tt_utc_offset(when), entry["offset"] + 32.184)

    def test_naive_datetime(self) -> None:
        when = datetime(2012, 7, 1, 0, 0, 0)
        self.assertEqual(get_tt_utc_offset(when), 34.0 + 32.184)

    def test_post_2016(self) -> None:
        when = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 37.0 + 32.184)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
