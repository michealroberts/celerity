# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import math
import unittest

from celerity.integration import perform_definite_integral

# **************************************************************************************


class TestPerformDefiniteIntegral(unittest.TestCase):
    def assertAlmostEqualRelative(self, a: float, b: float, rel_tol: float = 1e-9):
        """
        Helper to compare floating-point values using relative tolerance.
        """
        self.assertTrue(
            math.isclose(a, b, rel_tol=rel_tol),
            msg=f"Expected {a} ≈ {b} within rel_tol={rel_tol}",
        )

    def f_x_squared(self, x: float) -> float:
        return x**2

    def f_sin(self, x: float) -> float:
        return math.sin(x)

    def f_exp(self, x: float) -> float:
        return math.exp(x)

    def f_x_fourth(self, x: float) -> float:
        return x**4

    def f_identity(self, x: float) -> float:
        return x

    def test_polynomial_integral(self) -> None:
        result = perform_definite_integral(self.f_x_squared, 0.0, 1.0, 10)
        self.assertAlmostEqualRelative(result, 1.0 / 3.0)

    def test_trigonometric_integral(self) -> None:
        result = perform_definite_integral(self.f_sin, 0.0, math.pi, 100)
        self.assertAlmostEqualRelative(result, 2.0, rel_tol=1e-6)

    def test_exponential_integral(self) -> None:
        result = perform_definite_integral(self.f_exp, 0.0, 1.0, 100)
        self.assertAlmostEqualRelative(result, math.e - 1, rel_tol=1e-6)

    def test_zero_width_interval(self) -> None:
        result = perform_definite_integral(self.f_x_fourth, 2.0, 2.0, 10)
        self.assertEqual(result, 0.0)

    def test_invalid_subintervals_raises(self) -> None:
        with self.assertRaises(ValueError):
            perform_definite_integral(self.f_identity, 0.0, 1.0, 5)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
