from __future__ import annotations

from typing import Optional

import pandas as pd
import yfinance as yf

from .utils import (
    clean_dataframe,
    validate_price_dataframe,
)


class YahooDownloader:
    """
    Download historical market data from Yahoo Finance.
    """

    def __init__(
        self,
        auto_adjust: bool = False,
    ) -> None:

        self.auto_adjust = auto_adjust

    def download(
        self,
        ticker: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Download price history.

        Parameters
        ----------
        ticker
            Yahoo Finance ticker.

        start
            YYYY-MM-DD

        end
            YYYY-MM-DD

        Returns
        -------
        DataFrame
        """

        df = yf.download(
            ticker=ticker,
            start=start,
            end=end,
            auto_adjust=self.auto_adjust,
            progress=False,
            threads=False,
        )

        if df.empty:
            raise RuntimeError(
                f"No data returned for {ticker}"
            )

        df = clean_dataframe(df)

        validate_price_dataframe(df)

        return df
