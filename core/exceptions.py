"""
Custom exceptions.
"""


class EagleError(Exception):
    """Base exception."""


class DataDownloadError(EagleError):
    """Download failed."""


class CacheError(EagleError):
    """Cache error."""


class ValidationError(EagleError):
    """Validation failed."""


class IndicatorError(EagleError):
    """Indicator calculation failed."""


class BacktestError(EagleError):
    """Backtest failed."""
