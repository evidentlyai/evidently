"""Example custom metric that can be loaded from external module.

To use this custom metric in your config.yaml:

modules:
  - custom_metric.py

metrics:
  - type: evidently:metric_v2:CustomAverageMetric
    column: "age"
"""
from typing import Optional

from evidently.core.datasets import Dataset
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.pydantic_utils import register_type_alias


class CustomAverageMetric(SingleValueMetric):
    """A custom metric that calculates the average of a specific column.
    
    This is an example of a custom metric that can be defined in an external
    Python file and loaded via YAML configuration.
    """
    
    class Config:
        type_alias = "evidently:metric_v2:CustomAverageMetric"
    
    column: str
    """Column to calculate average for."""


class CustomAverageCalculation(SingleValueCalculation[CustomAverageMetric]):
    """Calculation for CustomAverageMetric."""
    
    def calculate(self, context, current_data: Dataset, reference_data: Optional[Dataset]):
        column_data = current_data.column(self.metric.column).data
        current_avg = column_data.mean()
        
        reference_avg = None
        if reference_data is not None:
            ref_column_data = reference_data.column(self.metric.column).data
            reference_avg = ref_column_data.mean()
        
        return (
            self.result(current_avg),
            None if reference_avg is None else self.result(reference_avg),
        )
    
    def display_name(self) -> str:
        return f"Average of column '{self.metric.column}'"


register_type_alias(
    SingleValueMetric,
    "custom_metric.CustomAverageMetric",
    "evidently:metric_v2:CustomAverageMetric"
)
