# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import radians

# **************************************************************************************

"""
The previous standard epoch "J1900" was defined by international
agreement to be equivalent to: The Gregorian date January 0.5, 1900,
at 12:00 TT (Terrestrial Time), equivalent to noon on December 31, 1899.

The Julian date 2415020.0 TT (Terrestrial Time).
"""

J1900: float = 2415020.0

# **************************************************************************************

"""
The standard epoch "J1970" is defined by international agreement to be
equivalent to: The Gregorian date January 1, 1970, at 00:00 TT
(Terrestrial Time).

The Julian date 2440587.5 TT (Terrestrial Time).

This is useful because it is the "epoch" referenced to the Unix 0 
time system. The Unix time 0 is exactly midnight UTC on 1 January 
1970, with Unix time incrementing by 1 for every non-leap second 
after this.
"""
J1970: float = 2440587.5

# **************************************************************************************

"""
The currently-used standard epoch "J2000" is defined by international 
agreement to be equivalent to: The Gregorian date January 1, 2000, 
at 12:00 TT (Terrestrial Time). 

The Julian date 2451545.0 TT (Terrestrial Time).
"""
J2000: float = 2451545.0

# **************************************************************************************

"""
The speed of light in a vacuum is defined to be exactly 299,792,458 m/s.
"""
c = 299_792_458 

# **************************************************************************************

"""
The Planck constant is defined to be exactly 6.62607015 × 10^-34 J·s.
"""
h = 6.626_070_15e-34

# **************************************************************************************

"""
The astronomical unit (AU) is a unit of length used in astronomy.

It is defined as the mean distance from the Earth to the Sun.
"""
AU = 149597870700.0

# **************************************************************************************

"""
A parsec (short for "parallax second") is a unit of distance used in astronomy

It is defined as the distance at which one astronomical unit subtends an angle of one arcsecond.
"""
PARSEC = AU / radians(1 / 3600)

# **************************************************************************************