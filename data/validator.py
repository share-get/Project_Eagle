"""
Project Eagle - Data Validator

Validate OHLCV market data before feature generation.
"""

from __future__ import annotations

import pandas as pd

from project_eagle.core.constants import Columns
from project_eagle.core.exceptions import ValidationError


class DataValidator:
    """
    Validate downloaded market data.

    Validation rules
    ----------------
    1. DataFrame cannot be empty
    2. Required columns must exist
    3. Index must be DatetimeIndex
    4. Index cannot contain duplicates
    5. Index must be sorted ascending
    6. OHLCV columns must be numeric
    """

    REQUIRED_COLUMNS = (
        Columns.OPEN,
        Columns.HIGH,
        Columns.LOW,
        Columns.CLOSE,
        Columns.VOLUME,
    )

    def __init__(
        self,
        allow_missing: bool = False,
        auto_sort: bool = True,
    ) -> None:
        self.allow_missing = allow_missing
        self.auto_sort = auto_sort

    def validate(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate market dataframe.

        Parameters
        ----------
        df
            Market OHLCV dataframe.

        Returns
        -------
        pd.DataFrame
            Validated dataframe.

        Raises
        ------
        ValidationError
        """

        self._validate_not_empty(df)

        df = self._validate_index(df)

        self._validate_columns(df)

        self._validate_numeric(df)

        self._validate_missing(df)

        return df

    def _validate_not_empty(
        self,
        df: pd.DataFrame,
    ) -> None:

        if df.empty:
            raise ValidationError(
                "DataFrame is empty."
            )

    def _validate_index(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if not isinstance(
            df.index,
            pd.DatetimeIndex,
        ):
            raise ValidationError(
                "Index must be DatetimeIndex."
            )

        if df.index.has_duplicates:
            raise ValidationError(
                "Duplicate dates found."
            )

        if not df.index.is_monotonic_increasing:

            if self.auto_sort:

                df = df.sort_index()

            else:

                raise ValidationError(
                    "Index is not sorted."
                )

        return df

    def _validate_columns(
        self,
        df: pd.DataFrame,
    ) -> None:

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValidationError(
                f"Missing columns: {missing}"
            )

    def _validate_numeric(
        self,
        df: pd.DataFrame,
    ) -> None:

        for column in self.REQUIRED_COLUMNS:

            if not pd.api.types.is_numeric_dtype(
                df[column]
            ):
                raise ValidationError(
                    f"Column '{column}' must be numeric."
                )

    def _validate_missing(
        self,
        df: pd.DataFrame,
    ) -> None:

        if self.allow_missing:
            return

        missing_count = int(
            df[self.REQUIRED_COLUMNS]
            .isna()
            .sum()
            .sum()
        )

        if missing_count > 0:
            raise ValidationError(
                f"Found {missing_count} missing values."
            )
