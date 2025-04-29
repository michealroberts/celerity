# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.light import get_light_travel_distance

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