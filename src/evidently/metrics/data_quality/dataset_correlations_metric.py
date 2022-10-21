from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.calculations.data_quality import calculate_correlations
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import HeatmapData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import get_heatmaps_widget
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class CorrelationStats:
    target_prediction_correlation: Optional[float] = None
    abs_max_target_features_correlation: Optional[float] = None
    abs_max_prediction_features_correlation: Optional[float] = None
    abs_max_correlation: Optional[float] = None
    abs_max_features_correlation: Optional[float] = None


@dataclasses.dataclass
class DatasetCorrelation:
    correlation: Dict[str, pd.DataFrame]
    stats: Dict[str, CorrelationStats]


@dataclasses.dataclass
class DatasetCorrelationsMetricResult:
    current: DatasetCorrelation
    reference: Optional[DatasetCorrelation]


class DatasetCorrelationsMetric(Metric[DatasetCorrelationsMetricResult]):
    """Calculate different correlations with target, predictions and features"""

    @staticmethod
    def _get_correlations_stats(correlation: pd.DataFrame, column_mapping: ColumnMapping) -> CorrelationStats:
        correlation_matrix = correlation.copy()
        target_name = column_mapping.target
        prediction_name = column_mapping.prediction
        columns = [i for i in correlation_matrix.columns if i not in [target_name, prediction_name]]
        # fill diagonal with 1 values for getting abs max values
        np.fill_diagonal(correlation_matrix.values, 0)

        if (
            isinstance(prediction_name, str)
            and prediction_name in correlation_matrix
            and target_name in correlation_matrix
        ):
            target_prediction_correlation = correlation_matrix.loc[prediction_name, target_name]

            if pd.isnull(target_prediction_correlation):
                target_prediction_correlation = None

        else:
            target_prediction_correlation = None

        if target_name in correlation_matrix:
            abs_max_target_features_correlation = correlation_matrix.loc[target_name, columns].abs().max()

            if pd.isnull(abs_max_target_features_correlation):
                abs_max_target_features_correlation = None

        else:
            abs_max_target_features_correlation = None

        if isinstance(prediction_name, str) and prediction_name in correlation_matrix:
            abs_max_prediction_features_correlation = correlation_matrix.loc[prediction_name, columns].abs().max()

            if pd.isnull(abs_max_prediction_features_correlation):
                abs_max_prediction_features_correlation = None

        else:
            abs_max_prediction_features_correlation = None

        abs_max_correlation = correlation_matrix.abs().max().max()

        if pd.isnull(abs_max_correlation):
            abs_max_correlation = None

        abs_max_features_correlation = correlation_matrix.loc[columns, columns].abs().max().max()

        if pd.isnull(abs_max_features_correlation):
            abs_max_features_correlation = None

        return CorrelationStats(
            target_prediction_correlation=target_prediction_correlation,
            abs_max_target_features_correlation=abs_max_target_features_correlation,
            abs_max_prediction_features_correlation=abs_max_prediction_features_correlation,
            abs_max_correlation=abs_max_correlation,
            abs_max_features_correlation=abs_max_features_correlation,
        )

    def _get_correlations(self, dataset: pd.DataFrame, column_mapping: ColumnMapping) -> DatasetCorrelation:
        columns = process_columns(dataset, column_mapping)
        correlations = calculate_correlations(dataset, columns)

        stats = {
            name: self._get_correlations_stats(correlation, column_mapping)
            for name, correlation in correlations.items()
        }

        return DatasetCorrelation(
            correlation=correlations,
            stats=stats,
        )

    def calculate(self, data: InputData) -> DatasetCorrelationsMetricResult:
        current_correlations = self._get_correlations(dataset=data.current_data, column_mapping=data.column_mapping)

        if data.reference_data is not None:
            reference_correlation: Optional[DatasetCorrelation] = self._get_correlations(
                dataset=data.reference_data, column_mapping=data.column_mapping
            )

        else:
            reference_correlation = None

        return DatasetCorrelationsMetricResult(
            current=current_correlations,
            reference=reference_correlation,
        )


@default_renderer(wrap_type=DatasetCorrelationsMetric)
class DataQualityCorrelationMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetCorrelationsMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result["current"].pop("correlation", None)

        if result["reference"]:
            result["reference"].pop("correlation", None)

        return result

    def _get_heatmaps(self, metric_result: DatasetCorrelationsMetricResult) -> BaseWidgetInfo:
        tabs = []

        for correlation_method in metric_result.current.correlation:
            current_correlation = metric_result.current.correlation[correlation_method]

            if metric_result.reference is not None:
                reference_heatmap_data: Optional[HeatmapData] = HeatmapData(
                    name="Reference", matrix=metric_result.reference.correlation[correlation_method]
                )

            else:
                reference_heatmap_data = None

            tabs.append(
                TabData(
                    title=correlation_method,
                    widget=get_heatmaps_widget(
                        primary_data=HeatmapData(name="Current", matrix=current_correlation),
                        secondary_data=reference_heatmap_data,
                        color_options=self.color_options,
                    ),
                )
            )

        return widget_tabs(title="", tabs=tabs)

    def render_html(self, obj: DatasetCorrelationsMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Dataset Correlations Metric"),
            self._get_heatmaps(metric_result=metric_result),
        ]
        return result
