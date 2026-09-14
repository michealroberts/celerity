# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from datetime import datetime, timezone
from typing import TypedDict

import pytest

from src.celerity.aberration import get_correction_to_equatorial_for_aberration
from src.celerity.common import EquatorialCoordinate
from src.celerity.coordinates import get_correction_to_equatorial
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
# precession correction from the rp matrix of bp06, the aberration correction from ab
# with the Earth state from epv00, and the apparent place from atci13 with the equation
# of the origins subtracted to give the equinox-based right ascension.

# **************************************************************************************

# The tolerance on the nutation in longitude and obliquity, and on the nutation
# correction to an equatorial coordinate. celerity uses the IAU 2000B series evaluated
# in TT, so the difference from IAU 2000A is at the milliarcsecond level and reflects the
# terms omitted from the truncated series:
TOLERANCE_IN_NUTATION: float = 0.002 / 3600

# **************************************************************************************

# The tolerance on the precession correction to an equatorial coordinate. celerity uses
# the IAU 2006 (P03) equatorial precession angles evaluated in TT, so the difference from
# ERFA is at the microarcsecond level and reflects only the series truncation:
TOLERANCE_IN_PRECESSION: float = 0.001 / 3600

# **************************************************************************************

# The tolerance on the aberration correction to an equatorial coordinate. celerity uses
# a first-order annual aberration model (Meeus, Astronomical Algorithms, 23.3), so the
# difference from ERFA is dominated by the neglected second-order and planetary terms:
TOLERANCE_IN_ABERRATION: float = 0.3 / 3600

# **************************************************************************************

# The tolerance on the full apparent place, i.e. the precession, nutation and aberration
# corrections applied in turn. This is currently dominated by the first-order aberration
# model and the mean obliquity used when applying the nutation:
TOLERANCE_IN_APPARENT_PLACE: float = 0.05 / 3600

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
]

# **************************************************************************************

