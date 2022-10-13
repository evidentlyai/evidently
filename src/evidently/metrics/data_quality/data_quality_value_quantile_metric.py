from typing import List
from typing import Optional

import dataclasses
import pandas as pd
from dataclasses import dataclass

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.utils.visualizations import make_hist_for_num_plot


@dataclass
class DataQualityValueQuantileMetricResults:
    column_name: str
    # range of the quantile (from 0 to 1)
    quantile: float
    # calculated value of the quantile in current data
    current: float
    # calculated value of the quantile in reference data
    reference: Optional[float] = None
    # distributions for the column
    current_distribution: Optional[pd.DataFrame] = None
    reference_distribution: Optional[pd.DataFrame] = None


class DataQualityValueQuantileMetric(Metric[DataQualityValueQuantileMetricResults]):
    """Calculates quantile with specified range"""

    column_name: str
    quantile: float

    def __init__(self, column_name: str, quantile: float) -> None:
        self.quantile = quantile
        self.column_name = column_name

    def calculate(self, data: InputData) -> DataQualityValueQuantileMetricResults:
        if not 0 < self.quantile <= 1:
            raise ValueError("Quantile should all be in the interval (0, 1].")

        if self.column_name not in data.current_data:
            raise ValueError(f"Column '{self.column_name}' is not in current data.")

        current_column = data.current_data[self.column_name]

        if not pd.api.types.is_numeric_dtype(current_column.dtype):
            raise ValueError(f"Column '{self.column_name}' in current data is not numeric.")

        current_quantile = data.current_data[self.column_name].quantile(self.quantile)

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column '{self.column_name}' is not in reference data.")

            reference_column = data.reference_data[self.column_name]

            if not pd.api.types.is_numeric_dtype(reference_column.dtype):
                raise ValueError(f"Column '{self.column_name}' in reference data is not numeric.")

            reference_quantile = reference_column.quantile(self.quantile)

        else:
            reference_column = None
            reference_quantile = None

        distributions = make_hist_for_num_plot(current_column, reference_column)
        return DataQualityValueQuantileMetricResults(
            column_name=self.column_name,
            current=current_quantile,
            quantile=self.quantile,
            current_distribution=distributions["current"],
            reference_distribution=distributions.get("reference"),
            reference=reference_quantile,
        )


@default_renderer(wrap_type=DataQualityValueQuantileMetric)
class DataQualityValueQuantileMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueQuantileMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("current_distribution", None)
        result.pop("reference_distribution", None)
        return result

    def render_html(self, obj: DataQualityValueQuantileMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        column_name = metric_result.column_name
        counters = [
            CounterData.float(label="Quantile", value=metric_result.quantile, precision=3),
            CounterData.float(label="Current dataset value", value=metric_result.current, precision=3),
        ]

        if metric_result.reference is not None:
            counters.append(
                CounterData.float(label="Reference dataset value", value=metric_result.reference, precision=3),
            )

        result = [
            header_text(label=f"Data Value Quantile Metrics for the column: {column_name}"),
            counter(counters=counters),
        ]
        return result
