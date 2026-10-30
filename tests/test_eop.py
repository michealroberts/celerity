# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from src.celerity.eop import EarthOrbitalParameters

# **************************************************************************************

eop: EarthOrbitalParameters = {
    "mjd": 60000.0,
    "x_polar_motion": 0.123456,
    "y_polar_motion": 0.234567,
    "dut1": -0.0417670,
    "lod": 1.234,
    "pole_offset_in_ecliptic_longitude": -0.135,
    "pole_offset_in_ecliptic_obliquity": -0.045,
}

# **************************************************************************************


def test_mjd() -> None:
    assert eop["mjd"] == 60000.0


# **************************************************************************************


def test_x_polar_motion() -> None:
    assert abs(eop["x_polar_motion"] - 0.123456) < 1e-6


# **************************************************************************************


def test_y_polar_motion() -> None:
    assert abs(eop["y_polar_motion"] - 0.234567) < 1e-6


# **************************************************************************************


def test_dut1() -> None:
    assert abs(eop["dut1"] - (-0.0417670)) < 1e-6


# **************************************************************************************


def test_lod() -> None:
    assert abs(eop["lod"] - 1.234) < 1e-3


# **************************************************************************************


def test_pole_offset_in_ecliptic_longitude() -> None:
    assert abs(eop["pole_offset_in_ecliptic_longitude"] - (-0.135)) < 1e-3


# **************************************************************************************


def test_pole_offset_in_ecliptic_obliquity() -> None:
    assert abs(eop["pole_offset_in_ecliptic_obliquity"] - (-0.045)) < 1e-3


# **************************************************************************************


def test_all_keys_present() -> None:
    expected_keys = {
        "mjd",
        "x_polar_motion",
        "y_polar_motion",
        "dut1",
        "lod",
        "pole_offset_in_ecliptic_longitude",
        "pole_offset_in_ecliptic_obliquity",
    }
    assert set(eop.keys()) == expected_keys


# **************************************************************************************
