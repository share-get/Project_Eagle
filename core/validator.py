from __future__ import annotations

import pandas as pd


class DataValidator:
    """
    Validate OHLCV market data.
    """

    REQUIRED_COLUMNS = (
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    )

    def validate(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if df.empty:
            raise ValidationError(
    "Empty dataframe."
)

        missing = [
            c
            for c in self.REQUIRED_COLUMNS
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        if not isinstance(
            df.index,
            pd.DatetimeIndex,
        ):
            raise TypeError(
                "Index must be DatetimeIndex."
            )

        if df.index.has_duplicates:
            raise ValueError(
                "Duplicated datetime index."
            )

        if not df.index.is_monotonic_increasing:
            df = df.sort_index()

        if (df["Close"] <= 0).any():
            raise ValueError(
                "Invalid close price."
            )

        return df
