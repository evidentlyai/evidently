"""
Data processor abstraction layer for Pandas and Polars support.

This module provides a unified interface for working with Pandas and Polars dataframes,
enabling gradual migration to Polars while maintaining backward compatibility.

The key design principle is lazy evaluation:
  - Convert pandas DataFrames to Polars lazy frames
  - Perform operations on lazy frames for optimization
  - Only materialize (collect) when results are needed
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeGuard
from typing import Union

import pandas as pd

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False


# Type hints
DataFrame = Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"]
PolarsDF = Union["pl.DataFrame", "pl.LazyFrame"]


class DataFrameProcessor:
    """
    Unified interface for Pandas and Polars dataframe operations.

    Provides lazy evaluation support for Polars to enable automatic optimization.
    Maintains backward compatibility with existing Pandas code.
    """

    def __init__(self, enable_polars: bool = True):
        """
        Initialize the processor.

        Args:
            enable_polars: If True and available, use Polars for operations.
                          Falls back to Pandas if not available.
        """
        self.enable_polars = enable_polars and POLARS_AVAILABLE
        self._polars_cache: Dict[str, Any] = {}

    @property
    def polars_enabled(self) -> bool:
        """Check if Polars acceleration is enabled."""
        return self.enable_polars

    @staticmethod
    def is_pandas(df: DataFrame) -> TypeGuard[pd.DataFrame]:
        """Check if dataframe is a Pandas DataFrame."""
        return isinstance(df, pd.DataFrame)

    @staticmethod
    def is_polars(df: DataFrame) -> TypeGuard[PolarsDF]:
        """Check if dataframe is a Polars DataFrame or LazyFrame."""
        if not POLARS_AVAILABLE:
            return False
        return isinstance(df, (pl.DataFrame, pl.LazyFrame))

    @staticmethod
    def is_lazy(df: DataFrame) -> TypeGuard["pl.LazyFrame"]:
        """Check if Polars dataframe is lazy."""
        if not POLARS_AVAILABLE:
            return False
        return isinstance(df, pl.LazyFrame)

    def to_polars(self, df: pd.DataFrame, lazy: bool = True) -> PolarsDF:
        """
        Convert Pandas DataFrame to Polars.

        Args:
            df: Pandas DataFrame to convert
            lazy: If True, return a lazy frame for deferred computation

        Returns:
            Polars DataFrame or LazyFrame
        """
        if not self.enable_polars:
            raise RuntimeError("Polars is not available or disabled")

        polars_df = pl.from_pandas(df)

        if lazy:
            return polars_df.lazy()
        return polars_df

    def to_pandas(self, df: PolarsDF) -> pd.DataFrame:
        """
        Convert Polars DataFrame/LazyFrame to Pandas.

        Args:
            df: Polars DataFrame or LazyFrame

        Returns:
            Pandas DataFrame
        """
        if isinstance(df, pl.LazyFrame):
            return df.collect().to_pandas()
        elif isinstance(df, pl.DataFrame):
            return df.to_pandas()
        else:
            raise TypeError(f"Expected Polars DataFrame/LazyFrame, got {type(df)}")

    def process_dataframe(self, df: DataFrame, force_pandas: bool = False) -> DataFrame:
        """
        Process a dataframe, optionally converting to Polars.

        Args:
            df: Input dataframe (Pandas or Polars)
            force_pandas: If True, always return Pandas

        Returns:
            Processed dataframe
        """
        if force_pandas:
            if self.is_polars(df):
                return self.to_pandas(df)
            return df

        # If Polars enabled and input is Pandas, convert
        if self.enable_polars and self.is_pandas(df):
            return self.to_polars(df, lazy=True)

        return df

    def filter_rows(self, df: DataFrame, conditions: Dict[str, Any]) -> DataFrame:
        """
        Filter rows based on conditions.

        Works with both Pandas and Polars, using native operations.

        Args:
            df: Input dataframe
            conditions: Dictionary of {column: value} conditions

        Returns:
            Filtered dataframe
        """
        if self.is_polars(df):
            result = df
            for column, value in conditions.items():
                result = result.filter(pl.col(column) == value)
            return result
        else:
            # Pandas path
            result = df
            for column, value in conditions.items():
                result = result[result[column] == value]
            return result

    def group_by_aggregate(self, df: DataFrame, group_cols: List[str], agg_dict: Dict[str, str]) -> DataFrame:
        """
        Group by columns and aggregate.

        Args:
            df: Input dataframe
            group_cols: Columns to group by
            agg_dict: Aggregation spec {column: operation}
                     E.g., {"value": "mean", "count": "sum"}

        Returns:
            Aggregated dataframe
        """
        if self.is_polars(df):
            polars_aggs = []
            for col, op in agg_dict.items():
                if op == "mean":
                    polars_aggs.append(pl.col(col).mean().alias(f"{col}_mean"))
                elif op == "sum":
                    polars_aggs.append(pl.col(col).sum().alias(f"{col}_sum"))
                elif op == "count":
                    polars_aggs.append(pl.col(col).count().alias(f"{col}_count"))
                elif op == "min":
                    polars_aggs.append(pl.col(col).min().alias(f"{col}_min"))
                elif op == "max":
                    polars_aggs.append(pl.col(col).max().alias(f"{col}_max"))
                elif op == "std":
                    polars_aggs.append(pl.col(col).std().alias(f"{col}_std"))
                else:
                    raise ValueError(f"Unsupported aggregation: {op}")

            return df.groupby(group_cols).agg(polars_aggs)
        else:
            # Pandas path
            return df.groupby(group_cols).agg(agg_dict)

    def select_columns(self, df: DataFrame, columns: List[str]) -> DataFrame:
        """
        Select specific columns.

        Args:
            df: Input dataframe
            columns: List of column names

        Returns:
            Dataframe with selected columns
        """
        if self.is_polars(df):
            return df.select(columns)
        else:
            return df[columns]

    def collect(self, df: DataFrame) -> DataFrame:
        """
        Materialize a lazy dataframe (Polars) or return as-is (Pandas).

        Use this when you need actual results, e.g., for display or export.

        Args:
            df: Input dataframe

        Returns:
            Materialized dataframe
        """
        if self.is_lazy(df):
            return df.collect()
        return df

    def to_dict(self, df: DataFrame, orient: str = "list") -> Dict[str, Any]:
        """
        Convert dataframe to dictionary.

        Args:
            df: Input dataframe
            orient: Orientation for Pandas (ignored for Polars)

        Returns:
            Dictionary representation
        """
        if self.is_lazy(df):
            df = df.collect()

        if self.is_polars(df):
            return df.to_dict(as_series=False)
        else:
            return df.to_dict(orient=orient)

    def shape(self, df: DataFrame) -> Tuple[int, int]:
        """
        Get shape (rows, columns) of dataframe.

        For lazy frames, this triggers materialization.

        Args:
            df: Input dataframe

        Returns:
            Tuple of (n_rows, n_columns)
        """
        if self.is_polars(df):
            # Polars lazy frames don't guarantee shape without materialization
            if self.is_lazy(df):
                df = df.collect()
            return df.shape
        else:
            return df.shape

    def get_column(self, df: DataFrame, column: str) -> Any:
        """
        Extract a column as Series/Array.

        Args:
            df: Input dataframe
            column: Column name

        Returns:
            Column data
        """
        if self.is_polars(df):
            if self.is_lazy(df):
                df = df.collect()
            return df[column].to_numpy()
        else:
            return df[column].values

    def describe_performance_characteristics(self) -> Dict[str, Any]:
        """
        Return information about processor configuration.

        Useful for benchmarking and debugging.
        """
        return {
            "polars_enabled": self.enable_polars,
            "polars_available": POLARS_AVAILABLE,
            "polars_version": pl.__version__ if POLARS_AVAILABLE else None,
            "pandas_version": pd.__version__,
        }


# Convenience functions for common use cases


def enable_lazy_evaluation() -> DataFrameProcessor:
    """Create a processor with Polars lazy evaluation enabled."""
    return DataFrameProcessor(enable_polars=True)


def use_pandas_only() -> DataFrameProcessor:
    """Create a processor that only uses Pandas."""
    return DataFrameProcessor(enable_polars=False)


# Global default processor (can be configured by users)
class _ProcessorRegistry:
    """Registry for managing the default processor instance."""

    _instance: Optional[DataFrameProcessor] = None

    @classmethod
    def get(cls) -> DataFrameProcessor:
        """Get the default data processor instance."""
        if cls._instance is None:
            cls._instance = DataFrameProcessor(enable_polars=True)
        return cls._instance

    @classmethod
    def set(cls, processor: DataFrameProcessor) -> None:
        """Set the default data processor instance."""
        cls._instance = processor


def get_default_processor() -> DataFrameProcessor:
    """Get the default data processor instance."""
    return _ProcessorRegistry.get()


def set_default_processor(processor: DataFrameProcessor) -> None:
    """Set the default data processor instance."""
    _ProcessorRegistry.set(processor)
