# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from __future__ import annotations

from typing import TypedDict

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
    x_pole: float

    # The y-coordinate of the Earth's celestial intermediate pole (CIP) with respect
    # to the IERS Reference Pole (IRP), measured in degrees along the meridian
    # 90° west of the IERS Reference Meridian (IRM). Positive values indicate
    # displacement of the pole toward 90° west longitude:
    y_pole: float

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
    dψ: float

    # dε — the celestial pole offset in ecliptic obliquity, measured in degrees,
    # representing the observed deviation of the true celestial pole from the
    # position predicted by the IAU 1980 theory of nutation. This offset is applied
    # along the direction of increasing ecliptic obliquity and, together with dψ,
    # fully describes the residual between the observed and modeled pole position:
    dε: float


# **************************************************************************************
