from typing import Dict
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
    # calculated value of the quantile
    value: float
    # range of the quantile (from 0 to 1)
    quantile: float
    distr_for_plot: Dict[str, pd.DataFrame]
    ref_value: Optional[float]


class DataQualityValueQuantileMetric(Metric[DataQualityValueQuantileMetricResults]):
    """Calculates quantile with specified range"""

    column_name: str
    quantile: float

    def __init__(self, column_name: str, quantile: float) -> None:
        if quantile is not None:
            if not 0 <= quantile <= 1:
                raise ValueError("Quantile should all be in the interval [0, 1].")

        self.column_name = column_name
        self.quantile = quantile

    def calculate(self, data: InputData) -> DataQualityValueQuantileMetricResults:
        curr_feature = data.current_data[self.column_name]
        ref_feature = None
        ref_value = None

        if data.reference_data is not None:
            ref_feature = data.reference_data[self.column_name]
            ref_value = data.reference_data[self.column_name].quantile(self.quantile)

        distr_for_plot = make_hist_for_num_plot(curr_feature, ref_feature)
        return DataQualityValueQuantileMetricResults(
            column_name=self.column_name,
            value=data.current_data[self.column_name].quantile(self.quantile),
            quantile=self.quantile,
            distr_for_plot=distr_for_plot,
            ref_value=ref_value,
        )


@default_renderer(wrap_type=DataQualityValueQuantileMetric)
class DataQualityValueQuantileMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueQuantileMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("distr_for_plot", None)
        return result

    def render_html(self, obj: DataQualityValueQuantileMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        column_name = metric_result.column_name
        counters = [
            CounterData.float(label="Quantile", value=metric_result.quantile, precision=3),
            CounterData.float(label="Current dataset value", value=metric_result.value, precision=3),
        ]

        if metric_result.ref_value:
            counters.append(
                CounterData.float(label="Reference dataset value", value=metric_result.ref_value, precision=3),
            )

        result = [
            header_text(label=f"Data Value Quantile Metrics for the column: {column_name}"),
            counter(counters=counters),
        ]
        return result
