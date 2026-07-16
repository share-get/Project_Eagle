"""
Project Eagle - Data Manager
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from project_eagle.core.config import Config

from .cache import CacheManager
from .features.builder import FeatureBuilder
from .providers.base import DataProvider
from .validator import DataValidator


class DataManager:
    """
    Coordinate data download, cache, validation and feature generation.
    """

    def __init__(
        self,
        provider: DataProvider,
        config: Config | None = None,
        validator: DataValidator | None = None,
        features: FeatureBuilder | None = None,
    ) -> None:

        self.config = config or Config()
        self.config.ensure()

        self.provider = provider

        self.cache = CacheManager(
            self.config.cache_dir,
        )

        self.validator = validator or DataValidator()

        self.features = features or FeatureBuilder()

    def get_price(
        self,
        ticker: str,
        refresh: bool = False,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """
        Get historical price.
        """

        if (
            not refresh
            and self.cache.exists(ticker)
        ):
            df = self.cache.load(ticker)

        else:

            df = self.provider.download(
                ticker=ticker,
                start=start,
                end=end,
            )

            df = self.validator.validate(df)

            df = self.features.transform(df)

            self.cache.save(
                ticker,
                df,
            )

        return df

    def refresh(
        self,
        ticker: str,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """
        Force download newest data.
        """

        return self.get_price(
            ticker=ticker,
            refresh=True,
            start=start,
            end=end,
        )

    def get_prices(
        self,
        tickers: list[str],
        refresh: bool = False,
    ) -> dict[str, pd.DataFrame]:
        """
        Download multiple tickers.
        """

        result: dict[str, pd.DataFrame] = {}

        for ticker in tickers:

            result[ticker] = self.get_price(
                ticker,
                refresh=refresh,
            )

        return result

    def clear_cache(self) -> None:
        """
        Remove all cached files.
        """

        self.cache.clear()
