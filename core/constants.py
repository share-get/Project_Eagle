"""
Global constants used across Project Eagle.
"""

from enum import Enum


class Columns:
    """Canonical dataframe column names."""

    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    VOLUME = "Volume"

    RETURN = "Return"
    LOG_RETURN = "LogReturn"

    PEAK = "Peak"
    DRAWDOWN = "Drawdown"

    VOL20 = "Vol20"
    VOL60 = "Vol60"
    VOL120 = "Vol120"


class Signal(Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    WAIT = "WAIT"
    REDUCE = "REDUCE"
