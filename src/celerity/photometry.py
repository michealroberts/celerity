# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from typing import List, Sequence, Union

# **************************************************************************************


def convert_adu_to_electrons_for_frame(
    frame: Sequence[Union[int, float]], gain: float
) -> List[float]:
    """
    Converts a sequence of ADU values to electrons using the gain value.

    :param frame: A sequence of ADU values (e.g., list, tuple, or other sequence types).
    :param gain: The gain value in e-/ADU.
    :return: A list of converted values in electrons.
    :raises ValueError: If any value in the frame is not numeric.
    """
    try:
        return [float(adu) * gain for adu in frame]
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"All values in the frame must be numeric. Invalid value encountered: {e}"
        )


# **************************************************************************************
