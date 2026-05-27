"""
Utilities for supporting Polars-optimized metrics.

This module provides decorators and utilities to enable metrics to use Polars
for performance optimization while maintaining backward compatibility with Pandas.

Key Features:
- Decorator for marking metrics as Polars-compatible
- Helper functions for efficient dataframe operations
- Lazy evaluation support for complex calculations
"""

from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd

from .data_processor import POLARS_AVAILABLE
from .data_processor import DataFrameProcessor

if POLARS_AVAILABLE:
    import polars as pl

# Type variables for decorators
F = TypeVar("F", bound=Callable[..., Any])
ResultType = TypeVar("ResultType")


class PolarsOptimization:
    """Configuration for Polars optimization in a metric."""

    def __init__(
        self,
        enabled: bool = True,
        lazy_eval: bool = True,
        safe_mode: bool = False,
    ):
        """Initialize Polars optimization config.

        Args:
            enabled: Whether to use Polars when available
            lazy_eval: Whether to use lazy evaluation for Polars
            safe_mode: If True, validate that Polars and Pandas results match
        """
        self.enabled = enabled and POLARS_AVAILABLE
        self.lazy_eval = lazy_eval
        self.safe_mode = safe_mode
        self.processor = DataFrameProcessor(enable_polars=self.enabled)


# Thread-local storage for metric-level optimization config
_metric_optimization_config: Dict[str, PolarsOptimization] = {}


def polars_optimized(
    *,
    enabled: bool = True,
    lazy_eval: bool = True,
    safe_mode: bool = False,
) -> Callable[[F], F]:
    """Decorator to mark a metric calculation as Polars-optimized.

    This decorator adds Polars support to metric calculation classes.
    When Polars is available, operations will be performed on Polars dataframes
    for better performance. Falls back to Pandas if needed.

    Args:
        enabled: Whether Polars optimization is enabled by default
        lazy_eval: Use lazy evaluation for Polars (deferred computation)
        safe_mode: If True, validate that Polars and Pandas results match

    Example:
        ```python
        @polars_optimized(enabled=True, lazy_eval=True)
        class CustomMetricCalculation(SingleValueCalculation):
            def calculate(self, context, current_data, reference_data):
                # Use dataframe operations
                df = current_data.as_dataframe()
                # ... calculation logic
        ```
    """

    def decorator(cls: F) -> F:
        # Initialize optimization config for this class
        config = PolarsOptimization(
            enabled=enabled,
            lazy_eval=lazy_eval,
            safe_mode=safe_mode,
        )
        _metric_optimization_config[cls.__name__] = config

        # Add convenience method to access processor
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self._polars_config = config
            self._polars_processor = config.processor

        cls.__init__ = new_init

        # Add method to get processor
        def get_polars_processor(self) -> DataFrameProcessor:
            return self._polars_processor

        cls.get_polars_processor = get_polars_processor  # type: ignore[assignment]

        return cls

    return decorator


def supports_polars_operations(dataframe: Any) -> bool:
    """Check if a dataframe supports Polars operations.

    Args:
        dataframe: The dataframe to check

    Returns:
        True if dataframe can be converted to Polars
    """
    return DataFrameProcessor.is_pandas(dataframe) or DataFrameProcessor.is_polars(dataframe)


def to_polars_lazy(
    df: Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"],
    processor: Optional[DataFrameProcessor] = None,
) -> Union["pl.DataFrame", "pl.LazyFrame", pd.DataFrame]:
    """Convert a dataframe to Polars lazy frame if possible.

    Args:
        df: Input dataframe
        processor: Optional DataFrameProcessor instance

    Returns:
        Polars LazyFrame if available and df is Pandas, otherwise unchanged
    """
    if processor is None:
        processor = DataFrameProcessor(enable_polars=True)

    if processor.is_pandas(df):
        return processor.to_polars(df, lazy=True)

    return df


def to_pandas_safe(
    df: Any,
    processor: Optional[DataFrameProcessor] = None,
) -> pd.DataFrame:
    """Safely convert any supported dataframe to Pandas.

    Args:
        df: Input dataframe (Pandas or Polars)
        processor: Optional DataFrameProcessor instance

    Returns:
        Pandas DataFrame
    """
    if processor is None:
        processor = DataFrameProcessor(enable_polars=True)

    if processor.is_polars(df):
        return processor.to_pandas(df)

    if isinstance(df, pd.DataFrame):
        return df

    raise TypeError(f"Unsupported dataframe type: {type(df)}")


def polars_aggregate(
    df: Union[pd.DataFrame, "pl.DataFrame"],
    group_cols: list,
    agg_specs: Dict[str, str],
    processor: Optional[DataFrameProcessor] = None,
) -> Union[pd.DataFrame, "pl.DataFrame"]:
    """Efficiently aggregate data using appropriate library.

    Uses Polars if available for better performance, falls back to Pandas.

    Args:
        df: Input dataframe
        group_cols: Columns to group by
        agg_specs: Dictionary of column -> aggregation operation
        processor: Optional DataFrameProcessor instance

    Returns:
        Aggregated dataframe (Pandas or Polars based on input)
    """
    if processor is None:
        processor = DataFrameProcessor(enable_polars=True)

    if not processor.enable_polars or processor.is_pandas(df):
        # Pandas path
        return df.groupby(group_cols).agg(agg_specs)

    # Polars path
    return processor.group_by_aggregate(df, group_cols, agg_specs)


def collect_if_lazy(df: Any) -> Any:
    """Materialize a Polars lazy frame, or return unchanged.

    Args:
        df: Dataframe (can be Polars lazy or eager, Pandas, etc.)

    Returns:
        Materialized dataframe
    """
    if not POLARS_AVAILABLE:
        return df

    if isinstance(df, pl.LazyFrame):
        return df.collect()

    return df


def describe_dataframe_type(df: Any) -> str:
    """Get a human-readable description of dataframe type.

    Args:
        df: Dataframe to describe

    Returns:
        String describing the dataframe type
    """
    if isinstance(df, pd.DataFrame):
        return f"Pandas DataFrame ({len(df)} rows, {len(df.columns)} cols)"

    if POLARS_AVAILABLE:
        if isinstance(df, pl.DataFrame):
            rows, cols = df.shape
            return f"Polars DataFrame (eager, {rows} rows, {cols} cols)"

        if isinstance(df, pl.LazyFrame):
            return "Polars LazyFrame (deferred computation)"

    return f"Unknown dataframe type: {type(df)}"
