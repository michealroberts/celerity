# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

import unittest

from celerity.constants import J1900, J1970, J2000, c, h

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

# **************************************************************************************