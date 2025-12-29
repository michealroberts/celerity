# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from enum import Enum
from typing import Dict

# **************************************************************************************


class Planet(Enum):
    MERCURY = "Mercury"
    VENUS = "Venus"
    EARTH = "Earth"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"


# **************************************************************************************

"""
Maps NAIF (Navigation and Ancillary Information Facility) planetary barycenter IDs to 
their corresponding Planet enum values. These IDs are used in the SPICE toolkit for 
astronomical calculations and ephemeris data.
"""
NAIF_PLANETARY_BARYCENTER_ID_TO_PLANET: Dict[int, Planet] = {
    # Mercury Barycenter:
    1: Planet.MERCURY,
    # Venus Barycenter:
    2: Planet.VENUS,
    # Earth-Moon Barycenter:
    3: Planet.EARTH,
    # Mars Barycenter:
    4: Planet.MARS,
    # Jupiter Barycenter:
    5: Planet.JUPITER,
    # Saturn Barycenter:
    6: Planet.SATURN,
    # Uranus Barycenter:
    7: Planet.URANUS,
    # Neptune Barycenter:
    8: Planet.NEPTUNE,
}

# **************************************************************************************
