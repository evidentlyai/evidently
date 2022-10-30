from typing import List
from typing import Optional

import dataclasses
from dataclasses import dataclass

from evidently.calculations.data_drift import get_drift_for_columns
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.utils.data_operations import process_columns


@dataclass
class DatasetDriftMetricResults:
    threshold: float
    number_of_columns: int
    number_of_drifted_columns: int
    share_of_drifted_columns: float
    dataset_drift: bool


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
            columns=self.columns,
        )
        return DatasetDriftMetricResults(
            threshold=self.threshold,
            number_of_columns=result.number_of_columns,
            number_of_drifted_columns=result.number_of_drifted_columns,
            share_of_drifted_columns=result.share_of_drifted_columns,
            dataset_drift=result.dataset_drift,
        )


@default_renderer(wrap_type=DatasetDriftMetric)
class DataDriftMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetDriftMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        return result

    def render_html(self, obj: DatasetDriftMetric) -> List[BaseWidgetInfo]:
        result = obj.get_result()

        if result.dataset_drift:
            drift_detected = "detected"

        else:
            drift_detected = "NOT detected"

        counters = [
            CounterData.int("Columns", result.number_of_columns),
            CounterData.int("Drifted Columns", result.number_of_drifted_columns),
            CounterData.float("Share of Drifted Columns", result.share_of_drifted_columns, 3),
        ]

        return [
            counter(
                counters=[
                    CounterData(
                        f"Dataset Drift is {drift_detected}. Dataset drift detection threshold is {result.threshold}",
                        "Dataset Drift",
                    )
                ],
                title="",
            ),
            counter(
                counters=counters,
                title="",
            ),
        ]
