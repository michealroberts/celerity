# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from typing import Callable

# **************************************************************************************

RealFunction = Callable[[float], float]

# **************************************************************************************


def perform_definite_integral(f: RealFunction, a: float, b: float, n: int) -> float:
    """
    Approximates the definite integral of f from a to b using Simpson's rule.

    :param f: The function to integrate
    :param a: The lower limit of integration
    :param b: The upper limit of integration
    :param n: The number of subintervals (must be even)
    :return: The approximate value of the integral
    """
    # Ensure that the lower limit is less than the upper limit:
    if a > b:
        raise ValueError("Lower limit must be less than upper limit")

    # If the interval is zero width, return 0.0:
    if a == b:
        return 0.0

    # Ensure that n is a positive even integer:
    if n <= 0:
        raise ValueError("Number of subintervals must be positive")

    # Ensure that n is an even integer:
    if n % 2 != 0:
        raise ValueError("Number of subintervals must be even")

    h = (b - a) / n

    # Calculate the x values:
    x: list[float] = [a + i * h for i in range(n + 1)]

    # Calculate the function values at each x:
    y: list[float] = [f(i) for i in x]

    return (h / 3) * (
        y[0]
        + 4 * sum(y[i] for i in range(1, n, 2))
        + 2 * sum(y[i] for i in range(2, n - 1, 2))
        + y[-1]
    )


# **************************************************************************************
