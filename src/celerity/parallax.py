def get_distance(parallax: float) -> float:
    """
    Get distance in parsecs from parallax in arcseconds.

    :param parallax: parallax in arcseconds
    :return: distance in parsecs
    """
    return 1.0 / parallax
