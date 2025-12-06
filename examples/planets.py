# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime, timezone

from celerity.common import (
    GeographicCoordinate,
    HeliocentricSphericalCoordinate,
)
from celerity.coordinates import (
    convert_equatorial_to_horizontal,
    convert_heliocentric_to_equatorial,
)
from celerity.planet import Planet
from celerity.planets import get_planetary_heliocentric_coordinate
from celerity.refraction import get_correction_to_horizontal_for_refraction

# **************************************************************************************


def main() -> None:
    date = datetime(2025, 12, 6, 0, 0, 0, 0, tzinfo=timezone.utc)

    observer: GeographicCoordinate = {
        "latitude": 19.820611,
        "longitude": -155.468094,
    }

    venus: HeliocentricSphericalCoordinate = get_planetary_heliocentric_coordinate(
        date, Planet.VENUS
    )

    equatorial = convert_heliocentric_to_equatorial(date, venus)

    # N.B. You can apply further refraction corrections to the horizontal
    # coordinate if desired after this step:
    horizontal = convert_equatorial_to_horizontal(
        date,
        observer,
        equatorial,
    )

    # Apply atmospheric refraction correction to the horizontal coordinates:
    topocentric = get_correction_to_horizontal_for_refraction(horizontal)

    # Apply formatting to 6 decimal places for display:
    print(f"Altitude: {topocentric['alt']:.6f}°")
    print(f"Azimuth:  {topocentric['az']:.6f}°")


# **************************************************************************************

if __name__ == "__main__":
    main()

# **************************************************************************************
