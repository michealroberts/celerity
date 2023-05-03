def get_normalised_azimuthal_degree(degree: float) -> float:
    """
    Applies a correction to a degree value greater than 360°

    :param degree: The degree value to correct
    :return: The corrected degree value (0° <= degree < 360°)
    """
    # Correct for large angles (+ive or -ive):
    d = degree % 360

    # Correct for negative angles
    if d < 0:
        d += 360

    return d


def get_normalised_inclination_degree(degree: float) -> float:
    """
    Applies a correction to a degree value greater than 90° or less than -90°

    :param degree: The degree value to correct
    :return: The corrected degree value (-90° <= degree <= 90°)
    """
    d = degree

    # Correct for angles greater than 90° or less than -90°
    if degree > 90:
        d = 180 - degree

    # Correct for angles less than -90°
    if degree < -90:
        d = -180 - degree

    if d < 0:
        d % -90

    if d > 0:
        d % 90

    return d
