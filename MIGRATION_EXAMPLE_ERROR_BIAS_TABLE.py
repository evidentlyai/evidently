# Example: Migrating RegressionErrorBiasTable to New Report API
# This file demonstrates the exact implementation pattern

"""
BEFORE (Using Legacy API):
    from evidently.legacy.metrics import RegressionErrorBiasTable
    from evidently.legacy.report import Report
    
    report = Report([RegressionErrorBiasTable()])
    report.run(reference_data=ref_df, current_data=curr_df)

AFTER (Using New Report API):
    from evidently import Report
    from evidently.metrics import RegressionErrorBiasTable  # NEW!
    
    report = Report([RegressionErrorBiasTable()])
    snapshot = report.run(curr_dataset, ref_dataset)
"""

# ============================================================================
# IMPLEMENTATION EXAMPLE - Add to src/evidently/metrics/regression.py
# ============================================================================

from typing import List, Optional, Dict, Tuple, TypeVar, Generic
import abc
from evidently.core.metric_types import (
    SingleValue,
    SingleValueMetric,
    MetricResult,
    get_default_render,
    get_default_render_ref,
)
from evidently.core.report import Context
from evidently.legacy.base_metric import InputData
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.metrics._legacy import LegacyMetricCalculation

# Import the legacy metric and its result type
from evidently.legacy.metrics.regression_performance.error_bias_table import (
    RegressionErrorBiasTable as LegacyRegressionErrorBiasTable,
)
from evidently.legacy.metrics.regression_performance.error_bias_table import (
    RegressionErrorBiasTableResults,
)


# STEP 1: Define the new metric class
class RegressionErrorBiasTable(SingleValueMetric):
    """
    Regression Error Bias analysis metric for the new Report API.
    
    Analyzes prediction error bias across different features. Categorizes errors
    as underestimation, overestimation, or within majority band based on a
    quantile threshold.
    
    Args:
        columns: Specific columns to analyze. If None, uses all numeric and categorical features.
        top_error: Quantile threshold for defining "top" errors (default: 0.05 = 5%).
                   Must be between 0 and 0.5. Lower values = stricter threshold.
        regression_name: Name of the regression task (for multi-task support).
    
    Example:
        ```python
        from evidently import Report
        from evidently.metrics import RegressionErrorBiasTable
        
        report = Report([
            RegressionErrorBiasTable(columns=['age', 'income']),
            RegressionErrorBiasTable(top_error=0.1),
        ])
        snapshot = report.run(current_data, reference_data)
        ```
    """
    
    regression_name: str = "default"
    """Name of the regression task."""
    
    columns: Optional[List[str]] = None
    """List of feature columns to analyze. None means all features."""
    
    top_error: Optional[float] = None
    """Error quantile threshold (0-0.5). Default is 0.05."""


