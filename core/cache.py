"""
Cache Manager
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class CacheManager:
    """
    CSV cache manager.
    """

    def __init__(self, cache_dir: Path):

        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def cache_path(
        self,
        ticker: str,
    ) -> Path:

        safe = (
            ticker
            .replace("^", "")
            .replace("=", "_")
            .replace("/", "_")
        )

        return self.cache_dir / f"{safe}.csv"

    def exists(
        self,
        ticker: str,
    ) -> bool:

        return self.cache_path(ticker).exists()

    def load(
        self,
        ticker: str,
    ) -> pd.DataFrame:

        return pd.read_csv(
            self.cache_path(ticker),
            index_col=0,
            parse_dates=True,
        )

    def save(
        self,
        ticker: str,
        df: pd.DataFrame,
    ) -> None:

        df.to_csv(
            self.cache_path(ticker)
        )

    def remove(
        self,
        ticker: str,
    ) -> None:

        path = self.cache_path(ticker)

        if path.exists():

            path.unlink()
