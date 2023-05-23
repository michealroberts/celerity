# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from datetime import datetime, timezone

# *****************************************************************************************************************


def get_summer_solstice(year: int) -> datetime:
    """
    Get the datetime of the summer solstice for the given year.

    :param year: The year to get the summer solstice for.
    :return: The datetime of the summer solstice for the given year.
    """
    T = year / 1000

    # Get the Julian date of the summer solstice (using Meeus' formula):
    JD = 1721233.2486 + 365.2417284 * year - 0.053018 * pow(T, 2) + 0.009332 * pow(T, 3)

    # Convert the Julian date to a datetime UTC object:
    return datetime.utcfromtimestamp((JD - 2440587.5) * 86400).astimezone(
        tz=timezone.utc
    )


# *****************************************************************************************************************
