from typing import List
from typing import Optional

import dataclasses
from dataclasses import dataclass

from evidently.calculations.data_drift import DatasetDriftMetrics
from evidently.calculations.data_drift import get_drift_for_columns
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


@dataclass
class DatasetDriftMetricResults:
    threshold: float
    options: DataDriftOptions
    columns: DatasetColumns
    metrics: DatasetDriftMetrics


class DatasetDriftMetric(Metric[DatasetDriftMetricResults]):
    columns: Optional[List[str]]
    threshold: float
    options: DataDriftOptions

    def __init__(
        self, columns: Optional[List[str]] = None, threshold: float = 0.5, options: Optional[DataDriftOptions] = None
    ):
        self.columns = columns
        self.threshold = threshold

        if options is None:
            self.options = DataDriftOptions()

        else:
            self.options = options

    def get_parameters(self) -> tuple:
        return self.threshold, self.columns, self.options

    def calculate(self, data: InputData) -> DatasetDriftMetricResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        dataset_columns = process_columns(data.reference_data, data.column_mapping)
        result = get_drift_for_columns(
            current_data=data.current_data,
            reference_data=data.reference_data,
            data_drift_options=self.options,
            drift_share_threshold=self.threshold,
            dataset_columns=dataset_columns,
        )
        return DatasetDriftMetricResults(
            threshold=self.threshold,
            options=self.options,
            columns=result.columns,
            metrics=result,
        )


@default_renderer(wrap_type=DatasetDriftMetric)
class DataDriftMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetDriftMetric) -> dict:
        result = dataclasses.asdict(obj.get_result().metrics)
        result.pop("metrics", None)
        return result

    def render_html(self, obj: DatasetDriftMetric) -> List[MetricHtmlInfo]:
        result = obj.get_result()

        if result.metrics.dataset_drift:
            drift_detected = "detected"

        else:
            drift_detected = "NOT detected"

        counters = [
            CounterData.int("Columns", result.metrics.n_features),
            CounterData.int("Drifted Columns", result.metrics.n_drifted_features),
            CounterData.float("Dataset Drift Score", result.metrics.share_drifted_features, 3),
        ]

        return [
            MetricHtmlInfo(
                "dataset_drift_title",
                header_text(label=f"Dataset Drift is {drift_detected}"),
            ),
            MetricHtmlInfo(
                "dataset_drift_threshold",
                header_text(label=f"Dataset Drift Threshold is {result.threshold}"),
            ),
            MetricHtmlInfo(
                "dataset_drift_details",
                counter(
                    counters=counters,
                    title="Dataset Drift Details",
                ),
            ),
        ]
