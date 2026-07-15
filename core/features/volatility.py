from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Feature


class VolatilityFeature(Feature):
    """
    Rolling volatility based on daily returns.
    """

    name = "volatility"

    def __init__(
        self,
        windows: tuple[int, ...] = (20, 60, 120),
        annualization: int = 252,
    ) -> None:

        self.windows = windows
        self.annualization = annualization

    def apply(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        out = df.copy()

        if "Return" not in out.columns:
            out["Return"] = out["Close"].pct_change()

        for window in self.windows:

            out[f"Vol{window}"] = (
                out["Return"]
                .rolling(window)
                .std()
                * np.sqrt(self.annualization)
            )

        return out
