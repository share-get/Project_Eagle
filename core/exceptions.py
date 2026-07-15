"""
Project Eagle - Custom Exceptions

Centralized exception hierarchy used across the project.
"""

from __future__ import annotations


class EagleError(Exception):
    """
    Base exception for Project Eagle.
    """

    pass


# =============================================================================
# Data Layer
# =============================================================================

class DataError(EagleError):
    """
    Base exception for all data related errors.
    """

    pass


class DataDownloadError(DataError):
    """
    Market data download failed.
    """

    pass


class CacheError(DataError):
    """
    Cache read/write failed.
    """

    pass


class ValidationError(DataError):
    """
    Data validation failed.
    """

    pass


class FeatureError(DataError):
    """
    Feature engineering failed.
    """

    pass


# =============================================================================
# Indicator Layer
# =============================================================================

class IndicatorError(EagleError):
    """
    Indicator calculation failed.
    """

    pass


# =============================================================================
# Factor Layer
# =============================================================================

class FactorError(EagleError):
    """
    Factor calculation failed.
    """

    pass


# =============================================================================
# Score Layer
# =============================================================================

class ScoreError(EagleError):
    """
    Eagle Score calculation failed.
    """

    pass


# =============================================================================
# Strategy Layer
# =============================================================================

class StrategyError(EagleError):
    """
    Strategy execution failed.
    """

    pass


# =============================================================================
# Backtest Layer
# =============================================================================

class BacktestError(EagleError):
    """
    Backtest execution failed.
    """

    pass


# =============================================================================
# Portfolio Layer
# =============================================================================

class PortfolioError(EagleError):
    """
    Portfolio management failed.
    """

    pass


# =============================================================================
# Report Layer
# =============================================================================

class ReportError(EagleError):
    """
    Report generation failed.
    """

    pass


# =============================================================================
# Configuration
# =============================================================================

class ConfigError(EagleError):
    """
    Configuration error.
    """

    pass
