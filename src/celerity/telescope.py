# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from math import pi
from typing import Optional, TypedDict

# **************************************************************************************


class CollectingSurface(TypedDict):
    diameter: float


# **************************************************************************************


def get_collecting_area(
    primary: CollectingSurface,
    secondary: Optional[CollectingSurface] = None,
) -> float:
    """
    Calculate the net collecting area of the telescope based on the primary and secondary
    mirrors. The collecting area is the area of the primary mirror minus the obstruction
    area of the secondary mirror (if present).

    :param primary: The primary mirror of the telescope.
    :param secondary: The secondary mirror of the telescope (if present).
    :return: The net collecting area of the telescope (in square meters).
    :raises ValueError: If the secondary mirror is larger than the primary mirror.
    """
    # Area of the primary mirror of the OTA/telescope:
    A = pi * (primary.get("diameter", 1) / 2) ** 2

    # If a secondary mirror is present, calculate the obstruction ratio of the secondary
    # mirror to the primary mirror:
    ε = (
        secondary.get("diameter", 0) / primary.get("diameter", 1)
        if secondary is not None
        else 0
    )

    # Sense check that the secondary mirror is not larger than the primary mirror:
    if secondary and (secondary.get("diameter", 0) > primary.get("diameter", 1)):
        raise ValueError(
            "The diameter of the secondary mirror cannot be larger than the primary mirror."
        )

    # Calculate the area of the secondary mirror:
    return A * (1 - ε**2)


# **************************************************************************************
