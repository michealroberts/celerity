# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from math import floor

from .common import Angle
from .utilities import convert_degree_to_dms

# *****************************************************************************************************************


def format_degree_as_dms(degree: float) -> str:
    """
    Convert coordinate (in decimal degrees) to degrees (°), minutes ('), seconds ('').

    :param degree: decimal degree
    :return: e.g., string '0º 0' 00"'
    """
    dms = convert_degree_to_dms(degree)
    return f"{dms['deg']:+03d}° {dms['min']:02d}' {dms['sec']:05.2f}\""


# *****************************************************************************************************************
