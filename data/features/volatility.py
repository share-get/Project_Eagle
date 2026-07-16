"""
Rolling annualized volatility.
"""

from __future__ import annotations

import pandas as pd

from project_eagle.core.constants import (
    Columns,
    TRADING_DAYS_PER_YEAR,
)

from .base import Feature


class VolatilityFeature(Feature):

    def __init__(
        self,
        windows: tuple[int, ...] = (
            20,
            60,
            120,
        ),
    ) -> None:

        self.windows = windows

    @property
    def name(self) -> str:
        return "volatility"

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        result = df.copy()

        if Columns.RETURN not in result.columns:
            returns = result[
                Columns.CLOSE
            ].pct_change()
        else:
            returns = result[
                Columns.RETURN
            ]

        mapping = {
            20: Columns.VOL20,
            60: Columns.VOL60,
            120: Columns.VOL120,
        }

        for window in self.windows:

            column = mapping.get(
                window,
                f"Vol{window}",
            )

            result[column] = (
                returns
                .rolling(window)
                .std()
                * (TRADING_DAYS_PER_YEAR ** 0.5)
            )

        return result
