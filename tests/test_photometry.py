# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest

from celerity.photometry import convert_adu_to_electrons_for_frame

# **************************************************************************************


class TestConvertAduToElectronsForFrame(unittest.TestCase):
    def test_basic_conversion(self):
        frame = [1, 2, 3]
        expected = [2.5, 5.0, 7.5]
        self.assertEqual(
            convert_adu_to_electrons_for_frame(frame=frame, gain=2.5), expected
        )

    def test_empty_frame(self):
        """An empty frame should return an empty list."""
        self.assertEqual(convert_adu_to_electrons_for_frame([], 5.0), [])

    def test_float_and_int_inputs(self):
        """Mix of ints and floats should all be converted to floats in the result."""
        frame = [0, 1.5, 2]
        result = convert_adu_to_electrons_for_frame(frame=frame, gain=1.0)
        self.assertIsInstance(result, list)
        for value in result:
            self.assertIsInstance(value, float)
        self.assertEqual(result, [0.0, 1.5, 2.0])

    def test_zero_gain(self):
        """A gain of zero should map all ADU values to 0.0."""
        frame = [10, 20, 30]
        self.assertEqual(
            convert_adu_to_electrons_for_frame(frame=frame, gain=0.0), [0.0, 0.0, 0.0]
        )

    def test_negative_gain(self):
        """Negative gains should correctly invert the sign of outputs."""
        frame = [1, 2, 3]
        expected = [-1.5, -3.0, -4.5]
        self.assertEqual(
            convert_adu_to_electrons_for_frame(frame=frame, gain=-1.5), expected
        )

    def test_non_numeric_adu(self):
        """Passing a non-numeric ADU value should raise a ValueError."""
        with self.assertRaises(ValueError):
            convert_adu_to_electrons_for_frame(frame=["a", 1], gain=2.0)


# **************************************************************************************

if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# **************************************************************************************
