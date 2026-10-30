# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime, timezone
from json import loads
from math import inf
from typing import List, Literal, TypedDict
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .temporal import get_modified_julian_date_as_parts
from .utilities import convert_arcseconds_to_degrees

# **************************************************************************************

EOP_TIMEOUT_SECONDS = 10

# **************************************************************************************

EOP_MAX_LOD_LOOKBACK_DAYS = 365

# **************************************************************************************

IERS_EOP_BASE_URL = "https://datacenter.iers.org/webservice/REST/eop/RestController.php"

# **************************************************************************************


class EarthOrbitalParameters(TypedDict):
    # The Modified Julian Date (MJD) for this EOP entry, representing the number
    # of days elapsed since the standard MJD epoch of 17 November 1858 at midnight
    # (00:00 UTC). Used as the primary time reference for all other EOP values in
    # this record:
    mjd: float

    # The x-coordinate of the Earth's celestial intermediate pole (CIP) with respect
    # to the IERS Reference Pole (IRP), measured in degrees along the direction
    # of the IERS Reference Meridian (IRM) toward Greenwich. Positive values indicate
    # displacement of the pole toward the Greenwich meridian:
    x_polar_motion: float

    # The y-coordinate of the Earth's celestial intermediate pole (CIP) with respect
    # to the IERS Reference Pole (IRP), measured in degrees along the meridian
    # 90° west of the IERS Reference Meridian (IRM). Positive values indicate
    # displacement of the pole toward 90° west longitude:
    y_polar_motion: float

    # The difference UT1 - UTC (in seconds), representing the offset between
    # Universal Time 1 (UT1, which tracks the actual rotation of the Earth) and
    # Coordinated Universal Time (UTC). This value is kept within ±0.9 seconds
    # of zero by the periodic insertion of leap seconds into the UTC timescale:
    dut1: float

    # The excess length of day (LOD) above the nominal 86400 SI seconds (in
    # seconds), representing the day-to-day variation in the Earth's rotation
    # rate. A positive LOD indicates the Earth is rotating more slowly than the
    # standard rate (i.e., the day is longer than 86400 seconds):
    lod: float

    # dψ — the celestial pole offset in ecliptic longitude, measured in degrees,
    # representing the observed deviation of the true celestial pole from the
    # position predicted by the IAU 1980 theory of nutation. This offset is applied
    # along the direction of increasing ecliptic longitude and accounts for
    # unpredictable free-core nutation and other geophysical effects not captured
    # by the precession-nutation model:
    pole_offset_in_ecliptic_longitude: float

    # dε — the celestial pole offset in ecliptic obliquity, measured in degrees,
    # representing the observed deviation of the true celestial pole from the
    # position predicted by the IAU 1980 theory of nutation. This offset is applied
    # along the direction of increasing ecliptic obliquity and, together with dψ,
    # fully describes the residual between the observed and modeled pole position:
    pole_offset_in_ecliptic_obliquity: float


# **************************************************************************************


class EOPRequestParams(TypedDict):
    param: Literal["UT1-UTC", "x_pole", "y_pole", "LOD", "dX", "dY"]
    mjd: int
    series: Literal["Finals All IAU2000"]


# **************************************************************************************


def parse_eop_value(value: object) -> float | None:
    if value is None:
        return None

    if isinstance(value, int | float):
        return float(value)

    raw = str(value).strip()

    if raw in {"", "-"}:
        return None

    return float(raw)


# **************************************************************************************


