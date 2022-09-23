from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently.calculations.data_drift import calculate_data_drift
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import WidgetType
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_task
from evidently.utils.types import Numeric


@dataclasses.dataclass
class ColumnDriftMetricResults:
    column_name: str
    column_type: str
    stattest_name: str
    threshold: Optional[float]
    drift_value: Numeric
    drift_detected: bool
    distr_for_plots: Dict[str, pd.DataFrame]


class ColumnDriftMetric(Metric[ColumnDriftMetricResults]):
    """Calculate drift metric for a column"""

    column_name: str
    options: DataDriftOptions

    def __init__(
        self,
        column_name: str,
        options: Optional[DataDriftOptions] = None,
    ):
        self.column_name = column_name

        if options is None:
            self.options = DataDriftOptions()

        else:
            self.options = options

    def calculate(self, data: InputData) -> ColumnDriftMetricResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        if self.column_name not in data.current_data:
            raise ValueError(f"Cannot find column {self.column_name} in current dataset")

        if self.column_name not in data.reference_data:
            raise ValueError(f"Cannot find column {self.column_name} in reference dataset")

        columns = process_columns(data.reference_data, data.column_mapping)
        target_name = columns.utility_columns.target

        task: Optional[str] = None

        if data.column_mapping.task is not None:
            task = data.column_mapping.task

        elif data.column_mapping.task is None and target_name:
            task = recognize_task(target_name, data.reference_data)

        column_type = columns.get_column_type(column_name=self.column_name, task=task)

        if column_type not in ["cat", "num"]:
            raise ValueError(f"Column type {column_type} is not supported by ColumnDriftMetric")

        stattest = self.options.get_feature_stattest_func(self.column_name, column_type)

        threshold = self.options.get_threshold(self.column_name)

        drift_result = calculate_data_drift(
            current_data=data.current_data,
            reference_data=data.reference_data,
            column_name=self.column_name,
            stattest=stattest,
            threshold=threshold,
            feature_type=column_type,
        )

        if column_type == "cat":
            distr_for_plots = make_hist_for_cat_plot(
                data.current_data[self.column_name], data.reference_data[self.column_name]
            )

        elif column_type == "num":
            distr_for_plots = make_hist_for_num_plot(
                data.current_data[self.column_name], data.reference_data[self.column_name]
            )

        else:
            raise ValueError(f"Column type {column_type} is not supported by ColumnDriftMetric")

        return ColumnDriftMetricResults(
            column_name=self.column_name,
            column_type=column_type,
            stattest_name=drift_result.stattest_name,
            threshold=drift_result.threshold,
            drift_value=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            distr_for_plots=distr_for_plots,
        )


@default_renderer(wrap_type=ColumnDriftMetric)
class ColumnDriftMetricRenderer(MetricRenderer):
    def render_html(self, obj: ColumnDriftMetric) -> List[MetricHtmlInfo]:
        result = obj.get_result()
        return [
            MetricHtmlInfo(
                "column_data_drift_title",
                BaseWidgetInfo(
                    type=str(WidgetType.COUNTER.value),
                    title="",
                    size=2,
                    params={"counters": [{"value": "", "label": f"Column Data Drift: {result.drift_detected}"}]},
                ),
                details=[],
            )
        ]

    def render_json(self, obj: ColumnDriftMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        # remove distribution data with pandas dataframes
        result.pop("distr_for_plots", None)
        return result
