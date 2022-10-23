from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently import ColumnMapping
from evidently.calculations.data_quality import calculate_column_distribution
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import HistogramData
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import histogram
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_column_type
from evidently.utils.types import ColumnDistribution


@dataclasses.dataclass
class ColumnDistributionMetricResult:
    column_name: str
    current: ColumnDistribution
    reference: Optional[ColumnDistribution] = None


class ColumnDistributionMetric(Metric[ColumnDistributionMetricResult]):
    """Calculates distribution for the column"""

    column_name: str

    def __init__(
        self,
        column_name: str,
    ) -> None:
        self.column_name = column_name

    @staticmethod
    def _calculate_distribution(
        column_name: str, dataset: pd.DataFrame, column_mapping: ColumnMapping
    ) -> ColumnDistribution:
        columns = process_columns(dataset, column_mapping)
        column_type = recognize_column_type(dataset=dataset, column_name=column_name, columns=columns)
        return calculate_column_distribution(dataset[column_name], column_type)

    def calculate(self, data: InputData) -> ColumnDistributionMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column '{self.column_name}' was not found in current data.")

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column '{self.column_name}' was not found in reference data.")

        current = self._calculate_distribution(self.column_name, data.current_data, data.column_mapping)

        if data.reference_data is not None:
            reference: Optional[ColumnDistribution] = self._calculate_distribution(
                self.column_name, data.reference_data, data.column_mapping
            )

        else:
            reference = None

        return ColumnDistributionMetricResult(
            column_name=self.column_name,
            current=current,
            reference=reference,
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
        current_histogram = HistogramData(
            name="current",
            x=list(metric_result.current.keys()),
            y=list(metric_result.current.values()),
        )

        if metric_result.reference is not None:
            reference_histogram: Optional[HistogramData] = HistogramData(
                name="reference",
                x=list(metric_result.reference.keys()),
                y=list(metric_result.reference.values()),
            )

        else:
            reference_histogram = None

        result = [
            header_text(label=f"Distribution for column '{metric_result.column_name}'."),
            histogram(
                title="",
                primary_hist=current_histogram,
                secondary_hist=reference_histogram,
                color_options=self.color_options,
                xaxis_title=metric_result.column_name,
                yaxis_title="Count",
            ),
        ]
        return result