def fetch_eop_parameter(
    param: Literal["UT1-UTC", "x_pole", "y_pole", "LOD", "dX", "dY"], MJD: int
) -> float | None:
    query: EOPRequestParams = EOPRequestParams(
        {
            "param": param,
            "mjd": MJD,
            "series": "Finals All IAU2000",
        }
    )

    url: str = f"{IERS_EOP_BASE_URL}?{urlencode(query)}"

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

    with urlopen(request, timeout=EOP_TIMEOUT_SECONDS) as response:
        # Assume UTF-8 or ASCII text in the response:
        raw = response.read().decode("utf-8", errors="ignore")

    # Load the JSON data from the response:
    data = loads(raw)

    if int(data["MJD"]) != MJD:
        raise ValueError(
            f"Received MJD {data['MJD']} does not match requested MJD {MJD}"
        )

    if data["Param"] != param:
        raise ValueError(
            f"Received parameter {data['Param']} does not match requested parameter {param}"
        )

    return parse_eop_value(data["Value"])


# **************************************************************************************


def fetch_earth_orientation_parameters(MJD: int) -> EarthOrbitalParameters:
    # Setup the query parameters for the IERS Rapid Service data:
    queries: List[EOPRequestParams] = [
        EOPRequestParams(
            {
                "param": "UT1-UTC",
                "mjd": MJD,
                "series": "Finals All IAU2000",
            }
        ),
        EOPRequestParams(
            {
                "param": "x_pole",
                "mjd": MJD,
                "series": "Finals All IAU2000",
            }
        ),
        EOPRequestParams(
            {
                "param": "y_pole",
                "mjd": MJD,
                "series": "Finals All IAU2000",
            }
        ),
        EOPRequestParams(
            {
                "param": "LOD",
                "mjd": MJD,
                "series": "Finals All IAU2000",
            }
        ),
        EOPRequestParams(
            {
                "param": "dX",
                "mjd": MJD,
                "series": "Finals All IAU2000",
            }
        ),
        EOPRequestParams(
            {
                "param": "dY",
                "mjd": MJD,
                "series": "Finals All IAU2000",
            }
        ),
    ]

    entry: EarthOrbitalParameters = EarthOrbitalParameters(
        {
            "mjd": float(MJD),
            "dut1": -inf,
            "x_polar_motion": -inf,
            "y_polar_motion": -inf,
            "lod": -inf,
            "pole_offset_in_ecliptic_longitude": -inf,
            "pole_offset_in_ecliptic_obliquity": -inf,
        }
    )

    for q in queries:
        value = fetch_eop_parameter(q["param"], MJD)

        if value is None:
            continue

        if q["param"] == "UT1-UTC":
            # Convert our DUT1 value from milliseconds to seconds:
            entry["dut1"] = value * 0.001

        if q["param"] == "x_pole":
            entry["x_polar_motion"] = convert_arcseconds_to_degrees(value / 1000.0)

        if q["param"] == "y_pole":
            entry["y_polar_motion"] = convert_arcseconds_to_degrees(value / 1000.0)

        if q["param"] == "LOD":
            # Convert LOD from milliseconds to seconds.
            entry["lod"] = value * 0.001

        if q["param"] == "dX":
            entry["pole_offset_in_ecliptic_longitude"] = convert_arcseconds_to_degrees(
                value / 1000.0
            )

        if q["param"] == "dY":
            entry["pole_offset_in_ecliptic_obliquity"] = convert_arcseconds_to_degrees(
                value / 1000.0
            )

    # IAU2000 predictions do not publish LOD, so backfill from the nearest prior MJD:
    if entry["lod"] == -inf:
        for fallback_mjd in range(MJD - 1, MJD - EOP_MAX_LOD_LOOKBACK_DAYS - 1, -1):
            value = fetch_eop_parameter("LOD", fallback_mjd)

            if value is None:
                continue

            entry["lod"] = value * 0.001
            break

    return entry


# **************************************************************************************

if __name__ == "__main__":
    # Get the current date and time:
    now = datetime.now(timezone.utc)

    # Convert to Modified Julian Date (MJD):
    MJD, _ = get_modified_julian_date_as_parts(when=now)

    # Fetch the Earth Orientation Parameters for the current MJD:
    eop = fetch_earth_orientation_parameters(MJD)

    print(f"EOP at MJD {MJD}: {eop}")

# **************************************************************************************
