# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from datetime import datetime, timedelta, timezone

from celerity.iers import (
    IERS_EOP_BASE_URL,
    MAX_CACHE_AGE_SECONDS,
    _iers_cache,
)
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

    def test_get_ut1_utc_offset_cache_hit(self) -> None:
        # Ensure we hit the cache on subsequent calls:
        _iers_cache.clear()

        when = datetime(2023, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        first = get_ut1_utc_offset(when)

        (url, cache) = next(iter(_iers_cache.items()))

        self.assertEqual(len(_iers_cache), 1)

        self.assertTrue(url.startswith(IERS_EOP_BASE_URL))
        self.assertIn("param=UT1-UTC", url)
        self.assertIn("mjd=", url)
        self.assertIn("series=", url)

        first_cached_at = cache.at
        first_cached_dut1 = float(cache.entry["dut1"])

        second = get_ut1_utc_offset(when)
        self.assertEqual(len(_iers_cache), 1)
        self.assertIn(url, _iers_cache)

        second_cached_at = _iers_cache[url].at
        second_cached_dut1 = float(_iers_cache[url].entry["dut1"])
        self.assertEqual(first_cached_at, second_cached_at)
        self.assertAlmostEqual(first, second, places=12)
        self.assertAlmostEqual(first, first_cached_dut1, places=12)
        self.assertAlmostEqual(second, second_cached_dut1, places=12)

    def test_get_ut1_utc_offset_cache_expiry(self) -> None:
        _iers_cache.clear()

        when = datetime(2023, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        first = get_ut1_utc_offset(when)
        self.assertEqual(len(_iers_cache), 1)

        (cached_url, cached_record) = next(iter(_iers_cache.items()))
        original_at = cached_record.at

        # Force-expire the cache entry by moving its timestamp into the past:
        cached_record.at = original_at - (MAX_CACHE_AGE_SECONDS + 1)

        second = get_ut1_utc_offset(when)

        self.assertEqual(len(_iers_cache), 1)
        self.assertIn(cached_url, _iers_cache)
        self.assertGreater(_iers_cache[cached_url].at, original_at)

        # DUT1 should remain reasonable/close; we cannot guarantee identical because IERS
        # can revise recent values, but for a historical date it should normally match:
        self.assertAlmostEqual(first, second, places=6)


# **************************************************************************************
