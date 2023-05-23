# *****************************************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# *****************************************************************************************************************

from datetime import datetime, timedelta
from math import radians
from typing import List, Optional, Tuple

from .common import GeographicCoordinate, HorizontalCoordinate
from .coordinates import convert_equatorial_to_horizontal
from .refraction import get_correction_to_horizontal_for_refraction
from .sun import get_equatorial_coordinate

# *****************************************************************************************************************


def get_solar_transit(
    date: datetime, observer: GeographicCoordinate, horizon: float = 0
) -> Tuple[Optional[datetime], Optional[datetime], Optional[datetime]]:
    # Set the date to be at 1 minute before midnight for the previous date:
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)

    # Cycle through the day in 1 second intervals to construct a list of
    # the Sun's altitude at each second:
    sun: List[HorizontalCoordinate] = []

    rise: Optional[int] = None

    set: Optional[int] = None

    for i in range(1440):
        # Get the Sun's equatorial coordinate:
        eq = get_equatorial_coordinate(date)

        # Convert the equatorial coordinate to a horizontal coordinate:
        hor = convert_equatorial_to_horizontal(date, observer, eq)

        # Correct the horizontal coordinate for atmospheric refraction:
        hor = get_correction_to_horizontal_for_refraction(hor, 288.15, 101325)

        # Find the altitude of the Sun where it crosses over the horizon:
        if hor["alt"] > horizon and rise is None:
            rise = i

        # Find the altitude of the Sun where it crosses back under the horizon:
        if hor["alt"] < horizon and set is None and rise is not None:
            set = i

        sun.append(hor)

        # Increment the date by 1 second:
        date += timedelta(minutes=1)

    # Find the index of the maximum altitude:
    noon = max(range(len(sun)), key=lambda i: sun[i]["alt"])

    date = date - timedelta(minutes=1440)

    # Get the time of the maximum altitude:
    transit = date.replace(hour=0, minute=0, second=0) + timedelta(minutes=noon)

    # Get the time of the sunrise:
    if rise is not None:
        sunrise = date.replace(hour=0, minute=0, second=0) + timedelta(minutes=rise)
    else:
        sunrise = None

    # Get the time of the sunset:
    if set is not None:
        sunset = date.replace(hour=0, minute=0, second=0) + timedelta(minutes=set)
    else:
        sunset = None

    return sunrise, transit, sunset


# *****************************************************************************************************************


def is_night(
    date: datetime, observer: GeographicCoordinate, horizon: float = 0
) -> bool:
    """
    Determine if the Sun is below the horizon at the given datetime and location.

    :param date: The datetime to check.
    :param observer: The geographic coordinates of the observer.
    :param horizon: The altitude of the horizon in degrees.
    """

    # Get the time of the sunset for the given date:
    sunrise, _, sunset = get_solar_transit(date, observer, horizon)

    if (sunrise is not None and date < sunrise) or (
        sunset is not None and date > sunset
    ):
        return True

    return False


# *****************************************************************************************************************
