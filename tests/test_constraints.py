# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

import unittest
from datetime import datetime, timezone

from celerity.common import EquatorialCoordinate, GeographicCoordinate
from celerity.constraints import AltitudeConstraint, Constraint

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
        when: datetime,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
    ) -> bool:
        return True


# **************************************************************************************


class AlwaysFalseConstraint(Constraint):
    """A constraint that is never satisfied."""

    def _is_satisfied(
        self,
        when: datetime,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
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


class TestAltitudeConstraint(unittest.TestCase):
    def setUp(self) -> None:
        self.observer = observer
        self.target = betelgeuse
        self.when = date

    def test_altitude_constraint(self):
        # Create an AltitudeConstraint with a minimum altitude of 0 degrees and a
        # maximum altitude of 90 degrees:
        constraint = AltitudeConstraint(
            {
                "minimum": 0.0,
                "maximum": 90.0,
            }
        )

        # Check that the constraint is satisfied for the target:
        result = constraint(observer=self.observer, target=self.target, when=self.when)
        self.assertTrue(result)

    def test_altitude_constraint_with_temperature(self):
        # Create an AltitudeConstraint with a minimum altitude of 0 degrees and a
        # maximum altitude of 90 degrees:
        constraint = AltitudeConstraint(
            {
                "minimum": 0.0,
                "maximum": 90.0,
                "temperature": 283.15,
            }
        )

        # Check that the constraint is satisfied for the target:
        result = constraint(
            observer=self.observer,
            target=self.target,
            when=self.when,
        )
        self.assertTrue(result)

    def test_altitude_constraint_with_pressure(self):
        # Create an AltitudeConstraint with a minimum altitude of 0 degrees and a
        # maximum altitude of 90 degrees:
        constraint = AltitudeConstraint(
            {
                "minimum": 0.0,
                "maximum": 90.0,
                "pressure": 101325,
            }
        )

        # Check that the constraint is satisfied for the target:
        result = constraint(observer=self.observer, target=self.target, when=self.when)
        self.assertTrue(result)

    def test_invalid_minimum_and_maximum_altitude(self):
        with self.assertRaises(ValueError):
            AltitudeConstraint(
                {
                    "minimum": 90.0,
                    "maximum": 0.0,
                }
            )

    def test_invalid_minimum_altitude(self):
        with self.assertRaises(ValueError):
            AltitudeConstraint(
                {
                    "minimum": -1.0,
                    "maximum": 90.0,
                }
            )

    def test_invalid_maximum_altitude(self):
        with self.assertRaises(ValueError):
            AltitudeConstraint(
                {
                    "minimum": 0.0,
                    "maximum": 91.0,
                }
            )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
