# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from math import pi

from celerity.telescope import (
    CollectingSurface,
    get_collecting_area,
)

# **************************************************************************************


class TestGetCollectingArea(unittest.TestCase):
    def test_primary_only(self):
        """Test the collecting area of a primary mirror only."""
        A = get_collecting_area(
            primary=CollectingSurface(
                {
                    "diameter": 2.0,
                }
            ),
        )
        expected = pi * (2.0 / 2) ** 2
        self.assertAlmostEqual(A, expected, places=9)

    def test_with_secondary(self):
        """Test the collecting area of a primary mirror with a secondary mirror."""
        A = get_collecting_area(
            primary=CollectingSurface({"diameter": 2.0}),
            secondary=CollectingSurface({"diameter": 0.3}),
        )
        ε = 0.3 / 2.0
        expected = pi * (2.0 / 2) ** 2 * (1 - ε**2)
        self.assertAlmostEqual(A, expected, places=9)

    def test_secondary_equal_primary(self):
        """
        Test the collecting area of a primary mirror with a secondary mirror
        equal to the primary.
        """
        A = get_collecting_area(
            primary=CollectingSurface({"diameter": 1.5}),
            secondary=CollectingSurface({"diameter": 1.5}),
        )
        expected = 0.0
        self.assertAlmostEqual(A, expected, places=9)

    def test_secondary_zero(self):
        """Test the collecting area of a primary mirror with a secondary mirror of zero."""
        A = get_collecting_area(
            primary=CollectingSurface({"diameter": 1.2}),
            secondary=CollectingSurface({"diameter": 0.0}),
        )
        expected = pi * (1.2 / 2) ** 2
        self.assertAlmostEqual(A, expected, places=9)

    def test_missing_primary_diameter_uses_default(self):
        """Test the collecting area of a primary mirror with a missing diameter."""
        A = get_collecting_area(
            primary=CollectingSurface({}),
        )
        expected = pi * (1.0 / 2) ** 2
        self.assertAlmostEqual(A, expected, places=9)

    def test_secondary_none_uses_default_diameter_zero(self):
        """Test the collecting area of a primary mirror with a secondary mirror of None."""
        A_none = get_collecting_area(
            primary=CollectingSurface({"diameter": 2.5}),
        )
        A_zero = get_collecting_area(
            primary=CollectingSurface({"diameter": 2.5}),
            secondary=CollectingSurface({"diameter": 0.0}),
        )
        self.assertAlmostEqual(A_none, A_zero, places=9)

    def test_secondary_greater_than_primary(self):
        """
        Test the collecting area of a primary mirror with a secondary mirror
        larger than the primary mirror.
        """
        with self.assertRaises(ValueError):
            get_collecting_area(
                primary=CollectingSurface({"diameter": 1.0}),
                secondary=CollectingSurface({"diameter": 2.0}),
            )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
