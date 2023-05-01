"""
The previous standard epoch "J1900" was defined by international
agreement to be equivalent to: The Gregorian date January 0.5, 1900,
at 12:00 TT (Terrestrial Time), equivalent to noon on December 31, 1899.

The Julian date 2415020.0 TT (Terrestrial Time).
"""
J1900: float = 2415020.0

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

"""
The currently-used standard epoch "J2000" is defined by international 
agreement to be equivalent to: The Gregorian date January 1, 2000, 
at 12:00 TT (Terrestrial Time). 

The Julian date 2451545.0 TT (Terrestrial Time).
"""
J2000: float = 2451545.0
