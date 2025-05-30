# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.magnitude import get_absolute_magnitude

# **************************************************************************************


class TestGetAbsoluteMagnitude(unittest.TestCase):
    def test_known_value(self):
        # For example, let's pick m=5 and d=10 parsecs:
        self.assertAlmostEqual(get_absolute_magnitude(5, 10), 5.0, places=6)

    def test_bright_star(self):
        # Sirius has a magnitude of -1.46 and is at a distance of ~2.64 pc:
        result = get_absolute_magnitude(-1.46, 2.64)
        self.assertAlmostEqual(result, 1.432, places=2)

    def test_distance_one_parsec(self):
        # If the distance is 1 parsec, the absolute magnitude should equal the
        # apparent magnitude:
        self.assertAlmostEqual(get_absolute_magnitude(5, 1), 10.0, places=6)

    def test_invalid_distance(self):
        with self.assertRaises(ValueError):
            get_absolute_magnitude(5, 0)

        with self.assertRaises(ValueError):
            get_absolute_magnitude(5, -1)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
