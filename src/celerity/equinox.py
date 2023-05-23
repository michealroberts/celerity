# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from datetime import datetime, timezone

# *****************************************************************************************************************


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
    return datetime.utcfromtimestamp((JD - 2440587.5) * 86400).astimezone(
        tz=timezone.utc
    )


# *****************************************************************************************************************
