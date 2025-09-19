from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import DataframeValue
from evidently.core.metric_types import Metric
from evidently.core.report import Context
from evidently.legacy.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetric
from evidently.legacy.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetricResult
from evidently.legacy.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetric
from evidently.legacy.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.metrics._legacy import LegacyMetricCalculation


class ColumnCorrelations(Metric):
    column_name: str

    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        return []


class LegacyColumnCorrelationsCalculation(
    LegacyMetricCalculation[
        DataframeValue,
        ColumnCorrelations,
        ColumnCorrelationsMetricResult,
        ColumnCorrelationsMetric,
    ],
):
    def display_name(self) -> str:
        return f"Correlations between {self.metric.column_name} column and all the other columns."

    def calculate_value(
        self, context: "Context", legacy_result: ColumnCorrelationsMetricResult, render: List[BaseWidgetInfo]
    ) -> Tuple[DataframeValue, Optional[DataframeValue]]:
        current_result = legacy_result.current
        current_correlations = next(iter(current_result.values()))
        current_df = current_correlations.get_pandas()
        current_value = DataframeValue(display_name=self.display_name(), value=current_df)
        current_value.widget = render
        reference_value = None
        if legacy_result.reference is not None:
            reference_result = next(iter(legacy_result.reference.values()))
            reference_df = reference_result.get_pandas()
            reference_value = DataframeValue(display_name=self.display_name(), value=reference_df)
            reference_value.widget = []
        return current_value, reference_value

    def legacy_metric(self) -> ColumnCorrelationsMetric:
        return ColumnCorrelationsMetric(column_name=self.metric.column_name)


class DatasetCorrelations(Metric):
    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        return []


class LegacyDatasetCorrelationsCalculation(
    LegacyMetricCalculation[
        DataframeValue,
        DatasetCorrelations,
        DatasetCorrelationsMetricResult,
        DatasetCorrelationsMetric,
    ],
):
    def legacy_metric(self) -> DatasetCorrelationsMetric:
        return DatasetCorrelationsMetric()

    def calculate_value(
        self, context: "Context", legacy_result: DatasetCorrelationsMetricResult, render: List[BaseWidgetInfo]
    ) -> Tuple[DataframeValue, Optional[DataframeValue]]:
        current_result = legacy_result.current
        current_df = next(iter(current_result.correlation.values()))
        current_value = DataframeValue(display_name=self.display_name(), value=current_df)
        current_value.widget = render
        reference_value = None
        if legacy_result.reference is not None:
            reference_df = next(iter(legacy_result.reference.correlation.values()))
            reference_value = DataframeValue(display_name=self.display_name(), value=reference_df)
            reference_value.widget = []
        return current_value, reference_value

    def display_name(self) -> str:
        return """Calculate different correlations with target, predictions and features"""
