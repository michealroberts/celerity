import math


def get_airmass_pickering(altitude: float) -> float:
    """
    Gets the airmass of an object at a given altitude using Pickering's formula.

    Airmass is a measure of the amount of air along the line of sight when observing a star
    or other celestial source from below Earth's atmosphere. It is formulated
    as the integral of air density along the light ray.

    :see: Pickering, K. A. (2002). "The Southern Limits of the Ancient Star Catalog" (PDF). DIO. 12 (1): 20-39.
    :param: altitude: The altitude of the object in degrees.
    :return: The airmass of the object.
    """
    return 1 / math.sin(
        math.radians(altitude + 244 / (165 + (47 * math.pow(altitude, 1.1))))
    )
