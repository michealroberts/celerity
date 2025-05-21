# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, TypedDict

from .common import EquatorialCoordinate, GeographicCoordinate
from .coordinates import convert_equatorial_to_horizontal
from .refraction import get_correction_to_horizontal_for_refraction

# **************************************************************************************


class Constraint(ABC):
    """
    Base class for constraints on astronomical targets at a single time.

    Constraints determine whether a single target satisfies an observational
    condition at a specific moment.
    """

    def __call__(
        self,
        when: datetime,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
    ) -> bool:
        """
        Evaluate the constraint for one target at one moment in time.

        Constraints are evaluated in the context of an observer, a target,
        and a single time point.

        Args:
            observer (GeographicCoordinate): The observer's geographic coordinates.
            target (EquatorialCoordinate): The target's equatorial coordinates.
            when (datetime): The time at which to evaluate the constraint.

        Returns:
            bool: True if the target satisfies the constraint at the given time, otherwise False.

        Note:
            Subclasses must implement the `_is_satisfied` method to define specific
            constraint logic.
        """
        return self._is_satisfied(observer=observer, target=target, when=when)

    @abstractmethod
    def _is_satisfied(
        self,
        when: datetime,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
    ) -> bool:
        """
        Determine if the constraint is met for a target at a specific time.

        N.B. This method should be overridden by subclasses to implement the
        actual constraint logic.
        """
        raise NotImplementedError("Subclasses must implement _is_satisfied method.")


# **************************************************************************************


class AltitudeConstraintParameters(TypedDict):
    minimum_altitude: float
    maximum_altitude: float
    temperature: Optional[float]
    pressure: Optional[float]


# **************************************************************************************


class AltitudeConstraint(Constraint):
    """
    Constraint that checks if a target is above a specified altitude.

    Args:
        params (AltitudeConstraintParameters): Parameters for the altitude constraint.
    """

    def __init__(self, params: AltitudeConstraintParameters):
        self.minimum_altitude = params["minimum_altitude"]
        self.maximum_altitude = params["maximum_altitude"]

        # Sanity check to ensure that the maximum altitude is greater than the minimum altitude:
        if self.minimum_altitude > self.maximum_altitude:
            raise ValueError(
                "Minimum altitude must be less than or equal to maximum altitude."
            )

        # Sanity check to ensure that the minimum altitude is not less than 0 degrees:
        if self.minimum_altitude < 0.0:
            raise ValueError(
                "Minimum altitude must be greater than or equal to 0.0 degrees."
            )

        # Sanity check to ensure that the maximum altitude is not greater than 90 degrees:
        if self.maximum_altitude > 90.0:
            raise ValueError(
                "Maximum altitude must be less than or equal to 90.0 degrees."
            )

        # Default temperature is 283.15 K (10 degrees Celsius):
        self.temperature = params.get("temperature", 283.15) or 283.15

        # Default pressure is 101325 Pa (1 atmosphere):
        self.pressure = params.get("pressure", 101325) or 101325

    def _is_satisfied(
        self,
        when: datetime,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
    ) -> bool:
        """
        Check if the target's altitude is within the specified range.

        Args:
            observer (GeographicCoordinate): The observer's geographic coordinates.
            target (EquatorialCoordinate): The target's equatorial coordinates.
            when (datetime): The time at which to evaluate the constraint.

        Returns:
            bool: True if the target's altitude is within the specified range, otherwise False.
        """
        # Convert the target's equatorial coordinates to horizontal coordinates:
        hz = convert_equatorial_to_horizontal(
            date=when, observer=observer, target=target
        )

        # Correct the horizontal coordinates for atmospheric refraction:
        hz = get_correction_to_horizontal_for_refraction(
            target=hz,
            temperature=self.temperature,
            pressure=self.pressure,
        )

        # Check if the target's altitude is within the specified range:
        return (
            self.minimum_altitude <= hz["alt"] <= self.maximum_altitude
            if self.minimum_altitude < self.maximum_altitude
            else False
        )


# **************************************************************************************
