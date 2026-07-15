from __future__ import annotations

import pandas as pd

from .base import Feature


class DrawdownFeature(Feature):
    """
    Add drawdown related columns.

    Columns
    -------
    Peak
        Historical highest closing price.

    Drawdown
        Percentage drawdown from Peak.
    """

    name = "drawdown"

    def apply(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        out = df.copy()

        peak = out["Close"].cummax()

        out["Peak"] = peak

        out["Drawdown"] = (
            out["Close"] - peak
        ) / peak

        return out
