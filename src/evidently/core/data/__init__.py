"""Data processing utilities for Evidently metrics and reports."""

from .data_processor import DataFrameProcessor
from .polars_support import PolarsOptimization
from .polars_support import collect_if_lazy
from .polars_support import describe_dataframe_type
from .polars_support import polars_aggregate
from .polars_support import polars_optimized
from .polars_support import supports_polars_operations
from .polars_support import to_pandas_safe
from .polars_support import to_polars_lazy

__all__ = [
    "DataFrameProcessor",
    "PolarsOptimization",
    "polars_optimized",
    "supports_polars_operations",
    "to_polars_lazy",
    "to_pandas_safe",
    "polars_aggregate",
    "collect_if_lazy",
    "describe_dataframe_type",
]
