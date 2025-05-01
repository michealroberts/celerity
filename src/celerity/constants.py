# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2023 observerly

# **************************************************************************************

from math import radians
from typing import Final

from .common import Measurement

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

"""
The Hubble constant (H0) is the current rate of expansion of the universe.

It is defined as the ratio of the velocity of a galaxy to its distance from us.

The Hubble constant is usually expressed in units of kilometers per second per 
megaparsec (km/s/Mpc).

Planck 2018 value: 67.74 ± 0.46 km/s/Mpc
"""
H0_PLANCK_2018: Final[Measurement] = Measurement(
    {
        "value": 67.74,
        "uncertainty": 0.46,
    }
)

# **************************************************************************************

"""
SH0ES 2022 value: 73.04 ± 1.04 km/s/Mpc

The SH0ES (Supernovae, H0, and the Equation of State) collaboration is a team of
astronomers who are measuring the Hubble constant using Type Ia supernovae as
standard candles. The SH0ES team has been working on this problem for over a decade
and has made significant progress in measuring the Hubble constant with high precision.

N.B. The SH0ES team uses a variety of methods to measure the Hubble constant, including
the use of Cepheid variables, Type Ia supernovae, and gravitational lensing.
"""
H0_SH0ES_2022: Final[Measurement] = Measurement(
    {
        "value": 73.04,
        "uncertainty": 1.04,
    }
)

# **************************************************************************************

"""
The IAU (International Astronomical Union) has adopted a value of
the Hubble constant of 70.0 km/s/Mpc for use in cosmological calculations.
"""
H0_IAU_REFERENCE: Final[Measurement] = Measurement(
    {
        "value": 70.0,
        "uncertainty": 2.0,
    }
)

# **************************************************************************************
