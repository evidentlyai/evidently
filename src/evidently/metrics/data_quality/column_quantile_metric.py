from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd

from evidently.base_metric import ColumnMetricResult
from evidently.base_metric import ColumnName
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import ColumnType
from evidently.metric_results import Distribution
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import AnyOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import HistogramData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import get_histogram_figure_with_quantile
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.visualizations import get_distribution_for_column


class QuantileStats(MetricResult):
    value: float
    # calculated value of the quantile
    distribution: Distribution
    # distribution for the column


class ColumnQuantileMetricResult(ColumnMetricResult):
    # range of the quantile (from 0 to 1)
    quantile: float
    current: QuantileStats
    reference: Optional[QuantileStats] = None


class ColumnQuantileMetric(Metric[ColumnQuantileMetricResult]):
    """Calculates quantile with specified range"""

    column_name: ColumnName
    quantile: float

    def __init__(self, column_name: Union[str, ColumnName], quantile: float, options: AnyOptions = None) -> None:
        self.quantile = quantile
        self.column_name = ColumnName.from_any(column_name)
        super().__init__(options=options)

    def calculate(self, data: InputData) -> ColumnQuantileMetricResult:
        if not 0 < self.quantile <= 1:
            raise ValueError("Quantile should all be in the interval (0, 1].")

        if not data.has_column(self.column_name):
            raise ValueError(f"Column '{self.column_name}' is not in data.")

        column_type, current_column, reference_column = data.get_data(self.column_name)

        if not pd.api.types.is_numeric_dtype(current_column.dtype):
            raise ValueError(f"Column '{self.column_name}' in current data is not numeric.")

        current_quantile = current_column.quantile(self.quantile)

        if reference_column is not None:
            if not pd.api.types.is_numeric_dtype(reference_column.dtype):
                raise ValueError(f"Column '{self.column_name}' in reference data is not numeric.")

            reference_quantile = reference_column.quantile(self.quantile)
            reference_column = reference_column.replace([np.inf, -np.inf], np.nan)

        else:
            reference_column = None
            reference_quantile = None

        distributions = get_distribution_for_column(
            column_type="num", current=current_column.replace([np.inf, -np.inf], np.nan), reference=reference_column
        )
        reference = None
        if reference_quantile is not None:
            reference = QuantileStats(
                value=reference_quantile,
                distribution=distributions[1],
            )
        return ColumnQuantileMetricResult(
            column_name=self.column_name.display_name,
            column_type=ColumnType.Numerical.value,
            current=QuantileStats(
                value=current_quantile,
                distribution=distributions[0],
            ),
            quantile=self.quantile,
            reference=reference,
        )


@default_renderer(wrap_type=ColumnQuantileMetric)
class ColumnQuantileMetricRenderer(MetricRenderer):
    @staticmethod
    def _get_counters(metric_result: ColumnQuantileMetricResult) -> BaseWidgetInfo:
        counters = [
            CounterData.float(label="Quantile", value=metric_result.quantile, precision=3),
            CounterData.float(
                label="Quantile value (current)",
                value=metric_result.current.value,
                precision=3,
            ),
        ]

        if metric_result.reference is not None:
            counters.append(
                CounterData.float(
                    label="Quantile value (reference)",
                    value=metric_result.reference.value,
                    precision=3,
                ),
            )
        return counter(counters=counters)

    def _get_histogram(self, metric_result: ColumnQuantileMetricResult) -> BaseWidgetInfo:
        if metric_result.reference is not None:
            reference_histogram_data: Optional[HistogramData] = HistogramData.from_distribution(
                metric_result.reference.distribution,
                name="reference",
            )

        else:
            reference_histogram_data = None

        if metric_result.reference is not None:
            reference_quantile: Optional[float] = metric_result.reference.value

        else:
            reference_quantile = None

        figure = get_histogram_figure_with_quantile(
            current=HistogramData.from_distribution(
                metric_result.current.distribution,
                name="current",
            ),
            reference=reference_histogram_data,
            current_quantile=metric_result.current.value,
            reference_quantile=reference_quantile,
            color_options=self.color_options,
        )
        figure.update_layout(
            yaxis_title="count",
            xaxis_title=metric_result.column_name,
        )
        return plotly_figure(title="", figure=figure)

    def render_html(self, obj: ColumnQuantileMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        column_name = metric_result.column_name
        return [
            header_text(label=f"Column '{column_name}'. Quantile."),
            self._get_counters(metric_result),
            self._get_histogram(metric_result),
        ]
