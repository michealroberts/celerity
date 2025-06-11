# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2025 observerly

# **************************************************************************************

from datetime import datetime
from typing import TypedDict

# **************************************************************************************


class IERSTAIUTCOffsetEntry(TypedDict):
    """
    Represents a TAI-UTC offset entry.
    """

    # The datetime of the TAI-UTC offset entry:
    at: datetime
    # The TAI-UTC offset (in seconds):
    offset: float


# **************************************************************************************
