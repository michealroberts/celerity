# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timezone
from math import cos, radians
from typing import TypedDict

import pytest

from src.celerity.aberration import get_correction_to_equatorial_for_aberration
from src.celerity.common import EquatorialCoordinate
from src.celerity.coordinates import get_correction_to_equatorial
from src.celerity.deflection import get_correction_to_equatorial_for_light_deflection
from src.celerity.nutation import (
    get_correction_to_equatorial_for_nutation,
    get_nutation_in_longitude,
    get_nutation_in_obliquity,
)
from src.celerity.precession import (
    get_correction_to_equatorial_for_precession_of_equinoxes,
)

# **************************************************************************************

# The reference values below were evaluated once with pyerfa 2.0.1.5 (ERFA, the IAU SOFA
# derivative) using the IAU 2006/2000A models, with UTC converted to TT via utctai and
# taitt. Nutation components come from nut06a, the nutation correction from num06a, the
# precession correction from the rp matrix of bp06, the true place from num06a and rp
# applied in turn, the aberration correction from ab applied to that true place with the
# Earth's heliocentric velocity and distance from epv00 rotated into the same frame, so
# that it isolates annual aberration, the light deflection from ldsun applied to that
# true place with the Earth's heliocentric direction and distance from epv00 rotated
# into the same frame, and the apparent place from atci13, which includes
# the Sun's barycentric motion, with the equation of the origins subtracted to give the
# equinox-based right ascension.

# **************************************************************************************

# The tolerances below are on the sky. When applied to a right ascension they are
# divided by the cosine of the declination, since a given separation on the sky spans
# more right ascension close to the celestial poles.

# **************************************************************************************

# The tolerance on the nutation in longitude and obliquity, and on the nutation
# correction to an equatorial coordinate:
TOLERANCE_IN_NUTATION: float = 0.001 / 3600

# **************************************************************************************

# The tolerance on the precession correction to an equatorial coordinate:
TOLERANCE_IN_PRECESSION: float = 0.00001 / 3600

# **************************************************************************************

# The tolerance on the aberration correction to an equatorial coordinate:
TOLERANCE_IN_ABERRATION: float = 0.0002 / 3600

# **************************************************************************************

# The tolerance on the light deflection correction to an equatorial coordinate:
TOLERANCE_IN_LIGHT_DEFLECTION: float = 0.00001 / 3600

# **************************************************************************************

# The tolerance on the apparent place, i.e. the precession, nutation and aberration
# corrections applied in turn:
TOLERANCE_IN_APPARENT_PLACE: float = 0.012 / 3600

# **************************************************************************************


class NutationScenario(TypedDict):
    date: datetime
    Δψ: float
    Δε: float


# **************************************************************************************


class Scenario(TypedDict):
    date: datetime
    target: EquatorialCoordinate
    nutation: EquatorialCoordinate
    precession: EquatorialCoordinate
    true_place: EquatorialCoordinate
    deflection: EquatorialCoordinate
    aberration: EquatorialCoordinate
    apparent: EquatorialCoordinate


# **************************************************************************************

nutations: list[NutationScenario] = [
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "Δψ": -0.003869999279056249,
        "Δε": -0.0016026148146560315,
    },
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "Δψ": 0.004629796231811693,
        "Δε": 0.00042827265411278845,
    },
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "Δψ": -0.004863778935594231,
        "Δε": 0.0007474043457538264,
    },
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "Δψ": 0.0024661472297875784,
        "Δε": 0.002337817578678058,
    },
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "Δψ": -0.004330045827874393,
        "Δε": 0.0006657288862574993,
    },
]

# **************************************************************************************

