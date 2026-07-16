"""
Feature pipeline.
"""

from __future__ import annotations

import pandas as pd

from .base import Feature


class FeatureBuilder:
    """
    Sequential feature pipeline.

    Examples
    --------
    >>> builder = FeatureBuilder([
    ...     ReturnFeature(),
    ...     DrawdownFeature(),
    ... ])
    >>> df = builder.transform(df)
    """

    def __init__(
        self,
        features: list[Feature] | None = None,
    ) -> None:

        self._features = features or []

    def add(
        self,
        feature: Feature,
    ) -> None:
        """
        Add one feature.
        """
        self._features.append(feature)

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute feature pipeline.
        """

        result = df.copy()

        for feature in self._features:
            result = feature.transform(result)

        return result

    def __len__(self) -> int:
        return len(self._features)
