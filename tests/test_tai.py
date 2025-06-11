# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.tai import IERS_LEAP_SECONDS

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
