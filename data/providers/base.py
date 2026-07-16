"""
Base interface for market data providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class DataProvider(ABC):
    """
    Abstract base class for market data providers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""

    @abstractmethod
    def download(
        self,
        ticker: str,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """
        Download historical market data.

        Parameters
        ----------
        ticker
            Symbol to download.

        start
            Optional start date.

        end
            Optional end date.

        Returns
        -------
        pandas.DataFrame
            Historical OHLCV data.
        """
