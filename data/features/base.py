"""
Base class for all feature generators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Feature(ABC):
    """
    Base class for all engineered features.

    Each feature receives a DataFrame and returns
    a new DataFrame with additional columns.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Feature name."""

    @abstractmethod
    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Apply feature transformation.

        Parameters
        ----------
        df
            Input dataframe.

        Returns
        -------
        pd.DataFrame
            Dataframe with new feature columns.
        """
