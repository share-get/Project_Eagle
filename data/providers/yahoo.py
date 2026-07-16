"""
Yahoo Finance data provider.
"""

from __future__ import annotations

from typing import Final

import pandas as pd
import yfinance as yf

from project_eagle.core.constants import Columns
from project_eagle.core.exceptions import DataDownloadError

from .base import DataProvider


_REQUIRED_COLUMNS: Final = (
    Columns.OPEN,
    Columns.HIGH,
    Columns.LOW,
    Columns.CLOSE,
    Columns.VOLUME,
)


class YahooProvider(DataProvider):
    """
    Yahoo Finance implementation.

    Examples
    --------
    >>> provider = YahooProvider()
    >>> df = provider.download("VOO")
    """

    @property
    def name(self) -> str:
        return "Yahoo Finance"

    def download(
        self,
        ticker: str,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """
        Download OHLCV data from Yahoo Finance.
        """

        try:
            df = yf.download(
                tickers=ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=False,
            )
        except Exception as exc:
            raise DataDownloadError(
                f"Failed to download '{ticker}' from Yahoo Finance."
            ) from exc

        if df.empty:
            raise DataDownloadError(
                f"No data returned for '{ticker}'."
            )

        # yfinance may return MultiIndex columns for a single ticker.
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.rename_axis("Date")
        df = df.sort_index()

        missing = [
            column
            for column in _REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise DataDownloadError(
                f"Missing required columns: {missing}"
            )

        return df.loc[:, list(_REQUIRED_COLUMNS)].copy()
