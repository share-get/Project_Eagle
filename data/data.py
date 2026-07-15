"""
Project Eagle - Data Manager

Unified entry point for market data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .cache import CacheManager
from .downloader import YahooDownloader
from .features import (
    DrawdownFeature,
    FeatureBuilder,
    ReturnFeature,
    VolatilityFeature,
)
from .validator import DataValidator


class DataManager:
    """
    Unified market data interface.

    Pipeline

        Download
            ↓
        Cache
            ↓
        Validate
            ↓
        Build Features
            ↓
        Return DataFrame
    """

    def __init__(
        self,
        downloader: YahooDownloader | None = None,
        cache: CacheManager | None = None,
        validator: DataValidator | None = None,
        feature_builder: FeatureBuilder | None = None,
    ) -> None:

        self.downloader = downloader or YahooDownloader()

        self.cache = cache or CacheManager(
            Path("cache")
        )

        self.validator = validator or DataValidator()

        if feature_builder is None:

            builder = FeatureBuilder()

            builder.extend(
                [
                    ReturnFeature(),
                    DrawdownFeature(),
                    VolatilityFeature(),
                ]
            )

            self.builder = builder

        else:

            self.builder = feature_builder

    def get_price(
        self,
        ticker: str,
        refresh: bool = False,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """
        Get price dataframe.

        Parameters
        ----------
        ticker
            Yahoo ticker.

        refresh
            Ignore cache.

        Returns
        -------
        DataFrame
        """

        if (
            not refresh
            and self.cache.exists(ticker)
        ):

            df = self.cache.load(ticker)

        else:

            df = self.downloader.download(
                ticker=ticker,
                start=start,
                end=end,
            )

            self.cache.save(
                ticker,
                df,
            )

        df = self.validator.validate(df)

        df = self.builder.build(df)

        return df

    def get_prices(
        self,
        tickers: list[str],
    ) -> dict[str, pd.DataFrame]:

        return {
            ticker: self.get_price(ticker)
            for ticker in tickers
        }

    def refresh(
        self,
        ticker: str,
    ) -> pd.DataFrame:

        return self.get_price(
            ticker=ticker,
            refresh=True,
        )

    def clear_cache(
        self,
        ticker: str | None = None,
    ) -> None:

        if ticker is None:

            for file in self.cache.cache_dir.glob("*.csv"):
                file.unlink()

            return

        self.cache.remove(ticker)
