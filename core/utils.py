"""
Project Eagle
core/utils.py

Utility functions used across the project.
"""

from __future__ import annotations

import functools
import time
from datetime import datetime
from typing import Any, Callable, TypeVar

import numpy as np
import pandas as pd

T = TypeVar("T")


# ============================================================
# Date Helpers
# ============================================================


def today_string() -> str:
    """
    Return today's date in YYYY-MM-DD format.
    """

    return datetime.today().strftime("%Y-%m-%d")


def ensure_datetime_index(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ensure DataFrame index is DatetimeIndex.
    """

    if not isinstance(df.index, pd.DatetimeIndex):

        df.index = pd.to_datetime(df.index)

    return df


# ============================================================
# Validation
# ============================================================


def validate_price_dataframe(
    df: pd.DataFrame,
) -> None:
    """
    Validate OHLCV dataframe.
    """

    required = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

    if df.empty:

        raise ValueError(
            "Empty dataframe."
        )

    if (df["Close"] <= 0).any():

        raise ValueError(
            "Close price <= 0."
        )


# ============================================================
# Return Calculation
# ============================================================


def pct_return(
    series: pd.Series,
) -> pd.Series:

    return series.pct_change()


def log_return(
    series: pd.Series,
) -> pd.Series:

    return np.log(
        series / series.shift(1)
    )


def cumulative_return(
    series: pd.Series,
) -> pd.Series:

    r = pct_return(series)

    return (1 + r).cumprod() - 1


# ============================================================
# Drawdown
# ============================================================


def rolling_peak(
    series: pd.Series,
) -> pd.Series:

    return series.cummax()


def drawdown(
    series: pd.Series,
) -> pd.Series:

    peak = rolling_peak(series)

    return series / peak - 1.0


def max_drawdown(
    series: pd.Series,
) -> float:

    return float(drawdown(series).min())


# ============================================================
# Volatility
# ============================================================


def rolling_volatility(
    returns: pd.Series,
    window: int = 20,
) -> pd.Series:

    return returns.rolling(window).std()


def annualized_volatility(
    returns: pd.Series,
    trading_days: int = 252,
) -> float:

    return float(
        returns.std() * np.sqrt(trading_days)
    )


# ============================================================
# Annual Return
# ============================================================


def annualized_return(
    close: pd.Series,
    trading_days: int = 252,
) -> float:

    total = len(close)

    if total < 2:

        return np.nan

    years = total / trading_days

    growth = close.iloc[-1] / close.iloc[0]

    return float(growth ** (1 / years) - 1)


# ============================================================
# Timer Decorator
# ============================================================


def timer(func: Callable[..., T]) -> Callable[..., T]:

    @functools.wraps(func)
    def wrapper(
        *args: Any,
        **kwargs: Any,
    ) -> T:

        start = time.perf_counter()

        result = func(
            *args,
            **kwargs,
        )

        end = time.perf_counter()

        print(
            f"{func.__name__} "
            f"finished in "
            f"{end-start:.3f}s"
        )

        return result

    return wrapper
# ============================================================
# Retry Decorator
# ============================================================

from __future__ import annotations

import time
from typing import Iterable


def retry(
    retries: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """
    Retry decorator.

    Parameters
    ----------
    retries
        Maximum retry count.

    delay
        Waiting time between retries.

    exceptions
        Exception types to retry.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            last_error = None

            for attempt in range(retries):

                try:

                    return func(*args, **kwargs)

                except exceptions as exc:

                    last_error = exc

                    if attempt == retries - 1:
                        break

                    time.sleep(delay)

            raise last_error

        return wrapper

    return decorator


# ============================================================
# DataFrame Cleaning
# ============================================================

def flatten_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert MultiIndex columns into a flat Index.
    """

    if isinstance(df.columns, pd.MultiIndex):

        df.columns = df.columns.get_level_values(0)

    return df


def standardize_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove spaces from column names.
    """

    df.columns = [
        str(c).replace(" ", "")
        for c in df.columns
    ]

    return df


def clean_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standard cleaning pipeline.
    """

    df = flatten_columns(df)

    df = standardize_columns(df)

    df = ensure_datetime_index(df)

    df = df.sort_index()

    df = df.loc[~df.index.duplicated()]

    df = df.ffill()

    df = df.dropna(how="all")

    return df


# ============================================================
# Rolling Statistics
# ============================================================

def rolling_high(
    series: pd.Series,
    window: int = 252,
) -> pd.Series:

    return series.rolling(window).max()


def rolling_low(
    series: pd.Series,
    window: int = 252,
) -> pd.Series:

    return series.rolling(window).min()


# ============================================================
# Scaling
# ============================================================

def zscore(
    series: pd.Series,
) -> pd.Series:

    std = series.std()

    if std == 0 or np.isnan(std):

        return pd.Series(
            0.0,
            index=series.index,
        )

    return (series - series.mean()) / std


def minmax_scale(
    series: pd.Series,
) -> pd.Series:

    minimum = series.min()

    maximum = series.max()

    if maximum == minimum:

        return pd.Series(
            0.0,
            index=series.index,
        )

    return (
        series - minimum
    ) / (
        maximum - minimum
    )


# ============================================================
# Risk Metrics
# ============================================================

def sharpe_ratio(
    returns: pd.Series,
    risk_free: float = 0.0,
    trading_days: int = 252,
) -> float:

    excess = returns - risk_free / trading_days

    std = excess.std()

    if std == 0 or np.isnan(std):

        return np.nan

    return float(
        np.sqrt(trading_days)
        * excess.mean()
        / std
    )


def sortino_ratio(
    returns: pd.Series,
    risk_free: float = 0.0,
    trading_days: int = 252,
) -> float:

    downside = returns[returns < 0]

    std = downside.std()

    if std == 0 or np.isnan(std):

        return np.nan

    excess = returns.mean() - risk_free / trading_days

    return float(
        np.sqrt(trading_days)
        * excess
        / std
    )


def calmar_ratio(
    annual_return: float,
    max_drawdown_value: float,
) -> float:

    if max_drawdown_value == 0:

        return np.nan

    return annual_return / abs(max_drawdown_value)


# ============================================================
# Merge Helpers
# ============================================================

def align_dataframes(
    dataframes: Iterable[pd.DataFrame],
) -> list[pd.DataFrame]:
    """
    Align multiple DataFrames to the same date index.
    """

    dataframes = list(dataframes)

    if not dataframes:

        return []

    index = dataframes[0].index

    for df in dataframes[1:]:

        index = index.intersection(df.index)

    return [
        df.loc[index].copy()
        for df in dataframes
    ]


def latest_value(
    series: pd.Series,
):

    return series.iloc[-1]


# ============================================================
# END OF FILE
# ============================================================
