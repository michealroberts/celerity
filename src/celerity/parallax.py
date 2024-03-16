# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************


def get_distance(parallax: float) -> float:
    """
    Get distance in parsecs from parallax in arcseconds.

    :param parallax: parallax in arcseconds
    :return: distance in parsecs
    """
    return 1.0 / parallax


# **************************************************************************************


def convert_parallax_to_metres(parallax: float) -> float:
    """
    Convert parallax in arcseconds to metres.

    :param parallax: parallax in arcseconds
    :return: parallax in metres
    """
    # Get the distance in parsecs:
    d = get_distance(parallax)
    return d * 3.08567758128e16


# **************************************************************************************
