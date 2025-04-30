# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.cosmology import get_hubble_parameter

# **************************************************************************************

class TestDimensionlessHubbleParameter(unittest.TestCase):

    def test_z_0_1(self):
        expected = 1.0509512424689358
        result = get_hubble_parameter(0.1)
        self.assertAlmostEqual(result, expected, places=6)

    def test_z_1(self):
        expected = 1.7912472526147807
        result = get_hubble_parameter(1)
        self.assertAlmostEqual(result, expected, places=6)

    def test_z_10(self):
        expected = 20.535119684822877
        result = get_hubble_parameter(10)
        self.assertAlmostEqual(result, expected, places=6)

    def test_z_100(self):
        expected = 578.2679369977814
        result = get_hubble_parameter(100)
        self.assertAlmostEqual(result, expected, places=6)

    def test_z_1000(self):
        expected = 20206.040613805857
        result = get_hubble_parameter(1000)
        self.assertAlmostEqual(result, expected, places=6)

    def test_negative_redshift_raises(self):
        with self.assertRaises(ValueError):
            get_hubble_parameter(-1)

# **************************************************************************************

if __name__ == '__main__':
    unittest.main()

# **************************************************************************************