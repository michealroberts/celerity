# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from abc import ABC, abstractmethod
from datetime import datetime

from .common import EquatorialCoordinate, GeographicCoordinate

# **************************************************************************************


class Constraint(ABC):
    """
    Base class for constraints on astronomical targets at a single time.

    Constraints determine whether a single target satisfies an observational
    condition at a specific moment.
    """

    def __call__(
        self,
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
        when: datetime,
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
        observer: GeographicCoordinate,
        target: EquatorialCoordinate,
        when: datetime,
    ) -> bool:
        """
        Determine if the constraint is met for a target at a specific time.

        N.B. This method should be overridden by subclasses to implement the
        actual constraint logic.
        """
        raise NotImplementedError("Subclasses must implement _is_satisfied method.")


# **************************************************************************************
