# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import pow, radians, sin

# **************************************************************************************


def get_airmass(altitude: float) -> float:
    """
    Gets the airmass of an object at a given altitude using Pickering's formula.

    Airmass is a measure of the amount of air along the line of sight when observing a star
    or other celestial source from below Earth's atmosphere. It is formulated
    as the integral of air density along the light ray.

    :see: Pickering, K. A. (2002). "The Southern Limits of the Ancient Star Catalog" (PDF). DIO. 12 (1): 20-39.
    :param: altitude: The altitude of the object in degrees.
    :return: The airmass of the object.
    """
    return get_airmass_pickering(altitude)


# **************************************************************************************


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
    return 1 / sin(radians(altitude + 244 / (165 + (47 * pow(altitude, 1.1)))))


# **************************************************************************************


def get_airmass_karstenyoung(altitude: float) -> float:
    """
    Gets the airmass of an object at a given altitude using Karsten & Young's formula.

    Airmass is a measure of the amount of air along the line of sight when observing a star
    or other celestial source from below Earth's atmosphere. It is formulated
    as the integral of air density along the light ray.

    :see: Kasten, F.; Young, A. T. (1989). "Revised optical air mass tables and approximation formula". Applied Optics. 28 (22): 4735-4738.
    :param: altitude: The altitude of the object in degrees.
    :return: The airmass of the object.
    """
    return 1 / (sin(radians(altitude)) + 0.50572 * pow(altitude + 6.07995, -1.6364))


# **************************************************************************************
