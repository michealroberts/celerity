# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************


from .utilities import convert_degree_to_dms, convert_degree_to_hms

# **************************************************************************************


def format_degree_as_dms(degree: float) -> str:
    """
    Convert coordinate (in decimal degrees) to degrees (°), minutes ('), seconds ('').

    :param degree: decimal degree
    :return: e.g., string '0º 0' 00"'
    """
    dms = convert_degree_to_dms(degree)
    return f"{dms['deg']:+03d}° {dms['min']:02d}' {dms['sec']:05.2f}\""


# **************************************************************************************


def format_degree_as_hms(degree: float) -> str:
    """
    Convert coordinate (in decimal degrees) to hours (h), minutes (m), seconds (s).

    :param degree: decimal degree
    :return: e.g., string '0h 0m 00s'
    """
    hms = convert_degree_to_hms(degree)
    return f"{hms['hour']:02d}h {hms['min']:02d}m {hms['sec']:05.2f}s"


# **************************************************************************************
