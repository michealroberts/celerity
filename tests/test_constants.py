# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

import unittest

from celerity.constants import (
    AU,
    H0_PLANCK_2018,
    J1900,
    J1970,
    J2000,
    PARSEC,
    c,
    h,
)

# **************************************************************************************


class TestConstants(unittest.TestCase):
    def test_J1900(self):
        self.assertEqual(J1900, 2415020.0)

    def test_J1970(self):
        self.assertEqual(J1970, 2440587.5)

    def test_J2000(self):
        self.assertEqual(J2000, 2451545.0)

    def test_c(self):
        self.assertEqual(c, 299792458)

    def test_h(self):
        self.assertEqual(h, 6.62607015e-34)

    def test_AU(self):
        self.assertEqual(AU, 149597870700.0)

    def test_PARSEC(self):
        self.assertEqual(PARSEC, 3.085677581491367e16)

    def test_H0_PLANCK_2018(self):
        self.assertEqual(H0_PLANCK_2018["value"], 67.74)
        self.assertEqual(H0_PLANCK_2018["uncertainty"], 0.46)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
