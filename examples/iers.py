# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime, timezone

from celerity.temporal import get_ut1_utc_offset

# **************************************************************************************

if __name__ == "__main__":
    try:
        now = datetime.now(timezone.utc)
        # Fetch the IERS Rapid Service data again to demonstrate caching:
        dut1 = get_ut1_utc_offset(now)
        print(f"UT1-UTC offset at {now.isoformat()}: {dut1} seconds")

        # This should hit the cache:
        dut1 = get_ut1_utc_offset(now)
        print(f"UT1-UTC offset at {now.isoformat()}: {dut1} seconds")
    except Exception as e:
        print(f"An error occurred while getting UT1-UTC offset: {e}")

# **************************************************************************************