scenarios: list[Scenario] = [
    # Betelgeuse on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.78921196601357, "dec": 7.405429164798},
        "precession": {"ra": 88.79295832752871, "dec": 7.407063900238369},
        "aberration": {"ra": 88.79867698967043, "dec": 7.406789914568695},
        "apparent": {"ra": 88.79493424918059, "dec": 7.405153500675567},
    },
    # Vega on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23261171404425, "dec": 38.78502374271821},
        "precession": {"ra": 279.2347348170764, "dec": 38.78368890181726},
        "aberration": {"ra": 279.2273290383562, "dec": 38.78334161782614},
        "apparent": {"ra": 279.22521368176695, "dec": 38.78467974005863},
    },
    # Sirius on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28415219481592, "dec": -16.71738627503702},
        "precession": {"ra": 101.28715532272228, "dec": -16.716115902216348},
        "aberration": {"ra": 101.29318039867022, "dec": -16.716465687492715},
        "apparent": {"ra": 101.2901828949624, "dec": -16.717736410590707},
    },
    # Arcturus on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.9115857149967, "dec": 19.184581938028963},
        "precession": {"ra": 213.91530032385904, "dec": 19.182410290603585},
        "aberration": {"ra": 213.91278221847196, "dec": 19.18028829875967},
        "apparent": {"ra": 213.90907074576978, "dec": 19.182465497835448},
    },
    # Dubhe on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.92482412740236, "dec": 61.752136604477876},
        "precession": {"ra": 165.93196473117928, "dec": 61.751033089016616},
        "aberration": {"ra": 165.93685750984028, "dec": 61.746177618380656},
        "apparent": {"ra": 165.92971510248498, "dec": 61.74728517212735},
    },
    # Canopus on 2000-01-01:
    {
        "date": datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98662772876203, "dec": -52.69713270672398},
        "precession": {"ra": 95.98794961127693, "dec": -52.69569940118136},
        "aberration": {"ra": 95.99745664171114, "dec": -52.69623977372937},
        "apparent": {"ra": 95.99614560795548, "dec": -52.697673307902555},
    },
    # Betelgeuse on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.79744428153295, "dec": 7.407530798507679},
        "precession": {"ra": 88.93443372339166, "dec": 7.408217067914066},
        "aberration": {"ra": 88.78733140662348, "dec": 7.4068726883631575},
        "apparent": {"ra": 88.93329858012545, "dec": 7.4084849340507155},
    },
    # Vega on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23746677066043, "dec": 38.78356175291039},
        "precession": {"ra": 279.3224939660921, "dec": 38.79307153583077},
        "aberration": {"ra": 279.24166541689215, "dec": 38.78256913132908},
        "apparent": {"ra": 279.33216640263987, "dec": 38.79183515610252},
    },
    # Sirius on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.29083556182613, "dec": -16.716056409531614},
        "precession": {"ra": 101.4039274437955, "dec": -16.72756360999897},
        "aberration": {"ra": 101.28157281509891, "dec": -16.71683745321198},
        "apparent": {"ra": 101.40203035029172, "dec": -16.72822727149572},
    },
    # Arcturus on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.9193142597776, "dec": 19.180643134021267},
        "precession": {"ra": 214.03791430424695, "dec": 19.134157766247363},
        "aberration": {"ra": 213.91910489167216, "dec": 19.183581844225202},
        "apparent": {"ra": 214.04573523622858, "dec": 19.133570238693768},
    },
    # Dubhe on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.93781857502174, "dec": 61.749350848365474},
        "precession": {"ra": 166.09202163893252, "dec": 61.69457083710985},
        "aberration": {"ra": 165.93030461739045, "dec": 61.75579698703873},
        "apparent": {"ra": 166.09621370571048, "dec": 61.697654358710324},
    },
    # Canopus on 2010-06-15:
    {
        "date": datetime(2010, 6, 15, 3, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98973495512033, "dec": -52.695465601589525},
        "precession": {"ra": 96.04590361199902, "dec": -52.70179949558628},
        "aberration": {"ra": 95.97891153785547, "dec": -52.69677814962422},
        "apparent": {"ra": 96.0386566039513, "dec": -52.70263970673901},
    },
    # Betelgeuse on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.7882422896919, "dec": 7.407770307191752},
        "precession": {"ra": 89.0821544191646, "dec": 7.409267715625173},
        "aberration": {"ra": 88.7883918567132, "dec": 7.406101849409489},
        "apparent": {"ra": 89.07287680897146, "dec": 7.409028101989159},
    },
    # Vega on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23171023673484, "dec": 38.782640780194775},
        "precession": {"ra": 279.4141278380687, "dec": 38.802961078161346},
        "aberration": {"ra": 279.2397356958076, "dec": 38.780223087947405},
        "apparent": {"ra": 279.41612245746995, "dec": 38.798452235773844},
    },
    # Sirius on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28321858607794, "dec": -16.715004376824268},
        "precession": {"ra": 101.5258499602996, "dec": -16.73963933443159},
        "aberration": {"ra": 101.28323042828325, "dec": -16.718567349884996},
        "apparent": {"ra": 101.5179891361851, "dec": -16.740966112978835},
    },
    # Arcturus on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.9114290853619, "dec": 19.183598711079355},
        "precession": {"ra": 214.16593623802666, "dec": 19.083855346393335},
        "aberration": {"ra": 213.92070922796705, "dec": 19.18175657844484},
        "apparent": {"ra": 214.16747468800256, "dec": 19.08439322352507},
    },
    # Dubhe on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.92797622503213, "dec": 61.7530912748933},
        "precession": {"ra": 166.25876265809313, "dec": 61.635581251157504},
        "aberration": {"ra": 165.93614002170838, "dec": 61.75487463258346},
        "apparent": {"ra": 166.258963006501, "dec": 61.64148076730824},
    },
    # Canopus on 2021-05-14:
    {
        "date": datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98590989767034, "dec": -52.694754299546005},
        "precession": {"ra": 96.1064150953546, "dec": -52.70823059471847},
        "aberration": {"ra": 95.98116858222264, "dec": -52.69939473348227},
        "apparent": {"ra": 96.09758248364211, "dec": -52.71096559211423},
    },
    # Betelgeuse on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 88.7929583, "dec": 7.4070639},
        "nutation": {"ra": 88.79534209862399, "dec": 7.409421842086958},
        "precession": {"ra": 89.15439012776993, "dec": 7.4097244309518375},
        "aberration": {"ra": 88.79224584170433, "dec": 7.408608708924488},
        "apparent": {"ra": 89.1560697011673, "dec": 7.413621056513292},
    },
    # Vega on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 279.2347348, "dec": 38.7836889},
        "nutation": {"ra": 279.23591806196885, "dec": 38.78153880849428},
        "precession": {"ra": 279.4589372623369, "dec": 38.8078315592837},
        "aberration": {"ra": 279.2368251309677, "dec": 38.78852183434682},
        "apparent": {"ra": 279.46219234825406, "dec": 38.81052597738137},
    },
    # Sirius on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 101.2871553, "dec": -16.7161159},
        "nutation": {"ra": 101.28899170225554, "dec": -16.714015307026486},
        "precession": {"ra": 101.58546871130743, "dec": -16.745589989638383},
        "aberration": {"ra": 101.28527047804268, "dec": -16.712578055573182},
        "apparent": {"ra": 101.5854297909043, "dec": -16.73995536264618},
    },
    # Arcturus on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 213.9153003, "dec": 19.1824103},
        "nutation": {"ra": 213.91804747257032, "dec": 19.18029184123591},
        "precession": {"ra": 214.2285375741675, "dec": 19.059287226843605},
        "aberration": {"ra": 213.91126535471366, "dec": 19.18567936517261},
        "apparent": {"ra": 214.22724749380075, "dec": 19.060430107624352},
    },
    # Dubhe on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 165.9319647, "dec": 61.7510331},
        "nutation": {"ra": 165.93889163936203, "dec": 61.75064974432048},
        "precession": {"ra": 166.340158254035, "dec": 61.60672241701942},
        "aberration": {"ra": 165.9210120033976, "dec": 61.75168306297155},
        "apparent": {"ra": 166.33615049738535, "dec": 61.606984471981114},
    },
    # Canopus on 2026-09-14:
    {
        "date": datetime(2026, 9, 14, 0, 0, 0, 0, tzinfo=timezone.utc),
        "target": {"ra": 95.9879496, "dec": -52.6956994},
        "nutation": {"ra": 95.98861187366724, "dec": -52.69347667022211},
        "precession": {"ra": 96.13600501453601, "dec": -52.71139836664715},
        "aberration": {"ra": 95.98572770655088, "dec": -52.690350492556604},
        "apparent": {"ra": 96.13448251348838, "dec": -52.70382587533667},
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
        scenario["nutation"]["ra"], abs=TOLERANCE_IN_NUTATION
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
        scenario["precession"]["ra"], abs=TOLERANCE_IN_PRECESSION
    )
    assert target["dec"] + correction["dec"] == pytest.approx(
        scenario["precession"]["dec"], abs=TOLERANCE_IN_PRECESSION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial_for_aberration(scenario: Scenario) -> None:
    target = scenario["target"]

    correction = get_correction_to_equatorial_for_aberration(scenario["date"], target)

    assert target["ra"] + correction["ra"] == pytest.approx(
        scenario["aberration"]["ra"], abs=TOLERANCE_IN_ABERRATION
    )
    assert target["dec"] + correction["dec"] == pytest.approx(
        scenario["aberration"]["dec"], abs=TOLERANCE_IN_ABERRATION
    )


# **************************************************************************************


@pytest.mark.parametrize("scenario", scenarios)
def test_get_correction_to_equatorial(scenario: Scenario) -> None:
    apparent = get_correction_to_equatorial(scenario["date"], {**scenario["target"]})

    assert apparent["ra"] == pytest.approx(
        scenario["apparent"]["ra"], abs=TOLERANCE_IN_APPARENT_PLACE
    )
    assert apparent["dec"] == pytest.approx(
        scenario["apparent"]["dec"], abs=TOLERANCE_IN_APPARENT_PLACE
    )


# **************************************************************************************
