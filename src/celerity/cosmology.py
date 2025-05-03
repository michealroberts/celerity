# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from math import sqrt

from .common import Measurement
from .constants import (
    H0_PLANCK_2018,
    PARSEC,
    c,
)
from .integration import perform_definite_integral

# **************************************************************************************


def get_hubble_parameter(redshift: float) -> float:
    """
    Dimensionless Hubble parameter E(z) for flat ΛCDM cosmology, e.g., Ωk = 0.

    :param z: Redshift (z), must be >= 0.
    :return: Dimensionless Hubble parameter E(z).
    :raises ValueError: If z is negative.
    """
    if redshift < 0:
        raise ValueError("Redshift must be non-negative.")

    # The agreed upon matter density parameter (Ωm):
    OMEGA_M = 0.3153

    # The agreed upon dark energy density parameter (ΩΛ):
    OMEGA_LAMBDA = 0.6847

    # The agreed upon radiation density parameter (Ωr):
    OMEGA_R = 9.167e-5

    # The sum of the density parameters must approximately equal 1 for a flat universe:
    assert abs(OMEGA_M + OMEGA_LAMBDA + OMEGA_R - 1.0) < 1e-3, (
        "Density parameters must sum to 1."
    )

    return sqrt(
        OMEGA_R * pow(1 + redshift, 4) + OMEGA_M * pow(1 + redshift, 3) + OMEGA_LAMBDA
    )


# **************************************************************************************

# Alias for the dimensionless Hubble parameter function `get_hubble_parameter`:
e_z = get_hubble_parameter

# **************************************************************************************


def get_comoving_distance(z: float, H: Measurement = H0_PLANCK_2018) -> Measurement:
    """
    Comoving distance D_C(z) in meters.

    Args:
        z: Redshift (z), must be >= 0.
        H: Measurement of the Hubble constant (H0) in km/s/Mpc with its associated uncertainty.

    Returns:
        Measurement: Comoving distance in meters with its associated uncertainty.

    Raises:
        ValueError: If z is negative.
        ValueError: If the Hubble constant is not positive.
    """
    if z < 0:
        raise ValueError("Redshift must be non-negative.")

    # Calculate the Hubble constant in units of 1/s:
    H0 = (H["value"] * 1_000) / (1e6 * PARSEC)

    # Sense check that the Hubble constant is positive:
    if H0 <= 0:
        raise ValueError("Hubble constant must be positive.")

    # Calculate the uncertainty in Hubble constant in units of 1/s:
    H0_uncertainty = (H.get("uncertainty", 0.0) * 1_000) / (1e6 * PARSEC)

    def integrand(x: float) -> float:
        return 1.0 / get_hubble_parameter(x)

    d_c = perform_definite_integral(f=integrand, a=0.0, b=z, n=256)

    # Calculate the uncertainty in the comoving distance in meters:
    d_c_uncertainty = (
        (c * d_c * H0_uncertainty) / (pow(H0, 2)) if H0_uncertainty > 0 else 0.0
    )

    return Measurement(
        {
            "value": (c * d_c) / H0,
            "uncertainty": d_c_uncertainty,
        }
    )


# **************************************************************************************


def get_luminosity_distance(z: float, H: Measurement = H0_PLANCK_2018) -> Measurement:
    """
    Luminosity distance D_L(z) = (1 + z) · D_C(z), in meters.

    Args:
        z: Redshift (z), must be >= 0.
        H: Measurement of the Hubble constant (H0) in km/s/Mpc with its associated uncertainty.

    Returns:
        Measurement: Luminosity distance in meters with its associated uncertainty.

    Raises:
        ValueError: If z is negative.
        ValueError: If the Hubble constant is not positive.
    """
    if z < 0:
        raise ValueError("Redshift must be non-negative.")

    # Compute comoving distance (with its propagated uncertainty)
    d = get_comoving_distance(z, H)

    return Measurement(
        {
            "value": (1.0 + z) * d["value"],
            "uncertainty": (1.0 + z) * d.get("uncertainty", 0.0),
        }
    )


# **************************************************************************************


def get_angular_diameter_distance(
    z: float, H: Measurement = H0_PLANCK_2018
) -> Measurement:
    """
    Angular diameter distance D_A(z) = D_C(z) / (1 + z), in meters.

    Args:
        z: Redshift (z), must be >= 0.
        H: Measurement of the Hubble constant (H0) in km/s/Mpc with its associated uncertainty.

    Returns:
        Measurement: Angular diameter distance in meters with its associated uncertainty.

    Raises:
        ValueError: If z is negative.
        ValueError: If the Hubble constant is not positive.
    """
    if z < 0:
        raise ValueError("Redshift must be non-negative.")

    # Compute comoving distance (with its propagated uncertainty)
    d = get_comoving_distance(z, H)

    return Measurement(
        {
            "value": d["value"] / (1.0 + z),
            "uncertainty": d.get("uncertainty", 0.0) / (1.0 + z),
        }
    )


# **************************************************************************************
