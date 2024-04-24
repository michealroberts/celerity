# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime, timezone

# **************************************************************************************


def get_spring_equinox(year: int) -> datetime:
    """
    Get the datetime of the spring equinox for the given year.

    :param year: The year to get the spring equinox for.
    :return: The datetime of the spring equinox for the given year.
    """
    T = year / 1000

    # Get the Julian date of the spring equinox (using Meeus' formula):
    JD = (
        1721139.2855 + 365.2421376 * year + 0.067919 * pow(T, 2) - 0.0027879 * pow(T, 3)
    )

    # Convert the Julian date to a datetime UTC object:
    return datetime.fromtimestamp((JD - 2440587.5) * 86400).astimezone(tz=timezone.utc)


# **************************************************************************************


def get_autumn_equinox(year: int) -> datetime:
    """
    Get the datetime of the autumn equinox for the given year.

    :param year: The year to get the autumn equinox for.
    :return: The datetime of the autumn equinox for the given year.
    """
    T = year / 1000

    # Get the Julian date of the autumn equinox (using Meeus' formula):
    JD = (
        1721325.6978 + 365.2425055 * year - 0.126689 * pow(T, 2) + 0.0019401 * pow(T, 3)
    )

    # Convert the Julian date to a datetime UTC object:
    return datetime.fromtimestamp((JD - 2440587.5) * 86400).astimezone(tz=timezone.utc)


# **************************************************************************************
