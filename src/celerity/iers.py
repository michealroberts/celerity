# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from __future__ import annotations

from dataclasses import dataclass
from json import loads
from threading import Lock
from time import monotonic
from typing import Dict, TypedDict
from urllib.request import Request, urlopen

# **************************************************************************************

URL_OPEN_TIMEOUT_SECONDS = 10

# **************************************************************************************

IERS_EOP_BASE_URL = "https://datacenter.iers.org/webservice/REST/eop/RestController.php"

# **************************************************************************************


@dataclass
class IERSCache:
    at: float
    entry: DUT1Entry


# **************************************************************************************

_iers_cache_lock = Lock()

# **************************************************************************************

_iers_cache: Dict[str, IERSCache] = {}

# **************************************************************************************

MAX_CACHE_AGE_SECONDS = 6 * 60 * 60  # 6 hours

# **************************************************************************************


class DUT1Entry(TypedDict):
    # The Modified Julian Date (MJD) of the DUT1 entry:
    mjd: float
    # The DUT1 value, e.g., UT1 - UTC (in seconds)
    dut1: float


# **************************************************************************************


def fetch_iers_rapid_service_data(url: str) -> DUT1Entry:
    now = monotonic()

    with _iers_cache_lock:
        if url in _iers_cache and now - _iers_cache[url].at < MAX_CACHE_AGE_SECONDS:
            return _iers_cache[url].entry

    # Ensure we always expect to accept JSON responses, whilst also letting the server
    # know that we are a client (e.g., celerity) to avoid any potential issues with
    # server-side rate limiting or blocking:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "celerity",
        },
    )

    with urlopen(request, timeout=URL_OPEN_TIMEOUT_SECONDS) as response:
        # Assume UTF-8 or ASCII text in the response:
        raw = response.read().decode("utf-8", errors="ignore")

    # Load the JSON data from the response:
    data = loads(raw)

    # If the data is empty or does not contain the expected keys, raise an error:
    if not data or "Value" not in data or "Param" not in data:
        raise ValueError("No valid DUT1 data found for the specified date.")

    # If the DUT1 (UT1-UTC) parameter is not present, raise an error:
    if data["Param"] != "UT1-UTC":
        raise ValueError("Invalid parameter in DUT1 data, expected 'UT1-UTC'.")

    # If the DUT1 value is None, raise an error:
    if data["Value"] is None:
        raise ValueError("DUT1 value is None, no valid data found.")

    # If the MJD is None, raise an error:
    if data["MJD"] is None:
        raise ValueError("MJD is None, no valid data found.")

    entry = DUT1Entry(
        mjd=data["MJD"],
        dut1=float(data["Value"]) * 0.001,
    )

    with _iers_cache_lock:
        _iers_cache[url] = IERSCache(
            at=now,
            entry=entry,
        )

    return entry


# **************************************************************************************
