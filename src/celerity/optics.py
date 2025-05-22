# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from typing import Optional, TypedDict

# **************************************************************************************


class Transmission(TypedDict):
    # The transmission coefficient of an optical element, which is the fraction of light
    # that passes through the element. This is typically a value between 0 and 1.
    # A value of 1 means that all light passes through the element, while a value of 0
    # means that no light passes through:
    coefficient: float


# **************************************************************************************


class SurfaceReflectance(TypedDict):
    # The albedo of a reflecting surface, which is the fraction of light that is
    # reflected by the surface (e.g., the primary mirror of a telescope). This is
    # typically a value between 0 and 1. A value of 1 means that all light is reflected
    # (perfect reflector) by the surface, while a value of 0 means that no light is
    # reflected (black body):
    albedo: float


# **************************************************************************************


def get_optical_system_throughput(
    primary: SurfaceReflectance,
    secondary: Optional[SurfaceReflectance] = None,
    *,
    lens: Transmission,
    filter: Transmission,
    QE: float,
) -> float:
    """
    Calculate the throughput of the optical system. The throughput is the product of the
    reflectivity of the primary and secondary mirrors, the transmission of the
    optical elements (if present), and the quantum efficiency (QE) of the detector.

    :param primary: The primary mirror of the telescope.
    :param secondary: The secondary mirror of the telescope (if present).
    :param lens: The transmission coefficient of the lens.
    :param filter: The transmission coefficient of the filter.
    :param QE: The quantum efficiency of the detector (as a fraction of the incident light).
    :return: The throughput of the optical system (as a fraction of the incident light).
    :raises ValueError: If the reflectivity of the primary or secondary mirror is not
        between 0 and 1, or if the transmission coefficient of the lens or filter is not
        between 0 and 1, or if the quantum efficiency (QE) is not between 0 and 1.
    """
    # The reflectivity of the primary mirror is the fraction of light that is reflected
    # by the primary mirror. This is typically a value between 0 and 1. A value of 1 means
    # that all light is reflected by the primary mirror, while a value of 0 means that no
    # light is reflected:
    R1 = primary["albedo"]

    # The secondary mirror is optional, so if it is not present, we assume a reflectivity
    # of 1 (i.e., no loss):
    R2 = secondary["albedo"] if secondary is not None else 1.0

    # Sense check that the reflectivity of the primary mirror is fractional:
    if R1 < 0 or R1 > 1:
        raise ValueError("Reflectivity of primary mirror must be between 0 and 1.")

    # Sense check that the reflectivity of the secondary mirror is fractional:
    if R2 < 0 or R2 > 1:
        raise ValueError("Reflectivity of secondary mirror must be between 0 and 1.")

    L = lens.get("coefficient", 1)

    f = filter.get("coefficient", 1)

    # Sense check that the transmission coefficient of the lens is fractional:
    if L < 0 or L > 1:
        raise ValueError("Transmission coefficient of lens must be between 0 and 1.")

    # Sense check that the transmission coefficient of the filter is fractional:
    if f < 0 or f > 1:
        raise ValueError("Transmission coefficient of filter must be between 0 and 1.")

    # Sense check that the quantum efficiency (QE) is fractional, e.g., between 0 and 1:
    if QE < 0 or QE > 1:
        raise ValueError("Quantum efficiency (QE) must be between 0 and 1.")

    # The transmission of the optical elements is the fraction of light that passes
    # through the optical elements. This is typically a value between 0 and 1. A value of
    # 1 means that all light passes through the optical elements, while a value of 0 means
    # that no light passes through the optical elements:
    return R1 * R2 * L * f * QE


# **************************************************************************************
