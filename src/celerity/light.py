# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from typing import Optional

from .constants import c as SPEED_OF_LIGHT
from .constants import h as PLANCK_CONSTANT

# **************************************************************************************


def get_light_travel_distance(time: float) -> float:
    """
    Calculate the distance light travels in a given time.

    :param time: The time in seconds.
    :return: The distance light travels in the given time in meters.
    """
    return SPEED_OF_LIGHT * time


# **************************************************************************************


def get_photon_frequency(
    wavelength: float,
) -> float:
    """
    Calculate the frequency of a photon given its wavelength (in m).

    :param wavelength: Wavelength in meters
    :return: Photon frequency in Hz
    :raises ValueError: If wavelength is less than or equal to zero
    """
    if wavelength <= 0:
        raise ValueError("Wavelength must be a positive number.")

    return SPEED_OF_LIGHT / wavelength


# **************************************************************************************


def get_photon_wavelength(
    frequency: float,
) -> float:
    """
    Calculate the wavelength of a photon given its frequency (in Hz).

    :param frequency: Frequency in Hz
    :return: Photon wavelength in meters
    :raises ValueError: If frequency is less than or equal to zero
    """
    if frequency <= 0:
        raise ValueError("Frequency must be a positive number.")

    return SPEED_OF_LIGHT / frequency


# **************************************************************************************


def get_photon_energy(
    *,
    wavelength: Optional[float] = None,
    frequency: Optional[float] = None,
) -> float:
    """
    Calculate the energy of a photon given its wavelength.

    :param wavelength: Wavelength in meters (optional, exclusive with frequency)
    :param frequency: Frequency in Hz (optional, exclusive with wavelength)
    :return: Photon energy in joules
    :raises ValueError: If neither or both parameters are provided
    :raises ValueError: If wavelength or frequency is less than or equal to zero
    :raises ValueError: If neither wavelength nor frequency is provided
    """
    # XOR logic: either one of wavelength or frequency must be provided, but not both:
    if (wavelength is None) == (frequency is None):
        raise ValueError(
            "Provide exactly one of 'wavelength' or 'frequency', not both or neither."
        )

    # If neither wavelength nor frequency is provided, raise an error:
    if not wavelength and not frequency:
        raise ValueError("Either 'wavelength' or 'frequency' must be provided.")

    # If the wavelength is provided, but it is less than or equal to zero, raise an error:
    if wavelength is not None and wavelength <= 0:
        raise ValueError("Wavelength must be a positive number.")

    # If the frequency is provided, but it is less than or equal to zero, raise an error:
    if frequency is not None and frequency <= 0:
        raise ValueError("Frequency must be a positive number.")

    return (
        frequency * PLANCK_CONSTANT
        if frequency is not None
        else PLANCK_CONSTANT * SPEED_OF_LIGHT / wavelength
        if wavelength is not None
        else (_ for _ in ()).throw(
            ValueError("Either 'wavelength' or 'frequency' must be provided.")
        )
    )


# **************************************************************************************


def get_photon_momentum(
    *,
    wavelength: Optional[float] = None,
    frequency: Optional[float] = None,
) -> float:
    """
    Calculate the momentum of a photon given its wavelength or frequency.

    :param wavelength: Wavelength in meters (optional, exclusive with frequency)
    :param frequency: Frequency in Hz (optional, exclusive with wavelength)
    :return: Photon momentum in kg·m/s
    :raises ValueError: If neither or both parameters are provided
    :raises ValueError: If wavelength or frequency is less than or equal to zero
    :raises ValueError: If neither wavelength nor frequency is provided
    """
    # XOR logic: either one of wavelength or frequency must be provided, but not both:
    if (wavelength is None) == (frequency is None):
        raise ValueError(
            "Provide exactly one of 'wavelength' or 'frequency', not both or neither."
        )

    # If neither wavelength nor frequency is provided, raise an error:
    if not wavelength and not frequency:
        raise ValueError("Either 'wavelength' or 'frequency' must be provided.")

    # If the wavelength is provided, but it is less than or equal to zero, raise an error:
    if wavelength is not None and wavelength <= 0:
        raise ValueError("Wavelength must be a positive number.")

    # If the frequency is provided, but it is less than or equal to zero, raise an error:
    if frequency is not None and frequency <= 0:
        raise ValueError("Frequency must be a positive number.")

    return (
        (PLANCK_CONSTANT / wavelength)
        if wavelength is not None
        else (PLANCK_CONSTANT * frequency / SPEED_OF_LIGHT)
        if frequency is not None
        else (_ for _ in ()).throw(
            ValueError("Either 'wavelength' or 'frequency' must be provided.")
        )
    )


# **************************************************************************************
