from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently.calculations.data_drift import calculate_column_data_drift
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.utils import get_distribution_for_column
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.render_utils import plot_distr
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_column_type
from evidently.utils.types import Numeric


@dataclasses.dataclass
class ColumnDriftMetricResults:
    column_name: str
    column_type: str
    stattest_name: str
    threshold: Optional[float]
    drift_score: Numeric
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
        column_type = recognize_column_type(self.column_name, columns)

        if column_type not in ("cat", "num"):
            raise ValueError(f"Cannot calculate drift metric for column {self.column_name} with type {column_type}")

        drift_result = calculate_column_data_drift(
            column_name=self.column_name,
            column_type=column_type,
            current_data=data.current_data,
            reference_data=data.reference_data,
            drift_options=self.options,
        )
        distribution_for_plot = get_distribution_for_column(
            column_name=self.column_name,
            column_type=column_type,
            current_data=data.current_data,
            reference_data=data.reference_data,
        )

        return ColumnDriftMetricResults(
            column_name=drift_result.column_name,
            column_type=column_type,
            stattest_name=drift_result.stattest_name,
            threshold=drift_result.threshold,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            distr_for_plots=distribution_for_plot,
        )


@default_renderer(wrap_type=ColumnDriftMetric)
class ColumnDriftMetricRenderer(MetricRenderer):
    def render_html(self, obj: ColumnDriftMetric) -> List[MetricHtmlInfo]:
        result = obj.get_result()

        if result.drift_detected:
            drift = "detected"

        else:
            drift = "not detected"

        drift_score = round(result.drift_score, 3)

        fig = plot_distr(result.distr_for_plots["current"], result.distr_for_plots["reference"])
        fig_json = fig.to_plotly_json()
        return [
            MetricHtmlInfo(
                "column_data_drift_title",
                header_text(
                    label=f"Column '{result.column_name}' Data Drift: {drift}, "
                    f"Drift Score: {drift_score} ({result.stattest_name})"
                ),
            ),
            MetricHtmlInfo(
                "column_data_drift_distribution",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            ),
        ]

    def render_json(self, obj: ColumnDriftMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        # remove distribution data with pandas dataframes
        result.pop("distr_for_plots", None)
        return result
