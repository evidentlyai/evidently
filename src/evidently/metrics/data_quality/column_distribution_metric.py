from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_column_type
from evidently.utils.visualizations import get_distribution_for_column
from evidently.utils.visualizations import plot_distr


@dataclasses.dataclass
class ColumnDistributionMetricResult:
    column_name: str
    column_type: str
    current: pd.Series
    reference: Optional[pd.Series] = None


class ColumnDistributionMetric(Metric[ColumnDistributionMetricResult]):
    """Calculates distribution for the column"""

    column_name: str

    def __init__(self, column_name: str) -> None:
        self.column_name = column_name

    def calculate(self, data: InputData) -> ColumnDistributionMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column {self.column_name} is not in current data.")

        current_column = data.current_data[self.column_name]

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column {self.column_name} is not in reference data.")

            reference_column = data.reference_data[self.column_name]
            column_type_recognize_data = data.reference_data

        else:
            reference_column = None
            column_type_recognize_data = data.current_data

        columns = process_columns(column_type_recognize_data, data.column_mapping)
        column_type = recognize_column_type(
            dataset=column_type_recognize_data, column_name=self.column_name, columns=columns
        )

        distribution_for_plot = get_distribution_for_column(
            column_name=self.column_name,
            column_type=column_type,
            current=current_column,
            reference=reference_column,
        )
        return ColumnDistributionMetricResult(
            column_name=self.column_name,
            column_type=column_type,
            current=distribution_for_plot["current"],
            reference=distribution_for_plot.get("reference"),
        )


@default_renderer(wrap_type=ColumnDistributionMetric)
class ColumnDistributionMetricRenderer(MetricRenderer):
    def render_json(self, obj: ColumnDistributionMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("current_distribution", None)
        result.pop("reference_distribution", None)
        return result

    def render_html(self, obj: ColumnDistributionMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label=f"Distribution for column '{metric_result.column_name}'."),
            plot_distr(metric_result.current, metric_result.reference),
        ]
        return result
