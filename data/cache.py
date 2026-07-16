"""
Project Eagle - Cache Manager

Read and write local market data cache.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from project_eagle.core.exceptions import CacheError


class CacheManager:
    """
    Local CSV cache manager.

    Each ticker is stored as:

        cache/
            VOO.csv
            QQQM.csv
            SPY.csv
    """

    def __init__(
        self,
        cache_dir: Path,
    ) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(
        self,
        ticker: str,
    ) -> Path:
        """
        Return cache file path.
        """
        return self.cache_dir / f"{ticker.upper()}.csv"

    def exists(
        self,
        ticker: str,
    ) -> bool:
        """
        Whether cache exists.
        """
        return self._path(ticker).exists()

    def load(
        self,
        ticker: str,
    ) -> pd.DataFrame:
        """
        Load cached dataframe.
        """
        path = self._path(ticker)

        if not path.exists():
            raise CacheError(
                f"Cache not found: {path}"
            )

        try:
            df = pd.read_csv(
                path,
                index_col=0,
                parse_dates=True,
            )
        except Exception as exc:
            raise CacheError(
                f"Failed to load cache: {path}"
            ) from exc

        return df

    def save(
        self,
        ticker: str,
        df: pd.DataFrame,
    ) -> None:
        """
        Save dataframe to cache.
        """
        path = self._path(ticker)

        try:
            df.to_csv(path)
        except Exception as exc:
            raise CacheError(
                f"Failed to save cache: {path}"
            ) from exc

    def remove(
        self,
        ticker: str,
    ) -> None:
        """
        Delete one cache file.
        """
        path = self._path(ticker)

        if path.exists():
            path.unlink()

    def clear(
        self,
    ) -> None:
        """
        Delete all cache files.
        """
        for file in self.cache_dir.glob("*.csv"):
            file.unlink()

    def list(
        self,
    ) -> list[str]:
        """
        Return cached tickers.
        """
        return sorted(
            file.stem
            for file in self.cache_dir.glob("*.csv")
        )
