# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.optics import (
    SurfaceReflectance,
    Transmission,
    get_optical_system_throughput,
)

# **************************************************************************************


class TestGetOpticalSystemThroughput(unittest.TestCase):
    def test_all_elements_present(self):
        """Test throughput with primary, secondary, lens, filter, and QE all valid."""
        T = get_optical_system_throughput(
            primary=SurfaceReflectance({"albedo": 0.92}),
            secondary=SurfaceReflectance({"albedo": 0.90}),
            lens=Transmission({"coefficient": 0.98}),
            filter=Transmission({"coefficient": 0.85}),
            QE=0.80,
        )
        expected = 0.92 * 0.90 * 0.98 * 0.85 * 0.80
        self.assertAlmostEqual(T, expected, places=9)

    def test_without_secondary(self):
        """Test throughput when secondary is omitted (albedo=1.0)."""
        T = get_optical_system_throughput(
            primary=SurfaceReflectance({"albedo": 0.95}),
            lens=Transmission({"coefficient": 0.99}),
            filter=Transmission({"coefficient": 0.90}),
            QE=0.75,
        )
        expected = 0.95 * 1.0 * 0.99 * 0.90 * 0.75
        self.assertAlmostEqual(T, expected, places=9)

    def test_invalid_primary_albedo_negative(self):
        """Primary albedo < 0 should raise ValueError."""
        with self.assertRaises(ValueError):
            get_optical_system_throughput(
                primary=SurfaceReflectance({"albedo": -0.1}),
                lens=Transmission({"coefficient": 0.90}),
                filter=Transmission({"coefficient": 0.90}),
                QE=0.90,
            )

    def test_invalid_primary_albedo_gt_one(self):
        """Primary albedo > 1 should raise ValueError."""
        with self.assertRaises(ValueError):
            get_optical_system_throughput(
                primary=SurfaceReflectance({"albedo": 1.1}),
                lens=Transmission({"coefficient": 0.90}),
                filter=Transmission({"coefficient": 0.90}),
                QE=0.90,
            )

    def test_invalid_secondary_albedo(self):
        """Secondary albedo outside [0,1] should raise ValueError."""
        with self.assertRaises(ValueError):
            get_optical_system_throughput(
                primary=SurfaceReflectance({"albedo": 0.90}),
                secondary=SurfaceReflectance({"albedo": 1.2}),
                lens=Transmission({"coefficient": 0.90}),
                filter=Transmission({"coefficient": 0.90}),
                QE=0.90,
            )

    def test_invalid_lens_transmission(self):
        """Lens transmission coefficient < 0 should raise ValueError."""
        with self.assertRaises(ValueError):
            get_optical_system_throughput(
                primary=SurfaceReflectance({"albedo": 0.90}),
                lens=Transmission({"coefficient": -0.2}),
                filter=Transmission({"coefficient": 0.90}),
                QE=0.90,
            )

    def test_invalid_filter_transmission(self):
        """Filter transmission coefficient > 1 should raise ValueError."""
        with self.assertRaises(ValueError):
            get_optical_system_throughput(
                primary=SurfaceReflectance({"albedo": 0.90}),
                lens=Transmission({"coefficient": 0.90}),
                filter=Transmission({"coefficient": 1.5}),
                QE=0.90,
            )

    def test_invalid_qe(self):
        """Quantum efficiency outside [0,1] should raise ValueError."""
        with self.assertRaises(ValueError):
            get_optical_system_throughput(
                primary=SurfaceReflectance({"albedo": 0.90}),
                lens=Transmission({"coefficient": 0.90}),
                filter=Transmission({"coefficient": 0.90}),
                QE=1.2,
            )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
