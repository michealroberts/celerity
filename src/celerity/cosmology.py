# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from math import sqrt

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

    print(1 - OMEGA_M - OMEGA_LAMBDA)

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
