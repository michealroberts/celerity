# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from pathlib import Path
from struct import unpack
from typing import Dict, Sequence, Tuple
from urllib.request import Request, urlopen

from .planet import NAIF_PLANETARY_BARYCENTER_ID_TO_PLANET, Planet

# **************************************************************************************

# NASA NAIF server URL for DE440 ephemeris:
DE440_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de442.bsp"

# **************************************************************************************

# DAF is the underlying binary format used by NASA/NAIF for SPK ephemeris files:
DAF_RECORD_SIZE: int = 1024

# **************************************************************************************

# NAIF ID for the Solar System Barycenter, the mass-weighted center of the solar system:
SOLAR_SYSTEM_BARYCENTER_ID: int = 0

# **************************************************************************************


@dataclass(frozen=True)
class DETerm:
    """
    A single scalar coefficient in a Chebyshev polynomial series from the DE ephemeris
    (e.g. DE442).

    This represents one term of a Chebyshev series, consisting of a coefficient
    multiplied by a Chebyshev polynomial of a given degree.

    The term is typically used with a normalized time argument x in [-1, 1].
    """

    coefficient: float


# **************************************************************************************


@dataclass(frozen=True)
class DESegment:
    """
    A single DE ephemeris segment containing Chebyshev coefficients for a body's
    barycentric position over a fixed time interval.

    A segment corresponds to one contiguous time span in the development ephemeris.

    Within this interval, the position of a body is represented by three independent
    Chebyshev series (x, y, z), each defined by a set of coefficients.
    """

    # Start epoch (Julian days, TDB):
    start: float

    # End epoch (Julian days, TDB):
    end: float

    # Chebyshev coefficients for x:
    x: Tuple[float, ...]

    # Chebyshev coefficients for y:
    y: Tuple[float, ...]

    # Chebyshev coefficients for z:
    z: Tuple[float, ...]


# **************************************************************************************


@dataclass(frozen=True)
class PlanetDE442Series:
    """
    Complete DE442 ephemeris series for a planet relative to the Solar System Barycenter.
    """

    segments: Sequence[DESegment]


# **************************************************************************************


def _parse_chebyshev_segments(
    data: bytes,
    indices: Tuple[int, int],
) -> Sequence[DESegment]:
    """
    Parse Chebyshev coefficients from a segment's data (SPK Type 2 format).

    :param data: The raw SPK file bytes.
    :param indices: Tuple of (start_index, end_index) for the segment (1-indexed, double words).
    :return: List of DE442 segments.
    """
    # Extract start and end indices:
    start_index, end_index = indices

    # Convert start index to byte offset:
    start_byte = (start_index - 1) * 8

    # Convert end index to byte offset, accounting for footer:
    end_byte = end_index * 8

    # Calculate footer offset (32 bytes before end):
    footer_offset = end_byte - 32

    # Unpack footer metadata, e.g., the initial epoch of the first record (in seconds
    # past J2000 TDB), the interval length (in seconds), record size (number of
    # doubles), and number of records:
    initial_epoch, interval, rsize, n = unpack("<4d", data[footer_offset:end_byte])

    rsize = int(rsize)

    n = int(n)

    # Each record contains coefficients for x, y, z components:
    n_coef = rsize // 3

    segments: list[DESegment] = []

    for i in range(n):
        offset = start_byte + i * rsize * 8

        record = unpack(f"<{rsize}d", data[offset : offset + rsize * 8])

        # Calculate the start Julian date for the segment (i.e., in TDB):
        start = 2451545.0 + (initial_epoch + i * interval) / 86400.0

        # Calculate the end Julian date for the segment (i.e., in TDB):
        end = 2451545.0 + (initial_epoch + (i + 1) * interval) / 86400.0

        x = tuple(record[0:n_coef])

        y = tuple(record[n_coef : 2 * n_coef])

        z = tuple(record[2 * n_coef : 3 * n_coef])

        segments.append(
            DESegment(
                start=start,
                end=end,
                x=x,
                y=y,
                z=z,
            )
        )

    return segments


# **************************************************************************************


