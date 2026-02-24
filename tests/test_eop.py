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
            "mjd": 60000.0,
            "x_pole": 0.123456,
            "y_pole": 0.234567,
            "dut1": -0.0417670,
            "lod": 1.234,
            "dψ": -0.135,
            "dε": -0.045,
        }

    def test_modified_julian_date(self) -> None:
        self.assertEqual(self.eop["mjd"], 60000.0)

    def test_x_pole(self) -> None:
        self.assertAlmostEqual(self.eop["x_pole"], 0.123456, places=6)

    def test_y_pole(self) -> None:
        self.assertAlmostEqual(self.eop["y_pole"], 0.234567, places=6)

    def test_dut1(self) -> None:
        self.assertAlmostEqual(self.eop["dut1"], -0.0417670, places=6)

    def test_lod(self) -> None:
        self.assertAlmostEqual(self.eop["lod"], 1.234, places=3)

    def test_dψ(self) -> None:
        self.assertAlmostEqual(self.eop["dψ"], -0.135, places=3)

    def test_dε(self) -> None:
        self.assertAlmostEqual(self.eop["dε"], -0.045, places=3)

    def test_all_keys_present(self) -> None:
        expected_keys = {
            "mjd",
            "x_pole",
            "y_pole",
            "dut1",
            "lod",
            "dψ",
            "dε",
        }
        self.assertEqual(set(self.eop.keys()), expected_keys)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
