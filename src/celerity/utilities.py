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
