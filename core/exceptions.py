"""
Project Eagle exception hierarchy.
"""

from __future__ import annotations


class EagleError(Exception):
    """
    Base exception for Project Eagle.
    """

    pass


# ============================================================================
# Data
# ============================================================================

class DataError(EagleError):
    """
    Base exception for data layer.
    """

    pass


class DataDownloadError(DataError):
    """
    Raised when market data download fails.
    """

    pass


class ValidationError(DataError):
    """
    Raised when downloaded data is invalid.
    """

    pass


class CacheError(DataError):
    """
    Raised when cache read/write fails.
    """

    pass


# ============================================================================
# Indicators
# ============================================================================

class IndicatorError(EagleError):
    """
    Indicator calculation error.
    """

    pass


# ============================================================================
# Factors
# ============================================================================

class FactorError(EagleError):
    """
    Factor calculation error.
    """

    pass


# ============================================================================
# Strategy
# ============================================================================

class StrategyError(EagleError):
    """
    Strategy execution error.
    """

    pass


# ============================================================================
# Backtest
# ============================================================================

class BacktestError(EagleError):
    """
    Backtest execution error.
    """

    pass


# ============================================================================
# Configuration
# ============================================================================

class ConfigurationError(EagleError):
    """
    Invalid project configuration.
    """

    pass