# STEP 2: Define the calculation class
class RegressionErrorBiasTableCalculation(
    LegacyMetricCalculation[
        SingleValue,  # TResult - what the new metric returns
        RegressionErrorBiasTable,  # TMetric - the new metric class
        RegressionErrorBiasTableResults,  # TLegacyResult - what legacy metric returns
        LegacyRegressionErrorBiasTable,  # TLegacyMetric - the legacy metric
    ],
):
    """Calculation class that bridges new and legacy RegressionErrorBiasTable."""
    
    def legacy_metric(self) -> LegacyRegressionErrorBiasTable:
        """
        Convert new metric parameters to legacy metric instantiation.
        
        This maps the new metric's attributes to the legacy metric's constructor.
        The legacy metric does the actual heavy calculation work.
        """
        return LegacyRegressionErrorBiasTable(
            columns=self.metric.columns,
            top_error=self.metric.top_error,
        )
    
    def task_name(self) -> str:
        """
        Return the regression task name.
        
        This is used for multi-task regression support. The context will
        extract the target and prediction columns for this task.
        """
        return self.metric.regression_name
    
    def calculate_value(
        self,
        context: Context,
        legacy_result: RegressionErrorBiasTableResults,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        """
        Transform legacy result into new metric result.
        
        Args:
            context: Report execution context
            legacy_result: Result from legacy metric calculation
            render: HTML widgets from legacy rendering
        
        Returns:
            SingleValue metric result with the computed value
        
        Implementation note:
            The legacy metric returns rich data (error_bias dict, plot_data, etc.)
            We extract a meaningful scalar result. In this case, we count the
            number of features analyzed as the summarized metric value.
        """
        # Extract a scalar value from the complex legacy result
        if legacy_result.error_bias is None or len(legacy_result.error_bias) == 0:
            # If no error bias was calculated, return 0
            value = 0.0
        else:
            # Count the number of features with error bias analysis
            # (This is just an example - actual implementation might compute
            # a weighted average of bias metrics, correlation with features, etc.)
            value = float(len(legacy_result.error_bias))
        
        return self.result(value)
    
    def _gen_input_data(
        self,
        context: Context,
        task_name: Optional[str],
    ) -> InputData:
        """
        Override to provide regression-aware input data.
        
        This uses the parent regression helper to set up the column mapping
        with the correct target and prediction columns for the configured
        regression task.
        """
        return _gen_regression_input_data(context, task_name)
    
    def get_additional_widgets(self, context: Context) -> List[BaseWidgetInfo]:
        """
        Provide additional visualization widgets.
        
        The legacy metric renderer produces rich HTML widgets. We return those
        to be included in the report's widget list alongside the metric result.
        """
        # Widget list is already populated by the LegacyMetricCalculation base
        # class from the legacy renderer's output, so we typically return []
        # unless adding extra custom visualizations.
        return []
    
    def display_name(self) -> str:
        """Return human-readable metric name for UI display."""
        return "Regression Error Bias Table"


# ============================================================================
# ALTERNATIVE: For metrics returning complex structures
# ============================================================================

"""
If the metric result is more complex (like a DataFrame or custom structure),
you'd define a custom result class:

from evidently.core.metric_types import DataframeValue

class RegressionErrorBiasTableValue(DataframeValue):
    '''Error bias analysis results.'''
    error_bias: Dict[str, Dict[str, float]]
    analysis_by_feature: Dict[str, Any]

class RegressionErrorBiasTable(SingleValueMetric):
    columns: Optional[List[str]] = None
    top_error: Optional[float] = None

class RegressionErrorBiasTableCalculation(
    LegacyMetricCalculation[
        RegressionErrorBiasTableValue,  # Complex result type
        RegressionErrorBiasTable,
        RegressionErrorBiasTableResults,
        LegacyRegressionErrorBiasTable,
    ],
):
    def calculate_value(
        self,
        context: Context,
        legacy_result: RegressionErrorBiasTableResults,
        render: List[BaseWidgetInfo],
    ) -> RegressionErrorBiasTableValue:
        return self.result(
            df=legacy_result.current_plot_data,
            error_bias=legacy_result.error_bias or {},
            analysis_by_feature={...},
        )
"""


# ============================================================================
# EXPORT IN src/evidently/metrics/__init__.py
# ============================================================================

"""
Add to exports:

from .regression import RegressionErrorBiasTable

__all__ = [
    ...
    "RegressionErrorBiasTable",  # NEW
    ...
]
"""


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
# Example 1: Simple usage
from evidently import Report
from evidently.metrics import RegressionErrorBiasTable
import pandas as pd

current_df = pd.DataFrame({
    'target': [1, 2, 3, 4, 5],
    'prediction': [1.1, 2.2, 2.8, 4.1, 4.9],
    'age': [25, 35, 45, 55, 65],
    'income': [50000, 60000, 70000, 80000, 90000],
})

reference_df = pd.DataFrame({
    'target': [1, 2, 3, 4, 5],
    'prediction': [0.9, 2.1, 3.1, 3.9, 5.1],
    'age': [25, 35, 45, 55, 65],
    'income': [50000, 60000, 70000, 80000, 90000],
})

report = Report([
    RegressionErrorBiasTable(),
])

from evidently.core.datasets import Dataset
from evidently.core.data_definition import DataDefinition

definition = DataDefinition()
current = Dataset.from_pandas(current_df, data_definition=definition)
reference = Dataset.from_pandas(reference_df, data_definition=definition)

snapshot = report.run(current, reference)

# Example 2: With parameters
report = Report([
    RegressionErrorBiasTable(
        columns=['age', 'income'],  # Only analyze these
        top_error=0.1,  # Use 10th percentile instead of 5th
        regression_name='pricing_model',  # For multi-task regression
    ),
])

# Example 3: Combined with other metrics
report = Report([
    MAE(),
    RMSE(),
    RegressionErrorBiasTable(columns=['feature1', 'feature2']),
    RegressionPredictedVsActualScatter(),  # Another legacy migration
])
snapshot = report.run(current, reference)
"""


# ============================================================================
# TESTING
# ============================================================================

"""
# tests/metrics/regression_performance/test_error_bias_table_new_api.py

import pytest
import pandas as pd
from evidently import Report
from evidently.metrics import RegressionErrorBiasTable
from evidently.core.datasets import Dataset
from evidently.core.data_definition import DataDefinition, Regression

def test_regression_error_bias_table_new_api():
    current_df = pd.DataFrame({
        'target': [1.0, 2.0, 3.0, 4.0, 5.0],
        'prediction': [1.1, 2.2, 2.8, 4.1, 4.9],
        'feature1': [10, 20, 30, 40, 50],
    })
    
    reference_df = pd.DataFrame({
        'target': [1.0, 2.0, 3.0, 4.0, 5.0],
        'prediction': [0.9, 2.1, 3.1, 3.9, 5.1],
        'feature1': [10, 20, 30, 40, 50],
    })
    
    # Setup data
    data_definition = DataDefinition()
    data_definition.add_regression_task(
        Regression(target='target', prediction='prediction')
    )
    current = Dataset.from_pandas(current_df, data_definition=data_definition)
    reference = Dataset.from_pandas(reference_df, data_definition=data_definition)
    
    # Run report
    report = Report([RegressionErrorBiasTable()])
    snapshot = report.run(current, reference)
    
    # Verify results exist
    assert snapshot is not None
    metrics = snapshot.metrics
    assert len(metrics) > 0
    
    # Check metric result
    metric_result = snapshot.get_metric_result('RegressionErrorBiasTable')
    assert metric_result is not None
    assert metric_result.current is not None
    assert metric_result.current.value >= 0  # Number of features
"""
