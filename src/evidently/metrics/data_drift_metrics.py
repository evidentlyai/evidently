import dataclasses
from typing import Dict
from typing import List
from typing import Optional
from dataclasses import dataclass

import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.calculations.data_drift import get_overall_data_drift
from evidently.calculations.data_drift import DataDriftAnalyzerMetrics
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider
from evidently.utils.data_operations import process_columns


@dataclass
class DataDriftMetricsResults:
    options: DataDriftOptions
    metrics: DataDriftAnalyzerMetrics
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]


class DataDriftMetrics(Metric[DataDriftMetricsResults]):
    options: Optional[DataDriftOptions]

    def __init__(self, options: Optional[DataDriftOptions] = None):
        self.options = options

    def get_parameters(self) -> tuple:
        return tuple((self.options,))

    def calculate(self, data: InputData) -> DataDriftMetricsResults:
        columns = process_columns(data.current_data, data.column_mapping)
        options_provider: OptionsProvider = OptionsProvider()

        if self.options is not None:
            options_provider.add(self.options)

        options = options_provider.get(DataDriftOptions)

        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        drift_metrics = get_overall_data_drift(
            current_data=data.current_data,
            reference_data=data.reference_data,
            columns=columns,
            data_drift_options=options,
        )
        distr_for_plots = {}

        for feature in columns.num_feature_names:
            distr_for_plots[feature] = make_hist_for_num_plot(data.current_data[feature], data.reference_data[feature])

        for feature in columns.cat_feature_names:
            distr_for_plots[feature] = make_hist_for_cat_plot(data.current_data[feature], data.reference_data[feature])

        return DataDriftMetricsResults(options=options, metrics=drift_metrics, distr_for_plots=distr_for_plots)


@default_renderer(wrap_type=DataDriftMetrics)
class DataDriftMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataDriftMetrics) -> dict:
        return dataclasses.asdict(obj.get_result())

    @staticmethod
    def _get_features_drift_table(metrics: DataDriftAnalyzerMetrics) -> MetricHtmlInfo:
        headers = ["Column Name", "Drift", "Drift Score", "Stattest", "Threshold"]
        data = []

        for column_name, drift_info in metrics.features.items():
            data.append(
                (
                    column_name,
                    "drift was detected" if drift_info.drift_detected else "no drift",
                    f"{drift_info.p_value:.3f}",
                    f"{drift_info.stattest_name}",
                    f"{drift_info.threshold}"
                )
            )

        return MetricHtmlInfo(
            "data_drift_features",
            BaseWidgetInfo(
                title="Data Drift Scores",
                type=BaseWidgetInfo.WIDGET_INFO_TYPE_TABLE,
                size=2,
                params={"header": headers, "data": data},
            ),
            details=[],
        )

    def render_html(self, obj: DataDriftMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        metrics = metric_result.metrics
        if metrics.dataset_drift:
            dataset_drift = "drift was detected"

        else:
            dataset_drift = "drift was not detected"

        if metrics.n_drifted_features:
            features_drift = (
                f"{metrics.n_drifted_features} of {metrics.n_features} features "
                f"({round(metrics.share_drifted_features, 3)}%)"
            )

        else:
            features_drift = "no drifted features"

        result = [
            MetricHtmlInfo(
                "data_drift_title",
                BaseWidgetInfo(
                    type=BaseWidgetInfo.WIDGET_INFO_TYPE_COUNTER,
                    title="",
                    size=2,
                    params={"counters": [{"value": "", "label": "Data Drift"}]},
                ),
                details=[],
            ),
            MetricHtmlInfo(
                "data_drift_overview",
                BaseWidgetInfo(
                    type=BaseWidgetInfo.WIDGET_INFO_TYPE_COUNTER,
                    title="",
                    size=2,
                    params={"counters": [{
                        "value": "",
                        "label": f"Dataset Drift: {dataset_drift}. Features Drift: {features_drift}"}]},
                ),
                details=[],
            ),
            self._get_features_drift_table(metrics=metrics),
        ]
        return result
