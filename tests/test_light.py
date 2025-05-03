# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.constants import c as SPEED_OF_LIGHT
from celerity.constants import h as PLANCK_CONSTANT
from celerity.light import (
    get_light_travel_distance,
    get_photon_energy,
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


class TestPhotonEnergy(unittest.TestCase):
    def test_energy_from_frequency(self) -> None:
        """
        Test photon energy calculated from frequency.
        """
        frequency = 6e14  # Hz
        expected_energy = PLANCK_CONSTANT * frequency
        result = get_photon_energy(frequency=frequency)
        self.assertAlmostEqual(result, expected_energy, delta=1e-3 * expected_energy)

    def test_energy_from_wavelength(self) -> None:
        """
        Test photon energy calculated from wavelength.
        """
        wavelength = 500e-9  # meters (500 nm)
        expected_energy = PLANCK_CONSTANT * SPEED_OF_LIGHT / wavelength
        result = get_photon_energy(wavelength=wavelength)
        self.assertAlmostEqual(result, expected_energy, delta=1e-3 * expected_energy)

    def test_raises_on_both_parameters(self) -> None:
        """
        Test that passing both wavelength and frequency raises a ValueError.
        """
        with self.assertRaises(ValueError):
            get_photon_energy(wavelength=500e-9, frequency=6e14)

    def test_raises_on_neither_parameter(self) -> None:
        """
        Test that passing neither wavelength nor frequency raises a ValueError.
        """
        with self.assertRaises(ValueError):
            get_photon_energy()

    def test_negative_frequency_raises(self) -> None:
        """
        Test that a negative frequency raises a ValueError or returns invalid result.
        (This depends on implementation decision — adjust if needed.)
        """
        with self.assertRaises(ValueError):
            get_photon_energy(frequency=-1e14)

    def test_negative_wavelength_raises(self) -> None:
        """
        Test that a negative wavelength raises a ValueError or returns invalid result.
        (This depends on implementation decision — adjust if needed.)
        """
        with self.assertRaises(ValueError):
            get_photon_energy(wavelength=-500e-9)


# **************************************************************************************


if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
