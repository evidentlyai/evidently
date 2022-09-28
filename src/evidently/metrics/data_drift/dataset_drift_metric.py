from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.data_drift import DataDriftAnalyzerMetrics
from evidently.calculations.data_drift import calculate_all_drifts_for_metrics
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import DatasetColumns


@dataclass
class DatasetDriftMetricResults:
    threshold: float
    options: DataDriftOptions
    columns: DatasetColumns
    metrics: DataDriftAnalyzerMetrics
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]


class DatasetDriftMetric(Metric[DatasetDriftMetricResults]):
    threshold: float
    options: DataDriftOptions

    def __init__(self, threshold: float = 0.5, options: Optional[DataDriftOptions] = None):
        self.threshold = threshold

        if options is None:
            self.options = DataDriftOptions()

        else:
            self.options = options

    def get_parameters(self) -> tuple:
        return tuple((self.options,))

    def calculate(self, data: InputData) -> DatasetDriftMetricResults:
        result = calculate_all_drifts_for_metrics(data, self.options)
        return DatasetDriftMetricResults(
            threshold=self.threshold,
            options=self.options,
            columns=result.columns,
            metrics=result.metrics,
            distr_for_plots=result.distr_for_plots,
        )


@default_renderer(wrap_type=DatasetDriftMetric)
class DataDriftMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetDriftMetric) -> dict:
        return dataclasses.asdict(obj.get_result().metrics)

    def render_html(self, obj: DatasetDriftMetric) -> List[MetricHtmlInfo]:
        result = obj.get_result()

        if result.metrics.dataset_drift:
            drift_detected = "detected"

        else:
            drift_detected = "not detected"

        return [
            MetricHtmlInfo(
                "dataset_drift_title",
                header_text(label=f"Dataset Drift is {drift_detected}"),
            ),
            MetricHtmlInfo(
                "dataset_drift_threshold",
                header_text(label=f"Dataset Drift Threshold is {result.threshold}"),
            ),
        ]