scenarios: list[Scenario] = [
    # Betelgeuse on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.78921196601357, "dec": 7.405429164798},
        "precession": {"ra": 88.79295832752871, "dec": 7.407063900238369},
        "true_place": {"ra": 88.78921199354218, "dec": 7.405429165037095},
        "deflection": {"ra": 88.78921211250773, "dec": 7.405429326297917},
        "aberration": {"ra": 88.79493251107225, "dec": 7.405156041710694},
        "apparent": {"ra": 88.79493424918059, "dec": 7.405153500675567},
    },
    # Vega on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23261171404425, "dec": 38.78502374271821},
        "precession": {"ra": 279.2347348170764, "dec": 38.78368890181726},
        "true_place": {"ra": 279.23261173112104, "dec": 38.78502374453494},
        "deflection": {"ra": 279.23261163905437, "dec": 38.78502566336775},
        "aberration": {"ra": 279.22520401967074, "dec": 38.78467903580393},
        "apparent": {"ra": 279.22521368176695, "dec": 38.78467974005863},
    },
    # Sirius on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28415219481592, "dec": -16.71738627503702},
        "precession": {"ra": 101.28715532272228, "dec": -16.716115902216348},
        "true_place": {"ra": 101.28415221753842, "dec": -16.717386277252643},
        "deflection": {"ra": 101.28415221754393, "dec": -16.717385861436068},
        "aberration": {"ra": 101.29017873358715, "dec": -16.717734180738205},
        "apparent": {"ra": 101.2901828949624, "dec": -16.717736410590707},
    },
    # Arcturus on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.9115857149967, "dec": 19.184581938028963},
        "precession": {"ra": 213.91530032385904, "dec": 19.182410290603585},
        "true_place": {"ra": 213.91158573885616, "dec": 19.18458192863275},
        "deflection": {"ra": 213.9115844361731, "dec": 19.184582632356665},
        "aberration": {"ra": 213.90906462741398, "dec": 19.182460779176964},
        "apparent": {"ra": 213.90907074576978, "dec": 19.182465497835448},
    },
    # Dubhe on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.92482412740236, "dec": 61.752136604477876},
        "precession": {"ra": 165.93196473117928, "dec": 61.751033089016616},
        "true_place": {"ra": 165.92482415858439, "dec": 61.75213659349555},
        "deflection": {"ra": 165.92482283863018, "dec": 61.752136471761844},
        "aberration": {"ra": 165.92971420457596, "dec": 61.74727975209001},
        "apparent": {"ra": 165.92971510248498, "dec": 61.74728517212735},
    },
    # Canopus on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98662772876203, "dec": -52.69713270672398},
        "precession": {"ra": 95.98794961127693, "dec": -52.69569940118136},
        "true_place": {"ra": 95.98662774003944, "dec": -52.69713270790499},
        "deflection": {"ra": 95.98662786967928, "dec": -52.69713181476643},
        "aberration": {"ra": 95.99613767251633, "dec": -52.69767027450793},
        "apparent": {"ra": 95.99614560795548, "dec": -52.697673307902555},
    },
    # Polaris on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 37.954588, "dec": 89.2641094},
        "nutation": {"ra": 37.97564162724737, "dec": 89.26190990211472},
        "precession": {"ra": 37.95458856824958, "dec": 89.26410940892804},
        "true_place": {"ra": 37.97564219410124, "dec": 89.26190991103962},
        "deflection": {"ra": 37.975694766913804, "dec": 89.26190957474108},
        "aberration": {"ra": 38.190449024238134, "dec": 89.26697760613199},
        "apparent": {"ra": 38.19017577785115, "dec": 89.26697243951237},
    },
    # Betelgeuse on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.79744428153295, "dec": 7.407530798507679},
        "precession": {"ra": 88.93443372339166, "dec": 7.408217067914066},
        "true_place": {"ra": 88.9389198915273, "dec": 7.408679441084388},
        "deflection": {"ra": 88.93892223578833, "dec": 7.408672247275327},
        "aberration": {"ra": 88.93329234284407, "dec": 7.408494665505916},
        "apparent": {"ra": 88.93329858012545, "dec": 7.4084849340507155},
    },
    # Vega on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23746677066043, "dec": 38.78356175291039},
        "precession": {"ra": 279.3224939660921, "dec": 38.79307153583077},
        "true_place": {"ra": 279.325225273466, "dec": 38.792947278259895},
        "deflection": {"ra": 279.3252250235286, "dec": 38.792946612238666},
        "aberration": {"ra": 279.33215966601296, "dec": 38.79183639647064},
        "apparent": {"ra": 279.33216640263987, "dec": 38.79183515610252},
    },
    # Sirius on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.29083556182613, "dec": -16.716056409531614},
        "precession": {"ra": 101.4039274437955, "dec": -16.72756360999897},
        "true_place": {"ra": 101.40760725864199, "dec": -16.727507971063808},
        "deflection": {"ra": 101.40760844902763, "dec": -16.727510501293256},
        "aberration": {"ra": 101.40202277651129, "dec": -16.728222530191484},
        "apparent": {"ra": 101.40203035029172, "dec": -16.72822727149572},
    },
    # Arcturus on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.9193142597776, "dec": 19.180643134021267},
        "precession": {"ra": 214.03791430424695, "dec": 19.134157766247363},
        "true_place": {"ra": 214.04192758694006, "dec": 19.132392042772366},
        "deflection": {"ra": 214.04192815913615, "dec": 19.13239160081225},
        "aberration": {"ra": 214.04572891691558, "dec": 19.133567001621795},
        "apparent": {"ra": 214.04573523622858, "dec": 19.133570238693768},
    },
    # Dubhe on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.93781857502174, "dec": 61.749350848365474},
        "precession": {"ra": 166.09202163893252, "dec": 61.69457083710985},
        "true_place": {"ra": 166.09786299344603, "dec": 61.692886181404745},
        "deflection": {"ra": 166.09786658037604, "dec": 61.69288602308627},
        "aberration": {"ra": 166.09620754180858, "dec": 61.697650879720634},
        "apparent": {"ra": 166.09621370571048, "dec": 61.697654358710324},
    },
    # Canopus on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98973495512033, "dec": -52.695465601589525},
        "precession": {"ra": 96.04590361199902, "dec": -52.70179949558628},
        "true_place": {"ra": 96.04768811393255, "dec": -52.70156759500961},
        "deflection": {"ra": 96.04768859288745, "dec": -52.701568969716085},
        "aberration": {"ra": 96.03864470363699, "dec": -52.70263501597931},
        "apparent": {"ra": 96.0386566039513, "dec": -52.70263970673901},
    },
    # Polaris on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 37.954588, "dec": 89.2641094},
        "nutation": {"ra": 38.020873942049946, "dec": 89.26582439610266},
        "precession": {"ra": 41.06164186040743, "dec": 89.3090177461639},
        "true_place": {"ra": 41.13959680046372, "dec": 89.31068699091685},
        "deflection": {"ra": 41.139500927944546, "dec": 89.31068825128548},
        "aberration": {"ra": 40.80112362133398, "dec": 89.30685189107007},
        "apparent": {"ra": 40.800811523787296, "dec": 89.30684995706551},
    },
    # Betelgeuse on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.7882422896919, "dec": 7.407770307191752},
        "precession": {"ra": 89.0821544191646, "dec": 7.409267715625173},
        "true_place": {"ra": 89.07743879933936, "dec": 7.409983955534076},
        "deflection": {"ra": 89.07744181312415, "dec": 7.409982826527021},
        "aberration": {"ra": 89.07286845405618, "dec": 7.409031800372237},
        "apparent": {"ra": 89.07287680897146, "dec": 7.409028101989159},
    },
    # Vega on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23171023673484, "dec": 38.782640780194775},
        "precession": {"ra": 279.4141278380687, "dec": 38.802961078161346},
        "true_place": {"ra": 279.41110161971534, "dec": 38.80190736053199},
        "deflection": {"ra": 279.411100831592, "dec": 38.801906802459484},
        "aberration": {"ra": 279.4161181445298, "dec": 38.79845344427226},
        "apparent": {"ra": 279.41612245746995, "dec": 38.798452235773844},
    },
    # Sirius on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28321858607794, "dec": -16.715004376824268},
        "precession": {"ra": 101.5258499602996, "dec": -16.73963933443159},
        "true_place": {"ra": 101.52191263275374, "dec": -16.738520526889268},
        "deflection": {"ra": 101.52191429309474, "dec": -16.73852157023231},
        "aberration": {"ra": 101.51797955738164, "dec": -16.740962788672032},
        "apparent": {"ra": 101.5179891361851, "dec": -16.740966112978835},
    },
    # Arcturus on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.9114290853619, "dec": 19.183598711079355},
        "precession": {"ra": 214.16593623802666, "dec": 19.083855346393335},
        "true_place": {"ra": 214.1620635408431, "dec": 19.08503631139481},
        "deflection": {"ra": 214.16206372685122, "dec": 19.08503592924557},
        "aberration": {"ra": 214.16746936486803, "dec": 19.084390431455915},
        "apparent": {"ra": 214.16747468800256, "dec": 19.08439322352507},
    },
    # Dubhe on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.92797622503213, "dec": 61.7530912748933},
        "precession": {"ra": 166.25876265809313, "dec": 61.635581251157504},
        "true_place": {"ra": 166.25479363789188, "dec": 61.63763793987638},
        "deflection": {"ra": 166.25479585609864, "dec": 61.63763731688821},
        "aberration": {"ra": 166.25895690201443, "dec": 61.64147895979464},
        "apparent": {"ra": 166.258963006501, "dec": 61.64148076730824},
    },
    # Canopus on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98590989767034, "dec": -52.694754299546005},
        "precession": {"ra": 96.1064150953546, "dec": -52.70823059471847},
        "true_place": {"ra": 96.10437392137004, "dec": -52.70728167948718},
        "deflection": {"ra": 96.10437538135893, "dec": -52.70728263712903},
        "aberration": {"ra": 96.09756718954092, "dec": -52.710961160311506},
        "apparent": {"ra": 96.09758248364211, "dec": -52.71096559211423},
    },
    # Polaris on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 37.954588, "dec": 89.2641094},
        "nutation": {"ra": 37.81181600181118, "dec": 89.26304150486922},
        "precession": {"ra": 44.74527154349368, "dec": 89.3535374020311},
        "true_place": {"ra": 44.57329424630562, "dec": 89.35268672705091},
        "deflection": {"ra": 44.5732784445011, "dec": 89.35268829389221},
        "aberration": {"ra": 44.09810497394644, "dec": 89.35165441604757},
        "apparent": {"ra": 44.09791226300754, "dec": 89.35165417869038},
    },
    # Betelgeuse on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.79534209862399, "dec": 7.409421842086958},
        "precession": {"ra": 89.15439012776993, "dec": 7.4097244309518375},
        "true_place": {"ra": 89.15677590262463, "dec": 7.412076450269756},
        "deflection": {"ra": 89.15677460877598, "dec": 7.41207639322137},
        "aberration": {"ra": 89.15606956480866, "dec": 7.413622936936283},
        "apparent": {"ra": 89.1560697011673, "dec": 7.413621056513292},
    },
    # Vega on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23591806196885, "dec": 38.78153880849428},
        "precession": {"ra": 279.4589372623369, "dec": 38.8078315592837},
        "true_place": {"ra": 279.46011283453913, "dec": 38.80568674082442},
        "deflection": {"ra": 279.4601139824787, "dec": 38.8056865192853},
        "aberration": {"ra": 279.46218052524716, "dec": 38.81052457424408},
        "apparent": {"ra": 279.46219234825406, "dec": 38.81052597738137},
    },
    # Sirius on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28899170225554, "dec": -16.714015307026486},
        "precession": {"ra": 101.58546871130743, "dec": -16.745589989638383},
        "true_place": {"ra": 101.58730103260294, "dec": -16.74349681585499},
        "deflection": {"ra": 101.58729944697265, "dec": -16.74349706603443},
        "aberration": {"ra": 101.58542807631414, "dec": -16.739954507756604},
        "apparent": {"ra": 101.5854297909043, "dec": -16.73995536264618},
    },
    # Arcturus on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.91804747257032, "dec": 19.18029184123591},
        "precession": {"ra": 214.2285375741675, "dec": 19.059287226843605},
        "true_place": {"ra": 214.23127738596972, "dec": 19.05716118585187},
        "deflection": {"ra": 214.23128021579035, "dec": 19.057161917098128},
        "aberration": {"ra": 214.22723972671082, "dec": 19.06042353424424},
        "apparent": {"ra": 214.22724749380075, "dec": 19.060430107624352},
    },
    # Dubhe on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.93889163936203, "dec": 61.75064974432048},
        "precession": {"ra": 166.340158254035, "dec": 61.60672241701942},
        "true_place": {"ra": 166.3470519764673, "dec": 61.606321217642396},
        "deflection": {"ra": 166.34705149211814, "dec": 61.60632322117012},
        "aberration": {"ra": 166.33615495923084, "dec": 61.606976747915475},
        "apparent": {"ra": 166.33615049738535, "dec": 61.606984471981114},
    },
    # Canopus on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98861187366724, "dec": -52.69347667022211},
        "precession": {"ra": 96.13600501453601, "dec": -52.71139836664715},
        "true_place": {"ra": 96.13665884128419, "dec": -52.70917879525964},
        "deflection": {"ra": 96.13665684601828, "dec": -52.70917908466293},
        "aberration": {"ra": 96.13447762353236, "dec": -52.70382474997525},
        "apparent": {"ra": 96.13448251348838, "dec": -52.70382587533667},
    },
    # Polaris on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 37.954588, "dec": 89.2641094},
        "nutation": {"ra": 37.86001660008947, "dec": 89.26631964700023},
        "precession": {"ra": 46.72977875760054, "dec": 89.3742717661809},
        "true_place": {"ra": 46.650407760039656, "dec": 89.37664572221193},
        "deflection": {"ra": 46.650318709096304, "dec": 89.37664503596963},
        "aberration": {"ra": 46.921233324979006, "dec": 89.37238989072334},
        "apparent": {"ra": 46.92087438331386, "dec": 89.37238272669086},
    },
    # Betelgeuse on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.78875975596036, "dec": 7.407693141977986},
        "precession": {"ra": 89.33441537814454, "dec": 7.410699611663397},
        "true_place": {"ra": 89.33021750539476, "dec": 7.41134522822122},
        "deflection": {"ra": 89.33021761697647, "dec": 7.411345389152925},
        "aberration": {"ra": 89.33594820830722, "dec": 7.411070450488347},
        "apparent": {"ra": 89.33595133337457, "dec": 7.411069348034825},
    },
    # Vega on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.2320418878248, "dec": 38.78275548230243},
        "precession": {"ra": 279.57061184986486, "dec": 38.82006824209901},
        "true_place": {"ra": 279.56791617823893, "dec": 38.819125502570124},
        "deflection": {"ra": 279.56791611154523, "dec": 38.81912742079873},
        "aberration": {"ra": 279.56050867748235, "dec": 38.81881876411773},
        "apparent": {"ra": 279.56051770316, "dec": 38.81882421728263},
    },
    # Sirius on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28365044265645, "dec": -16.71512604352434},
        "precession": {"ra": 101.73404564040234, "dec": -16.760550439905966},
        "true_place": {"ra": 101.73053976147338, "dec": -16.759548458008314},
        "deflection": {"ra": 101.73053975410389, "dec": -16.759548041550183},
        "aberration": {"ra": 101.73656217182581, "dec": -16.759871089358693},
        "apparent": {"ra": 101.73656666840577, "dec": -16.75986991777819},
    },
    # Arcturus on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.91185388901258, "dec": 19.183467961007704},
        "precession": {"ra": 214.38454780761546, "dec": 18.998144254178918},
        "true_place": {"ra": 214.38109891155486, "dec": 18.999189486242344},
        "deflection": {"ra": 214.3810975985727, "dec": 18.999190204326727},
        "aberration": {"ra": 214.37851987850914, "dec": 18.997100705997802},
        "apparent": {"ra": 214.37852099802825, "dec": 18.997107937842106},
    },
    # Dubhe on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.9284145371366, "dec": 61.75286533485002},
        "precession": {"ra": 166.54261090701067, "dec": 61.53476452894888},
        "true_place": {"ra": 166.539092938958, "dec": 61.536594239131496},
        "deflection": {"ra": 166.53909161488733, "dec": 61.536594126744816},
        "aberration": {"ra": 166.54379393385946, "dec": 61.53172399906447},
        "apparent": {"ra": 166.54378573736417, "dec": 61.53172829484439},
    },
    # Canopus on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98613338492508, "dec": -52.69485768593339},
        "precession": {"ra": 96.20974787150101, "dec": -52.71935865153635},
        "true_place": {"ra": 96.20792920825247, "dec": -52.71851058272656},
        "deflection": {"ra": 96.20792932695598, "dec": -52.71850968881974},
        "aberration": {"ra": 96.21744270064512, "dec": -52.719012008243084},
        "apparent": {"ra": 96.21745192842363, "dec": -52.71900991699314},
    },
    # Polaris on 2040-01-01:
    {
        "date": datetime(2040, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 37.954588, "dec": 89.2641094},
        "nutation": {"ra": 37.827450440859835, "dec": 89.26315925271453},
        "precession": {"ra": 52.26167757899489, "dec": 89.42240043034538},
        "true_place": {"ra": 52.08236611489837, "dec": 89.42187013561202},
        "deflection": {"ra": 52.08242274225688, "dec": 89.42186964172167},
        "aberration": {"ra": 52.47309955053321, "dec": 89.4260942346596},
        "apparent": {"ra": 52.47303359400899, "dec": 89.42608708628741},
    },
]

