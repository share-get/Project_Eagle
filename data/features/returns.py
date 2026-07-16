"""
Daily return features.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from project_eagle.core.constants import Columns

from .base import Feature


class ReturnFeature(Feature):
    """
    Add arithmetic and log returns.
    """

    @property
    def name(self) -> str:
        return "return"

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        result = df.copy()

        close = result[Columns.CLOSE]

        result[Columns.RETURN] = close.pct_change()

        result[Columns.LOG_RETURN] = np.log(
            close / close.shift(1)
        )

        return result
