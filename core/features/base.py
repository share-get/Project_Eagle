from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Feature(ABC):
    """
    Base class for all dataframe features.
    """

    name: str = ""

    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature to dataframe.

        Returns
        -------
        pd.DataFrame
            DataFrame with new feature column(s).
        """
        raise NotImplementedError
