# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime
from json import loads
from typing import TypedDict
from urllib import request

from .temporal import get_modified_julian_date_as_parts

# **************************************************************************************


class DUT1Entry(TypedDict):
    # The Modified Julian Date (MJD) of the DUT1 entry:
    mjd: float
    # The DUT1 value, e.g., UT1 - UTC (in seconds)
    dut1: float


# **************************************************************************************

IERS_DUT1_URL = "https://datacenter.iers.org/webservice/REST/eop/RestController.php"

# **************************************************************************************


def fetch_iers_rapid_service_data(url: str) -> str:
    with request.urlopen(url) as response:
        # Assume UTF-8 or ASCII text in the response:
        raw = response.read()
    return raw.decode("utf-8", errors="ignore")


# **************************************************************************************


def get_ut1_utc_offset(when: datetime) -> float:
    MJD, _ = get_modified_julian_date_as_parts(when)

    url = f"{IERS_DUT1_URL}?param=UT1-UTC&mjd={MJD}&series=Finals%20All%20IAU1980"

    dut1 = 0.0

    response = fetch_iers_rapid_service_data(url)

    data = loads(response)

    if (
        not data
        or "Value" not in data
        or "Param" not in data
        or data["Param"] != "UT1-UTC"
    ):
        raise ValueError("No valid DUT1 data found for the specified date.")

    if data["Value"] is None:
        raise ValueError("DUT1 value is None, no valid data found.")

    dut1 = data["Value"] * 0.001

    return dut1


# **************************************************************************************
