# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.eop import EarthOrbitalParameters

# **************************************************************************************


class TestEarthOrbitalParameters(unittest.TestCase):
    """
    Test the EarthOrbitalParameters TypedDict.
    """

    def setUp(self) -> None:
        self.eop: EarthOrbitalParameters = {
            "modified_julian_date": 60000.0,
            "x_pole_arcseconds": 0.123456,
            "y_pole_arcseconds": 0.234567,
            "dut1": -0.0417670,
            "lod": 1.234,
            "celestial_pole_offset_dpsi_milliarcseconds": -0.135,
            "celestial_pole_offset_deps_milliarcseconds": -0.045,
        }

    def test_modified_julian_date(self) -> None:
        self.assertEqual(self.eop["modified_julian_date"], 60000.0)

    def test_x_pole_arcseconds(self) -> None:
        self.assertAlmostEqual(self.eop["x_pole_arcseconds"], 0.123456, places=6)

    def test_y_pole_arcseconds(self) -> None:
        self.assertAlmostEqual(self.eop["y_pole_arcseconds"], 0.234567, places=6)

    def test_dut1(self) -> None:
        self.assertAlmostEqual(self.eop["dut1"], -0.0417670, places=6)

    def test_lod(self) -> None:
        self.assertAlmostEqual(self.eop["lod"], 1.234, places=3)

    def test_celestial_pole_offset_dpsi_milliarcseconds(self) -> None:
        self.assertAlmostEqual(
            self.eop["celestial_pole_offset_dpsi_milliarcseconds"], -0.135, places=3
        )

    def test_celestial_pole_offset_deps_milliarcseconds(self) -> None:
        self.assertAlmostEqual(
            self.eop["celestial_pole_offset_deps_milliarcseconds"], -0.045, places=3
        )

    def test_all_keys_present(self) -> None:
        expected_keys = {
            "modified_julian_date",
            "x_pole_arcseconds",
            "y_pole_arcseconds",
            "dut1",
            "lod",
            "celestial_pole_offset_dpsi_milliarcseconds",
            "celestial_pole_offset_deps_milliarcseconds",
        }
        self.assertEqual(set(self.eop.keys()), expected_keys)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
