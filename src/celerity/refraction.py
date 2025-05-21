# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import radians, tan

from .common import HorizontalCoordinate

# **************************************************************************************


def get_correction_to_horizontal_for_refraction(
    target: HorizontalCoordinate, temperature: float = 283.15, pressure: float = 101325
) -> HorizontalCoordinate:
    """
    Corrects the horizontal coordinates of a target for atmospheric refraction.

    :param target: The horizontal coordinates of the target.
    :param temperature: The temperature in Kelvin.
    :param pressure: The pressure in Pascals.
    """
    alt = target["alt"]

    if alt < 0:
        return target

    # The pressure, in Pascals:
    P = pressure

    # The temperature, in Kelvin:
    T = temperature

    # Get the atmospheric refraction in degrees, corrected for temperature and pressure:
    R = (
        (1.02 / tan(radians(alt + (10.3 / (alt + 5.11)))))
        / 60
        * (P / 101325)
        * (283.15 / T)
    )

    return HorizontalCoordinate(
        {
            "az": target["az"],
            "alt": target["alt"] + R,
        }
    )


# **************************************************************************************
