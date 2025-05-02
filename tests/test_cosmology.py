# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.constants import H0_PLANCK_2018, H0_SH0ES_2022
from celerity.cosmology import (
    get_comoving_distance,
    get_hubble_parameter,
    get_luminosity_distance,
)

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


class TestComovingDistance(unittest.TestCase):
    def test_planck_z0(self):
        d = get_comoving_distance(0.0, H0_PLANCK_2018)
        self.assertEqual(d["value"], 0.0)
        self.assertEqual(d["uncertainty"], 0.0)

    def test_shoes_z0(self):
        d = get_comoving_distance(0.0, H0_SH0ES_2022)
        self.assertEqual(d["value"], 0.0)
        self.assertEqual(d["uncertainty"], 0.0)

    def test_planck_z0_1(self):
        d = get_comoving_distance(0.1, H0_PLANCK_2018)
        expected_val = 1.332914e25
        expected_unc = 9.46e22
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z1(self):
        d = get_comoving_distance(1.0, H0_PLANCK_2018)
        expected_val = 1.0442894e26
        expected_unc = 7.095e23
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z10(self):
        d = get_comoving_distance(10.0, H0_PLANCK_2018)
        expected_val = 2.9577636e26
        expected_unc = 2.00552e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z100(self):
        d = get_comoving_distance(100.0, H0_PLANCK_2018)
        expected_val = 3.940563e26
        expected_unc = 2.67718e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z1000(self):
        d = get_comoving_distance(1000.0, H0_PLANCK_2018)
        expected_val = 4.52003e26
        expected_unc = 3.072e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_shoes_z0_1(self):
        d = get_comoving_distance(0.1, H0_SH0ES_2022)
        expected_val = 1.236422e25
        expected_unc = 1.7974e23
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z1(self):
        d = get_comoving_distance(1.0, H0_SH0ES_2022)
        expected_val = 9.685148e25
        expected_unc = 1.38116e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z10(self):
        d = get_comoving_distance(10.0, H0_SH0ES_2022)
        expected_val = 2.7431162e26
        expected_unc = 3.90698e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z100(self):
        d = get_comoving_distance(100.0, H0_SH0ES_2022)
        expected_val = 3.6546818e26
        expected_unc = 5.203e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z1000(self):
        d = get_comoving_distance(1000.0, H0_SH0ES_2022)
        expected_val = 3.9610912e26
        expected_unc = 5.63816e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )


# **************************************************************************************


class TestLuminosityDistance(unittest.TestCase):
    def test_planck_z0(self):
        d = get_luminosity_distance(0.0, H0_PLANCK_2018)
        self.assertEqual(d["value"], 0.0)
        self.assertEqual(d["uncertainty"], 0.0)

    def test_shoes_z0(self):
        d = get_luminosity_distance(0.0, H0_SH0ES_2022)
        self.assertEqual(d["value"], 0.0)
        self.assertEqual(d["uncertainty"], 0.0)

    def test_planck_z0_1(self):
        d = get_luminosity_distance(0.1, H0_PLANCK_2018)
        expected_val = 1.4662054e25
        expected_unc = 1.0406e23
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z1(self):
        d = get_luminosity_distance(1.0, H0_PLANCK_2018)
        expected_val = 2.0885788e26
        expected_unc = 1.419e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z10(self):
        d = get_luminosity_distance(10.0, H0_PLANCK_2018)
        expected_val = 3.25353996e27
        expected_unc = 2.206072e25
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z100(self):
        d = get_luminosity_distance(100.0, H0_PLANCK_2018)
        expected_val = 3.97996863e28
        expected_unc = 2.7039518e26
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_planck_z1000(self):
        d = get_luminosity_distance(1000.0, H0_PLANCK_2018)
        expected_val = 4.52455003e29
        expected_unc = 3.075072e27
        self.assertAlmostEqual(d["value"], expected_val, delta=0.05 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.20 * expected_unc
        )

    def test_shoes_z0_1(self):
        d = get_luminosity_distance(0.1, H0_SH0ES_2022)
        expected_val = 1.3600642e25
        expected_unc = 1.97714e23
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z1(self):
        d = get_luminosity_distance(1.0, H0_SH0ES_2022)
        expected_val = 1.9370296e26
        expected_unc = 2.76232e24
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z10(self):
        d = get_luminosity_distance(10.0, H0_SH0ES_2022)
        expected_val = 3.01742782e27
        expected_unc = 4.297678e25
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z100(self):
        d = get_luminosity_distance(100.0, H0_SH0ES_2022)
        expected_val = 3.691228618e28
        expected_unc = 5.25503e26
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )

    def test_shoes_z1000(self):
        d = get_luminosity_distance(1000.0, H0_SH0ES_2022)
        expected_val = 3.9650522912e29
        expected_unc = 5.64379816e27
        self.assertAlmostEqual(d["value"], expected_val, delta=0.10 * expected_val)
        self.assertAlmostEqual(
            d["uncertainty"], expected_unc, delta=0.25 * expected_unc
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
