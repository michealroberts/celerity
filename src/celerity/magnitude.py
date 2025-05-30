# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from math import log10

# **************************************************************************************


def get_absolute_magnitude(magnitude: float, distance: float) -> float:
    """
    Calculate the absolute magnitude of a celestial object given its apparent magnitude
    and distance to the object (in parsecs).

    Args:
        magnitude (float): The apparent magnitude of the object.
        distance (float): The distance to the object (in parsecs).

    Returns:
        float: The absolute magnitude of the object.
    """
    # If the distance is negative or zero (non-positive), then this is not a valid
    # calculation:
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")

    # Return the absolute magnitude using the standard formula:
    return magnitude - 5 * (log10(distance) - 1)


# **************************************************************************************
