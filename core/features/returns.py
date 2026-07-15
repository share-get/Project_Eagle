from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Feature


class ReturnFeature(Feature):

    name = "return"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        out = df.copy()

        out["Return"] = out["Close"].pct_change()

        out["LogReturn"] = np.log(
            out["Close"] / out["Close"].shift(1)
        )

        return out
