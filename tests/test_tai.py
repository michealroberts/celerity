# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from datetime import datetime, timedelta, timezone

from celerity.tai import (
    IERS_LEAP_SECONDS,
    IERS_TAI_UTC_DRIFT,
    get_tai_utc_offset,
    get_tt_utc_offset,
)

# **************************************************************************************

# The TAI-UTC offset (in seconds) at the introduction of the current UTC system on
# 1972-01-01, before any leap second had been inserted:
INITIAL_TAI_UTC_OFFSET: float = 10.0

# **************************************************************************************

# The number of positive leap seconds inserted since 1972-01-01, as announced in IERS
# Bulletin C up to and including the insertion at the end of 2016-12-31:
NUMBER_OF_LEAP_SECONDS: int = 27

# **************************************************************************************

# The TT-TAI offset (in seconds), which is a fixed constant by definition:
TT_TAI_OFFSET: float = 32.184

# **************************************************************************************

# The dates on which a leap second came into force, paired with the TAI-UTC offset (in
# seconds) in force from that instant, as published in IERS Bulletin C. The offset
# immediately before each date is one second smaller:
LEAP_SECOND_BOUNDARIES: list[tuple[datetime, float]] = [
    (datetime(1980, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 19.0),
    (datetime(1999, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 32.0),
    (datetime(2006, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 33.0),
    (datetime(2009, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 34.0),
    (datetime(2012, 7, 1, 0, 0, 0, tzinfo=timezone.utc), 35.0),
    (datetime(2015, 7, 1, 0, 0, 0, tzinfo=timezone.utc), 36.0),
    (datetime(2017, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 37.0),
]

# **************************************************************************************


class TestIERSLeapSeconds(unittest.TestCase):
    def test_leap_seconds_count(self) -> None:
        # The initial entry for 1972-01-01 plus one entry per leap second inserted
        # since:
        self.assertEqual(len(IERS_LEAP_SECONDS), NUMBER_OF_LEAP_SECONDS + 1)

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

    def test_leap_seconds_at_midnight_on_the_first(self) -> None:
        # Every leap second comes into force at 00:00:00 UTC on the first of the month:
        for entry in IERS_LEAP_SECONDS:
            self.assertEqual(entry["at"].day, 1)
            self.assertEqual(entry["at"].hour, 0)
            self.assertEqual(entry["at"].minute, 0)
            self.assertEqual(entry["at"].second, 0)
            self.assertEqual(entry["at"].microsecond, 0)
            self.assertEqual(entry["at"].tzinfo, timezone.utc)

    def test_leap_seconds_start_at_initial_offset(self) -> None:
        # The first entry is the introduction of the current UTC system on 1972-01-01:
        self.assertEqual(
            IERS_LEAP_SECONDS[0]["at"],
            datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(IERS_LEAP_SECONDS[0]["offset"], INITIAL_TAI_UTC_OFFSET)

    def test_leap_seconds_increment_by_one_second(self) -> None:
        # Every leap second inserted to date has been positive, so each successive entry
        # must carry an offset exactly one second larger than the entry before it:
        for i in range(1, len(IERS_LEAP_SECONDS)):
            self.assertEqual(
                IERS_LEAP_SECONDS[i]["offset"] - IERS_LEAP_SECONDS[i - 1]["offset"],
                1.0,
                f"Leap second at {IERS_LEAP_SECONDS[i]['at']} is not a one second step",
            )

    def test_leap_seconds_end_at_current_offset(self) -> None:
        # The most recent leap second, inserted at the end of 2016-12-31, brought the
        # TAI-UTC offset to 37 seconds:
        self.assertEqual(
            IERS_LEAP_SECONDS[-1]["at"],
            datetime(2017, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            IERS_LEAP_SECONDS[-1]["offset"],
            INITIAL_TAI_UTC_OFFSET + NUMBER_OF_LEAP_SECONDS,
        )

    def test_leap_seconds_match_iers_bulletin_c(self) -> None:
        # The complete history of TAI-UTC as announced in IERS Bulletin C, with the year
        # and month from which each offset (in seconds) was in force:
        history = [
            (1972, 1, 10.0),
            (1972, 7, 11.0),
            (1973, 1, 12.0),
            (1974, 1, 13.0),
            (1975, 1, 14.0),
            (1976, 1, 15.0),
            (1977, 1, 16.0),
            (1978, 1, 17.0),
            (1979, 1, 18.0),
            (1980, 1, 19.0),
            (1981, 7, 20.0),
            (1982, 7, 21.0),
            (1983, 7, 22.0),
            (1985, 7, 23.0),
            (1988, 1, 24.0),
            (1990, 1, 25.0),
            (1991, 1, 26.0),
            (1992, 7, 27.0),
            (1993, 7, 28.0),
            (1994, 7, 29.0),
            (1996, 1, 30.0),
            (1997, 7, 31.0),
            (1999, 1, 32.0),
            (2006, 1, 33.0),
            (2009, 1, 34.0),
            (2012, 7, 35.0),
            (2015, 7, 36.0),
            (2017, 1, 37.0),
        ]

        self.assertEqual(len(IERS_LEAP_SECONDS), len(history))

        for entry, (year, month, offset) in zip(IERS_LEAP_SECONDS, history):
            self.assertEqual(
                entry["at"],
                datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc),
            )
            self.assertEqual(entry["offset"], offset)


# **************************************************************************************


class TestTAIUTCOffset(unittest.TestCase):
    def test_before_1960(self) -> None:
        # UTC did not exist before 1960-01-01, so no offset is defined:
        when = datetime(1959, 12, 31, 23, 59, 59)
        self.assertEqual(get_tai_utc_offset(when), 0.0)

    def test_before_1972(self) -> None:
        # Before leap seconds the offset drifted linearly; on 1970-01-01 it was about
        # 8.000082 seconds (ERFA dat, pyerfa 2.0.1.5):
        when = datetime(1970, 1, 1, 0, 0, 0)
        self.assertAlmostEqual(get_tai_utc_offset(when), 8.000082, places=9)

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
        # 1999-06-01 12:00 UTC should have offset 32:
        when = datetime(1999, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 32.0)

    def test_mid_year_offsets(self) -> None:
        # The offset in force on the first of June in years spanning the leap second
        # era, as published in IERS Bulletin C:
        self.assertEqual(get_tai_utc_offset(datetime(1980, 6, 1)), 19.0)
        self.assertEqual(get_tai_utc_offset(datetime(1990, 6, 1)), 25.0)
        self.assertEqual(get_tai_utc_offset(datetime(2000, 6, 1)), 32.0)
        self.assertEqual(get_tai_utc_offset(datetime(2010, 6, 1)), 34.0)
        self.assertEqual(get_tai_utc_offset(datetime(2016, 6, 1)), 36.0)
        self.assertEqual(get_tai_utc_offset(datetime(2020, 6, 1)), 37.0)

    def test_immediately_before_and_after_leap_seconds(self) -> None:
        # The offset steps up by exactly one second at the instant each leap second
        # comes into force, so the last second of the preceding day still carries the
        # old value:
        for at, offset in LEAP_SECOND_BOUNDARIES:
            before = at - timedelta(seconds=1)
            self.assertEqual(
                get_tai_utc_offset(before),
                offset - 1.0,
                f"Offset immediately before the leap second at {at} is incorrect",
            )
            self.assertEqual(
                get_tai_utc_offset(at),
                offset,
                f"Offset at the leap second at {at} is incorrect",
            )
            self.assertEqual(
                get_tai_utc_offset(at + timedelta(seconds=1)),
                offset,
                f"Offset immediately after the leap second at {at} is incorrect",
            )

    def test_exact_entry_boundaries(self) -> None:
        for entry in IERS_LEAP_SECONDS:
            when = entry["at"]
            self.assertEqual(get_tai_utc_offset(when), entry["offset"])

    def test_naive_datetime(self) -> None:
        # naive datetime treated as UTC
        when = datetime(2012, 7, 1, 0, 0, 0)
        self.assertEqual(get_tai_utc_offset(when), 35.0)

    def test_aware_datetime_in_non_utc_timezone(self) -> None:
        # 2012-07-01 01:59:59 in UTC+2 is 2012-06-30 23:59:59 UTC, so the leap second
        # inserted at the end of 2012-06-30 has not yet come into force:
        when = datetime(2012, 7, 1, 1, 59, 59, tzinfo=timezone(timedelta(hours=2)))
        self.assertEqual(get_tai_utc_offset(when), 34.0)

        # One second later, 2012-07-01 00:00:00 UTC, it has:
        when = datetime(2012, 7, 1, 2, 0, 0, tzinfo=timezone(timedelta(hours=2)))
        self.assertEqual(get_tai_utc_offset(when), 35.0)

    def test_post_2016(self) -> None:
        # After last known leap insertion
        when = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tai_utc_offset(when), 37.0)


# **************************************************************************************


class TestTTUTCOffset(unittest.TestCase):
    def test_before_1972(self) -> None:
        # Before leap seconds the TAI-UTC offset drifted; on 1970-01-01 it was about
        # 8.000082 seconds, so TT-UTC was about 40.184082 seconds:
        when = datetime(1970, 1, 1, 0, 0, 0)
        self.assertAlmostEqual(
            get_tt_utc_offset(when), 8.000082 + TT_TAI_OFFSET, places=9
        )

    def test_at_introduction_1972(self) -> None:
        when = datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 10.0 + TT_TAI_OFFSET)

    def test_just_before_first_leap(self) -> None:
        when = datetime(1972, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 10.0 + TT_TAI_OFFSET)

    def test_at_first_leap_effective(self) -> None:
        when = datetime(1972, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 11.0 + TT_TAI_OFFSET)

    def test_after_several_leaps(self) -> None:
        when = datetime(1999, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 32.0 + TT_TAI_OFFSET)

    def test_immediately_before_and_after_leap_seconds(self) -> None:
        for at, offset in LEAP_SECOND_BOUNDARIES:
            before = at - timedelta(seconds=1)
            self.assertEqual(get_tt_utc_offset(before), offset - 1.0 + TT_TAI_OFFSET)
            self.assertEqual(get_tt_utc_offset(at), offset + TT_TAI_OFFSET)

    def test_exact_entry_boundaries(self) -> None:
        for entry in IERS_LEAP_SECONDS:
            when = entry["at"]
            self.assertEqual(get_tt_utc_offset(when), entry["offset"] + TT_TAI_OFFSET)

    def test_naive_datetime(self) -> None:
        when = datetime(2012, 7, 1, 0, 0, 0)
        self.assertEqual(get_tt_utc_offset(when), 35.0 + TT_TAI_OFFSET)

    def test_post_2016(self) -> None:
        when = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(get_tt_utc_offset(when), 37.0 + TT_TAI_OFFSET)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()


# **************************************************************************************


class TestIERSTAIUTCDrift(unittest.TestCase):
    def test_drift_count(self) -> None:
        # There are fourteen expressions between 1960-01-01 and 1968-02-01:
        self.assertEqual(len(IERS_TAI_UTC_DRIFT), 14)

    def test_drift_ordered(self) -> None:
        for earlier, later in zip(IERS_TAI_UTC_DRIFT, IERS_TAI_UTC_DRIFT[1:]):
            self.assertLess(earlier["at"], later["at"])

    def test_drift_spans_1960_to_1968(self) -> None:
        self.assertEqual(
            IERS_TAI_UTC_DRIFT[0]["at"], datetime(1960, 1, 1, tzinfo=timezone.utc)
        )
        self.assertEqual(
            IERS_TAI_UTC_DRIFT[-1]["at"], datetime(1968, 2, 1, tzinfo=timezone.utc)
        )

    def test_drift_rates_are_small_and_positive(self) -> None:
        # The frequency offsets applied to UTC were between 1 and 3 milliseconds per
        # day:
        for entry in IERS_TAI_UTC_DRIFT:
            self.assertGreater(entry["rate"], 0.001)
            self.assertLess(entry["rate"], 0.003)

    def test_matches_erfa(self) -> None:
        # Reference values from ERFA dat (pyerfa 2.0.1.5) across the drift era, each
        # taken at the given fraction of the day:
        for when, expected in (
            (datetime(1960, 1, 1, tzinfo=timezone.utc) + timedelta(days=0.0), 0.943482),
            (datetime(1961, 1, 1, tzinfo=timezone.utc) + timedelta(days=0.0), 1.422818),
            (
                datetime(1961, 7, 31, tzinfo=timezone.utc) + timedelta(days=0.999),
                1.6975687040000045,
            ),
            (
                datetime(1961, 8, 1, tzinfo=timezone.utc) + timedelta(days=0.0),
                1.6475700000000002,
            ),
            (
                datetime(1962, 6, 15, tzinfo=timezone.utc) + timedelta(days=0.5),
                2.0317476,
            ),
            (
                datetime(1963, 11, 1, tzinfo=timezone.utc) + timedelta(days=0.0),
                2.6972788,
            ),
            (
                datetime(1964, 2, 29, tzinfo=timezone.utc) + timedelta(days=0.25),
                2.842582,
            ),
            (
                datetime(1965, 8, 15, tzinfo=timezone.utc) + timedelta(days=0.75),
                4.033998,
            ),
            (datetime(1966, 1, 1, tzinfo=timezone.utc) + timedelta(days=0.0), 4.31317),
            (
                datetime(1967, 6, 30, tzinfo=timezone.utc) + timedelta(days=0.5),
                5.727106,
            ),
            (datetime(1968, 2, 1, tzinfo=timezone.utc) + timedelta(days=0.0), 6.185682),
            (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(days=0.0), 8.000082),
            (
                datetime(1971, 12, 31, tzinfo=timezone.utc) + timedelta(days=0.999988),
                9.892241968896009,
            ),
        ):
            self.assertAlmostEqual(get_tai_utc_offset(when), expected, places=9)

    def test_offset_grows_within_an_expression(self) -> None:
        # Within one expression the offset increases at the stated rate, so a day later
        # it is larger by that rate:
        earlier = get_tai_utc_offset(datetime(1962, 3, 1, tzinfo=timezone.utc))
        later = get_tai_utc_offset(datetime(1962, 3, 2, tzinfo=timezone.utc))
        self.assertAlmostEqual(later - earlier, 0.0011232, places=12)

    def test_reaches_the_initial_leap_second_offset(self) -> None:
        # At the end of 1971 the drifted offset was just under 10 seconds, and the
        # leap second system then set it to exactly 10 seconds:
        before = get_tai_utc_offset(
            datetime(1971, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        )
        after = get_tai_utc_offset(datetime(1972, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
        self.assertGreater(before, 9.8)
        self.assertLess(before, 10.0)
        self.assertEqual(after, 10.0)

    def test_treats_naive_datetime_as_utc(self) -> None:
        self.assertEqual(
            get_tai_utc_offset(datetime(1965, 5, 14, 0, 0, 0)),
            get_tai_utc_offset(
                datetime(1965, 5, 14, 2, 0, 0, tzinfo=timezone(timedelta(hours=2)))
            ),
        )


# **************************************************************************************