# **************************************************************************************


@pytest.mark.parametrize("scenario", nutations)
def test_get_nutation_in_longitude(scenario: NutationScenario) -> None:
    assert get_nutation_in_longitude(scenario["date"]) == pytest.approx(
        scenario["Δψ"], abs=TOLERANCE_IN_NUTATION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", nutations)
def test_get_nutation_in_obliquity(scenario: NutationScenario) -> None:
    assert get_nutation_in_obliquity(scenario["date"]) == pytest.approx(
        scenario["Δε"], abs=TOLERANCE_IN_NUTATION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial_for_nutation(scenario: Scenario) -> None:
    target = scenario["target"]

    correction = get_correction_to_equatorial_for_nutation(scenario["date"], target)

    assert target["ra"] + correction["ra"] == pytest.approx(
        scenario["nutation"]["ra"],
        abs=TOLERANCE_IN_NUTATION / cos(radians(scenario["nutation"]["dec"])),
    )
    assert target["dec"] + correction["dec"] == pytest.approx(
        scenario["nutation"]["dec"], abs=TOLERANCE_IN_NUTATION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial_for_precession_of_equinoxes(
    scenario: Scenario,
) -> None:
    target = scenario["target"]

    correction = get_correction_to_equatorial_for_precession_of_equinoxes(
        scenario["date"], target
    )

    assert target["ra"] + correction["ra"] == pytest.approx(
        scenario["precession"]["ra"],
        abs=TOLERANCE_IN_PRECESSION / cos(radians(scenario["precession"]["dec"])),
    )
    assert target["dec"] + correction["dec"] == pytest.approx(
        scenario["precession"]["dec"], abs=TOLERANCE_IN_PRECESSION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial_for_aberration(scenario: Scenario) -> None:
    # Aberration is applied to the true place of date, as in the apparent place chain:
    target = scenario["true_place"]

    correction = get_correction_to_equatorial_for_aberration(scenario["date"], target)

    assert target["ra"] + correction["ra"] == pytest.approx(
        scenario["aberration"]["ra"],
        abs=TOLERANCE_IN_ABERRATION / cos(radians(scenario["aberration"]["dec"])),
    )
    assert target["dec"] + correction["dec"] == pytest.approx(
        scenario["aberration"]["dec"], abs=TOLERANCE_IN_ABERRATION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial_for_light_deflection(scenario: Scenario) -> None:
    # Light deflection is applied to the true place of date, as in the apparent place
    # chain:
    target = scenario["true_place"]

    correction = get_correction_to_equatorial_for_light_deflection(
        scenario["date"], target
    )

    assert target["ra"] + correction["ra"] == pytest.approx(
        scenario["deflection"]["ra"],
        abs=TOLERANCE_IN_LIGHT_DEFLECTION / cos(radians(scenario["deflection"]["dec"])),
    )
    assert target["dec"] + correction["dec"] == pytest.approx(
        scenario["deflection"]["dec"], abs=TOLERANCE_IN_LIGHT_DEFLECTION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial(scenario: Scenario) -> None:
    apparent = get_correction_to_equatorial(scenario["date"], {**scenario["target"]})

    assert apparent["ra"] == pytest.approx(
        scenario["apparent"]["ra"],
        abs=TOLERANCE_IN_APPARENT_PLACE / cos(radians(scenario["apparent"]["dec"])),
    )
    assert apparent["dec"] == pytest.approx(
        scenario["apparent"]["dec"], abs=TOLERANCE_IN_APPARENT_PLACE
    )


# **************************************************************************************
