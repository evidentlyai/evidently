from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently import ColumnType
from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.metric_types import DataframeMetric
from evidently.core.metric_types import DataframeValue
from evidently.core.metric_types import MetricId
from evidently.core.report import Context
from evidently.legacy.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetric
from evidently.legacy.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetricResult
from evidently.legacy.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetric
from evidently.legacy.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.html_widgets import header_text
from evidently.metrics._legacy import LegacyMetricCalculation


class ColumnCorrelations(MetricContainer):
    column_name: str

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        column_type = context.data_definition.get_column_type(self.column_name)
        if column_type == ColumnType.Numerical:
            return [
                ColumnCorrelationMatrix(column_name=self.column_name, kind="pearson"),
                ColumnCorrelationMatrix(column_name=self.column_name, kind="spearman"),
                ColumnCorrelationMatrix(column_name=self.column_name, kind="kendall"),
            ]
        if column_type == ColumnType.Categorical:
            return [
                ColumnCorrelationMatrix(column_name=self.column_name, kind="cramer_v"),
            ]
        return []

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        legacy_metric = ColumnCorrelationsMetric(column_name=self.column_name)
        _, legacy_widgets = context.get_legacy_metric(legacy_metric, None, None)
        return legacy_widgets


class ColumnCorrelationMatrix(DataframeMetric):
    column_name: str
    kind: Literal["auto", "pearson", "spearman", "kendall", "cramer_v"] = "auto"


class LegacyColumnCorrelationsCalculation(
    LegacyMetricCalculation[
        DataframeValue,
        ColumnCorrelationMatrix,
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
        kind: str = self.metric.kind if self.metric.kind != "auto" else next(iter(current_result.keys()))  # type: ignore[arg-type]
        current_correlations = current_result[kind]
        current_df = current_correlations.get_pandas()
        current_value = DataframeValue(display_name=self.display_name(), value=current_df)
        current_value.widget = _extract_render_tab(
            render, kind, title=f"Correlations for column '{self.metric.column_name}'"
        )
        reference_value = None
        if legacy_result.reference is not None:
            reference_result = legacy_result.reference[kind]
            reference_df = reference_result.get_pandas()
            reference_value = DataframeValue(display_name=self.display_name(), value=reference_df)
            reference_value.widget = []
        return current_value, reference_value

    def legacy_metric(self) -> ColumnCorrelationsMetric:
        return ColumnCorrelationsMetric(column_name=self.metric.column_name)


class DatasetCorrelations(MetricContainer):
    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        return [
            CorrelationMatrix(kind="pearson"),
            CorrelationMatrix(kind="spearman"),
            CorrelationMatrix(kind="kendall"),
            CorrelationMatrix(kind="cramer_v"),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        legacy_metric = DatasetCorrelationsMetric()
        _, legacy_widgets = context.get_legacy_metric(legacy_metric, None, None)
        return legacy_widgets


class CorrelationMatrix(DataframeMetric):
    kind: Literal["auto", "pearson", "spearman", "kendall", "cramer_v"] = "auto"


def _extract_render_tab(widgets: List[BaseWidgetInfo], kind: str, title: str) -> List[BaseWidgetInfo]:
    tabs_widgets = [w for w in widgets if w.type == "tabs"]
    if len(tabs_widgets) == 0:
        return []
    for tab in tabs_widgets[0].tabs:
        if tab.title == kind:
            return [header_text(label=f"{title} ({kind})"), tab.widget]
    return []


class LegacyDatasetCorrelationsCalculation(
    LegacyMetricCalculation[
        DataframeValue,
        CorrelationMatrix,
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
        kind: str = (
            self.metric.kind
            if self.metric.kind != "auto"
            else next(k for k, v in current_result.correlation.items() if len(v) > 0)
        )  # type: ignore[arg-type]
        current_df = current_result.correlation[kind]
        current_value = DataframeValue(display_name=self.display_name(), value=current_df)
        current_value.widget = _extract_render_tab(render, kind, title="Dataset Correlations")
        reference_value = None
        if legacy_result.reference is not None:
            reference_df = legacy_result.reference.correlation[kind]
            reference_value = DataframeValue(display_name=self.display_name(), value=reference_df)
            reference_value.widget = []
        return current_value, reference_value

    def display_name(self) -> str:
        return """Calculate different correlations with target, predictions and features"""
