"""Custom metrics for testing dynamic import functionality."""
from typing import List
from typing import Optional

from evidently.core.datasets import Dataset
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.pydantic_utils import register_type_alias


class CustomRowSumMetric(SingleValueMetric):
    """A custom metric that calculates the sum of a specific column.
    
    This is used for testing dynamic import from external modules.
    """
    
    class Config:
        type_alias = "evidently:metric_v2:CustomRowSumMetric"
    
    column: str = "a"
    """Column to calculate sum for."""


class CustomRowSumCalculation(SingleValueCalculation[CustomRowSumMetric]):
    """Calculation for CustomRowSumMetric."""
    
    def calculate(self, context, current_data: Dataset, reference_data: Optional[Dataset]):
        column_data = current_data.column(self.metric.column).data
        current_sum = column_data.sum()
        
        reference_sum = None
        if reference_data is not None:
            ref_column_data = reference_data.column(self.metric.column).data
            reference_sum = ref_column_data.sum()
        
        return (
            self.result(current_sum),
            None if reference_sum is None else self.result(reference_sum),
        )
    
    def display_name(self) -> str:
        return f"Sum of column '{self.metric.column}'"


register_type_alias(
    SingleValueMetric,
    "tests.cli.custom_metrics.CustomRowSumMetric",
    "evidently:metric_v2:CustomRowSumMetric"
)
