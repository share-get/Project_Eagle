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
    Unified data access entry.

    Responsibilities
    ----------------
    - download
    - cache
    - validate
    - build features
    """

    def __init__(
        self,
        cache_dir: str | Path = "cache",
        auto_adjust: bool = False,
    ) -> None:

        self.downloader = YahooDownloader(
            auto_adjust=auto_adjust
        )

        self.cache = CacheManager(cache_dir)

        self.validator = DataValidator()

        self.builder = FeatureBuilder()

        self.builder.extend(
            [
                ReturnFeature(),
                DrawdownFeature(),
                VolatilityFeature(),
            ]
        )
            def get_price(
        self,
        ticker: str,
        refresh: bool = False,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:

        if (
            not refresh
            and self.cache.exists(ticker)
        ):
            df = self.cache.load(ticker)

        else:

            df = self.downloader.download(
                ticker,
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

        result = {}

        for ticker in tickers:

            result[ticker] = self.get_price(
                ticker
            )

        return result
            def refresh(
        self,
        ticker: str,
    ) -> pd.DataFrame:

        return self.get_price(
            ticker=ticker,
            refresh=True,
        )
        
