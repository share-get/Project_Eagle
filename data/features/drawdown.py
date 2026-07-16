"""
Drawdown feature.
"""

from __future__ import annotations

import pandas as pd

from project_eagle.core.constants import Columns

from .base import Feature


class DrawdownFeature(Feature):

    @property
    def name(self) -> str:
        return "drawdown"

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        result = df.copy()

        close = result[Columns.CLOSE]

        peak = close.cummax()

        drawdown = close / peak - 1.0

        result[Columns.PEAK] = peak

        result[Columns.DRAWDOWN] = drawdown

        return result
