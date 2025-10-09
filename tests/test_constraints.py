# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from datetime import datetime, timezone

from celerity.common import EquatorialCoordinate, GeographicCoordinate
from celerity.constraints import Constraint

# **************************************************************************************

# For testing we need to specify a date because most calculations are
# differential w.r.t a time component. We set it to the author's birthday:
date = datetime(2021, 5, 14, 0, 0, 0, 0, tzinfo=timezone.utc)

# **************************************************************************************

# For testing, we will fix the latitude to be Manua Kea, Hawaii, US
latitude: float = 19.820611

# **************************************************************************************

# For testing, we will fix the longitude to be Manua Kea, Hawaii, US
longitude: float = -155.468094

# **************************************************************************************

betelgeuse: EquatorialCoordinate = {"ra": 88.7929583, "dec": 7.4070639}

# **************************************************************************************

observer: GeographicCoordinate = {
    "latitude": latitude,
    "longitude": longitude,
    "elevation": 0.0,
}

# **************************************************************************************


class AlwaysTrueConstraint(Constraint):
    """A constraint that is always satisfied."""

    def _is_satisfied(
        self,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
        when: datetime,
    ) -> bool:
        return True


# **************************************************************************************


class AlwaysFalseConstraint(Constraint):
    """A constraint that is never satisfied."""

    def _is_satisfied(
        self,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
        when: datetime,
    ) -> bool:
        return False


# **************************************************************************************


class TestConstraintBase(unittest.TestCase):
    def setUp(self) -> None:
        self.observer = observer
        self.target = betelgeuse
        self.when = date

    def test_cannot_instantiate_base(self):
        with self.assertRaises(TypeError):
            # Constraint has an abstract method, so this must fail:
            Constraint()

    def test_always_true_constraint(self):
        truthy = AlwaysTrueConstraint()
        result = truthy(observer=self.observer, target=self.target, when=self.when)
        self.assertTrue(result)

    def test_always_false_constraint(self):
        falsey = AlwaysFalseConstraint()
        result = falsey(observer=self.observer, target=self.target, when=self.when)
        self.assertFalse(result)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
