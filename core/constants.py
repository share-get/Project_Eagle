"""
Project Eagle - Global Constants

This module defines canonical names used throughout the project.

Keeping all column names and enums here avoids hard-coded strings
scattered across the codebase.
"""

from __future__ import annotations

from enum import Enum


# =============================================================================
# DataFrame Columns
# =============================================================================

class Columns:
    """
    Canonical DataFrame column names.
    """

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

    ROLLING_HIGH_252 = "RollingHigh252"
    ROLLING_LOW_252 = "RollingLow252"


# =============================================================================
# Trading Signals
# =============================================================================

class Signal(str, Enum):
    """
    Strategy output signals.
    """

    BUY = "BUY"
    HOLD = "HOLD"
    WAIT = "WAIT"
    REDUCE = "REDUCE"


# =============================================================================
# Data Source
# =============================================================================

class DataSource(str, Enum):
    """
    Supported market data providers.
    """

    YAHOO = "yahoo"

    # Reserved for future versions
    POLYGON = "polygon"
    ALPHA_VANTAGE = "alpha_vantage"
    FRED = "fred"


# =============================================================================
# Cache Format
# =============================================================================

class CacheFormat(str, Enum):
    """
    Supported cache formats.
    """

    CSV = "csv"

    # Future versions
    PARQUET = "parquet"
    DUCKDB = "duckdb"


# =============================================================================
# Trading Calendar
# =============================================================================

TRADING_DAYS_PER_YEAR = 252


# =============================================================================
# Default Feature Windows
# =============================================================================

VOLATILITY_WINDOWS = (
    20,
    60,
    120,
)

ROLLING_WINDOW = 252
