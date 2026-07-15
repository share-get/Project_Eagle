from __future__ import annotations

from typing import Iterable

import pandas as pd

from .base import Feature


class FeatureBuilder:
    """
    Execute registered features sequentially.
    """

    def __init__(self) -> None:
        self._features: list[Feature] = []

    def register(self, feature: Feature) -> None:
        self._features.append(feature)

    def extend(self, features: Iterable[Feature]) -> None:
        self._features.extend(features)

    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        for feature in self._features:
            result = feature.apply(result)

        return result
