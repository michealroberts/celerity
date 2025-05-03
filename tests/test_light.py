# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.light import (
    get_light_travel_distance,
    get_photon_frequency,
    get_photon_wavelength,
)

# **************************************************************************************


class TestLightTravelDistance(unittest.TestCase):
    def test_light_travel_distance(self):
        """
        Test the light travel distance calculation.
        """
        # Test with a time of 1 second
        time = 1.0
        expected_distance = 299792458.0  # Speed of light in m/s
        self.assertAlmostEqual(get_light_travel_distance(time), expected_distance)

        # Test with a time of 2 seconds
        time = 2.0
        expected_distance = 599584916.0  # Speed of light in m/s * 2 seconds
        self.assertAlmostEqual(get_light_travel_distance(time), expected_distance)

        # Test with a time of 0.5 seconds
        time = 0.5

        expected_distance = 149896229.0  # Speed of light in m/s * 0.5 seconds
        self.assertAlmostEqual(get_light_travel_distance(time), expected_distance)


# **************************************************************************************


class TestPhotonFrequency(unittest.TestCase):
    def test_photon_frequency(self) -> None:
        """
        Test the photon frequency calculation.
        """
        # Calculate the frequency using the wavelength of 500 nm:
        frequency = get_photon_frequency(500e-9)

        # Expected approximate frequency in Hz for 500 nm wavelength:
        expected_frequency = 6e14

        self.assertAlmostEqual(
            frequency, expected_frequency, delta=1e-3 * expected_frequency
        )

    def test_negative_photon_frequency(self) -> None:
        """
        Test the photon frequency calculation with a negative wavelength.
        """
        with self.assertRaises(ValueError):
            get_photon_frequency(-500e-9)


# **************************************************************************************


class TestPhotonWavelength(unittest.TestCase):
    def test_photon_wavelength(self) -> None:
        """
        Test the photon wavelength calculation.
        """
        # Calculate the wavelength using the frequency of 6e14 Hz:
        wavelength = get_photon_wavelength(6e14)

        # Expected approximate wavelength in meters for 6e14 Hz frequency:
        expected_wavelength = 500e-9

        self.assertAlmostEqual(
            wavelength, expected_wavelength, delta=1e-3 * expected_wavelength
        )

    def test_negative_photon_wavelength(self) -> None:
        """
        Test the photon wavelength calculation with a negative frequency.
        """
        with self.assertRaises(ValueError):
            get_photon_wavelength(-6e14)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
