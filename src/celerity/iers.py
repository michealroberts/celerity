# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from urllib import request

# **************************************************************************************

IERS_DUT1_URL = "https://datacenter.iers.org/data/latestVersion/bulletinA.txt"

# **************************************************************************************


def fetch_iers_rapid_service_data(url: str) -> str:
    with request.urlopen(url) as response:
        # Assume UTF-8 or ASCII text in the response:
        raw = response.read()
    return raw.decode("utf-8", errors="ignore")


# **************************************************************************************
