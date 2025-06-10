# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from celerity.iers import (
    IERS_DUT1_URL,
    fetch_iers_rapid_service_data,
)

# **************************************************************************************

if __name__ == "__main__":
    try:
        # Fetch the latest IERS Rapid Service data
        data = fetch_iers_rapid_service_data(url=IERS_DUT1_URL)
        print("IERS Rapid Service Data fetched successfully.")
        print(data)
    except Exception as e:
        print(f"An error occurred while fetching IERS data: {e}")

# **************************************************************************************