def _parse_summaries(
    data: bytes,
    nd: int,
    ni: int,
    forward: int,
) -> Sequence[Tuple[int, int, Tuple[int, int]]]:
    """
    Parse all summaries from the DAF file.

    :param data: The raw SPK file bytes.
    :param nd: Number of double precision values per summary.
    :param ni: Number of integer values per summary.
    :param forward: Record number of the first summary record.
    :return: List of (target, center, (start_idx, end_idx)) tuples.
    """
    summaries: list[Tuple[int, int, Tuple[int, int]]] = []

    record = forward

    while record > 0:
        offset = (record - 1) * DAF_RECORD_SIZE

        # Next summary record pointer (0 if this is the last):
        next_record = int(unpack("<d", data[offset : offset + 8])[0])

        # Number of summaries in this record:
        n_summaries = int(unpack("<d", data[offset + 16 : offset + 24])[0])

        summary_size = nd * 8 + ni * 4

        for i in range(n_summaries):
            s_offset = offset + 24 + i * summary_size

            integers = unpack(
                f"<{ni}i", data[s_offset + nd * 8 : s_offset + nd * 8 + ni * 4]
            )

            target, center = integers[0], integers[1]
            start_idx, end_idx = integers[4], integers[5]

            summaries.append((target, center, (start_idx, end_idx)))

        record = next_record

    return summaries


# **************************************************************************************


def _parse_file_record(data: bytes) -> Tuple[int, int, int]:
    """
    Parse the DAF file record header (the first 1024 bytes of the file).

    :param data: The raw SPK file bytes.
    :return: Tuple of (nd, ni, forward).
    """
    # Number of double precision components in each summary (bytes 8-12):
    nd = unpack("<i", data[8:12])[0]

    # Number of integer components in each summary (bytes 12-16):
    ni = unpack("<i", data[12:16])[0]

    # Record number of the first summary record (bytes 76-80):
    forward = unpack("<i", data[76:80])[0]

    return nd, ni, forward


# **************************************************************************************


def _ensure_de440_exists() -> None:
    """
    Download DE440 ephemeris to package data directory if it doesn't exist.
    """
    uri = resources.files("celerity.data").joinpath("de442.bsp")

    if uri.is_file():
        return

    request = Request(DE440_URL, headers={"User-Agent": "celerity/1.0"})

    with urlopen(request, timeout=300) as response:
        Path(str(uri)).write_bytes(response.read())


# **************************************************************************************


@lru_cache(maxsize=1)
def _load_de442() -> Dict[Planet, PlanetDE442Series]:
    # Load the DE442 SPK file from package resources:
    uri = resources.files("celerity.data").joinpath("de442.bsp")

    # Read the entire binary SPK file:
    data = uri.read_bytes()

    # Parse the file record to get DAF parameters:
    nd, ni, forward = _parse_file_record(data)

    planets: Dict[Planet, PlanetDE442Series] = {}

    summaries = _parse_summaries(data, nd, ni, forward)

    # Process each summary to extract Chebyshev segments:
    for target, center, indices in summaries:
        # Only process segments relative to the Solar System Barycenter:
        if center != SOLAR_SYSTEM_BARYCENTER_ID:
            continue

        # Only process segments for known planets:
        if target not in NAIF_PLANETARY_BARYCENTER_ID_TO_PLANET:
            continue

        # Get the planet from the target ID:
        planet = NAIF_PLANETARY_BARYCENTER_ID_TO_PLANET[target]

        # Parse Chebyshev segments for this planet:
        segments = _parse_chebyshev_segments(data, indices)

        planets[planet] = PlanetDE442Series(segments=segments)

    return planets


# **************************************************************************************


def get_de442_series(planet: Planet) -> PlanetDE442Series:
    """
    Retrieve the DE442 series for a specified planet.

    :param planet: The planet to retrieve the DE442 series for.
    :return: The DE442 series terms for the specified planet.
    """
    # Download the DE442 SPK file to the known location if not already cached:
    _ensure_de440_exists()

    return _load_de442()[planet]


# **************************************************************************************

if __name__ == "__main__":
    # Run as uv run python -m celerity.de440 to test loading the DE440 data:
    earth = get_de442_series(Planet.EARTH)
    print(f"Earth DE442 Series: {earth}")

# **************************************************************************************
