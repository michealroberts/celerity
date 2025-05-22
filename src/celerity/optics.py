# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from typing import TypedDict

# **************************************************************************************


class Transmission(TypedDict):
    # The transmission coefficient of an optical element, which is the fraction of light
    # that passes through the element. This is typically a value between 0 and 1.
    # A value of 1 means that all light passes through the element, while a value of 0
    # means that no light passes through:
    coefficient: float


# **************************************************************************************
