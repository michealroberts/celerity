# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from datetime import datetime
from math import cos, radians, sin, tan

from .common import EquatorialCoordinate
from .temporal import get_julian_date

# **************************************************************************************


def get_correction_to_equatorial_for_precession_of_equinoxes(
    date: datetime,
    target: EquatorialCoordinate,
) -> EquatorialCoordinate:
    """
    Corrects the equatorial coordinates of a target for the precession of the equinoxes.

    :param date: The date to correct the equatorial coordinates for.
    :param target: The equatorial J2000 coordinates of the target.
    :return: The corrected equatorial coordinates of the target.
    """
    ra, dec = radians(target["ra"]), radians(target["dec"])

    # Get the Julian date:
    JD = get_julian_date(date)

    # Get the difference in fractional Julian centuries between the target date and J2000.0
    T = (JD - 2451545.0) / 36525

    # Interpolate the precession in right ascension (in seconds*)
    M = 3.07234 + 0.00186 * T

    # Interpolate the precession in declination (in arcseconds)
    Nd = 20.0468 - 0.0085 * T

    # Calculate the precession correction in right ascension (in seconds*)
    Δra = M + Nd / 15 * sin(ra) * tan(dec) * T

    # Calculate the precession correction in declination (in arcseconds)
    Δdec = Nd * cos(ra) * T

    return {"ra": Δra / (3600 / 15), "dec": Δdec / 3600}


# **************************************************************************************
