from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd

from evidently.calculations.data_quality import get_rows_count
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import HistogramData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import get_histogram_figure_with_range
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.types import Numeric
from evidently.utils.visualizations import Distribution
from evidently.utils.visualizations import get_distribution_for_column


@dataclasses.dataclass
class ValuesInRangeStat:
    number_in_range: int
    number_not_in_range: int
    share_in_range: float
    share_not_in_range: float
    # number of rows without null-like values
    number_of_values: int


@dataclasses.dataclass
class ColumnValueRangeMetricResult:
    column_name: str
    left: Numeric
    right: Numeric
    current: ValuesInRangeStat
    current_distribution: Distribution
    reference: Optional[ValuesInRangeStat] = None
    reference_distribution: Optional[Distribution] = None

    def __eq__(self, other):
        return (
            self.column_name == other.column_name
            and self.left == other.left
            and self.right == other.right
            and self.current == other.current
            and self.reference == other.reference
        )


class ColumnValueRangeMetric(Metric[ColumnValueRangeMetricResult]):
    """Calculates count and shares of values in the predefined values range"""

    column_name: str
    left: Optional[Numeric]
    right: Optional[Numeric]

    def __init__(self, column_name: str, left: Optional[Numeric] = None, right: Optional[Numeric] = None) -> None:
        self.left = left
        self.right = right
        self.column_name = column_name

    @staticmethod
    def _calculate_in_range_stats(column: pd.Series, left: Numeric, right: Numeric) -> ValuesInRangeStat:
        column = column.dropna()
        rows_count = get_rows_count(column)

        if rows_count == 0:
            number_in_range = 0
            number_not_in_range = 0
            share_in_range = 0.0
            share_not_in_range = 0.0

        else:
            number_in_range = column.between(left=float(left), right=float(right), inclusive="both").sum()
            number_not_in_range = rows_count - number_in_range
            share_in_range = number_in_range / rows_count
            share_not_in_range = number_not_in_range / rows_count

        return ValuesInRangeStat(
            number_in_range=number_in_range,
            number_not_in_range=number_not_in_range,
            share_in_range=share_in_range,
            share_not_in_range=share_not_in_range,
            number_of_values=rows_count,
        )

    def calculate(self, data: InputData) -> ColumnValueRangeMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column {self.column_name} is not in current data.")

        if not pd.api.types.is_numeric_dtype(data.current_data[self.column_name].dtype):
            raise ValueError(f"Column {self.column_name} in current data should be numeric.")

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column {self.column_name} is not in reference data.")

            if not pd.api.types.is_numeric_dtype(data.reference_data[self.column_name].dtype):
                raise ValueError(f"Column {self.column_name} in reference data should be numeric.")

        if self.left is None:
            if data.reference_data is None:
                raise ValueError("Reference should be present")

            else:
                left: Numeric = float(data.reference_data[self.column_name].min())

        else:
            left = self.left

        if self.right is None:
            if data.reference_data is None:
                raise ValueError("Reference should be present")

            else:
                right: Numeric = float(data.reference_data[self.column_name].max())

        else:
            right = self.right

        current = self._calculate_in_range_stats(data.current_data[self.column_name], left, right)

        if data.reference_data is None:
            reference_column = None
            reference = None

        else:
            reference_column = data.reference_data[self.column_name]
            reference = self._calculate_in_range_stats(data.reference_data[self.column_name], left, right)

        # calculate distribution for visualisation
        current_column = data.current_data[self.column_name]
        distributions = get_distribution_for_column(
            column_type="num",
            current=current_column,
            reference=reference_column,
        )

        return ColumnValueRangeMetricResult(
            column_name=self.column_name,
            left=left,
            right=right,
            current=current,
            reference=reference,
            current_distribution=distributions[0],
            reference_distribution=distributions[1],
        )


@default_renderer(wrap_type=ColumnValueRangeMetric)
class ColumnValueRangeMetricRenderer(MetricRenderer):
    def render_json(self, obj: ColumnValueRangeMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("current_distribution", None)
        result.pop("reference_distribution", None)
        return result

    @staticmethod
    def _get_table_stat(metric_result: ColumnValueRangeMetricResult) -> BaseWidgetInfo:
        matched_stat_headers = ["Metric", "Current"]
        matched_stat = [
            ["Values in range", metric_result.current.number_in_range],
            ["%", np.round(metric_result.current.share_in_range * 100, 3)],
            ["Values out of range", metric_result.current.number_not_in_range],
            ["%", np.round(metric_result.current.share_not_in_range * 100, 3)],
            ["Values count", metric_result.current.number_of_values],
        ]

        if metric_result.reference is not None:
            matched_stat_headers.append("Reference")

            matched_stat[0].append(metric_result.reference.number_in_range)
            matched_stat[1].append(np.round(metric_result.reference.share_in_range * 100, 3))
            matched_stat[2].append(metric_result.reference.number_not_in_range)
            matched_stat[3].append(np.round(metric_result.reference.share_not_in_range * 100, 3))
            matched_stat[4].append(metric_result.reference.number_of_values)

        return table_data(
            title="",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def _get_tabs(
        self,
        metric_result: ColumnValueRangeMetricResult,
    ) -> BaseWidgetInfo:
        if metric_result.reference_distribution is not None:
            reference_histogram: Optional[HistogramData] = HistogramData(
                name="reference",
                x=list(metric_result.reference_distribution.x),
                y=list(metric_result.reference_distribution.y),
            )

        else:
            reference_histogram = None

        figure = get_histogram_figure_with_range(
            primary_hist=HistogramData(
                name="current",
                x=list(metric_result.current_distribution.x),
                y=list(metric_result.current_distribution.y),
            ),
            secondary_hist=reference_histogram,
            color_options=self.color_options,
            left=metric_result.left,
            right=metric_result.right,
        )
        figure.update_layout(
            yaxis_title="count",
            xaxis_title=metric_result.column_name,
        )

        tabs: List[TabData] = [
            TabData(
                title="Distribution",
                widget=plotly_figure(title="", figure=figure),
            ),
            TabData(
                title="Statistics",
                widget=self._get_table_stat(metric_result),
            ),
        ]
        return widget_tabs(
            title="",
            tabs=tabs,
        )

    @staticmethod
    def _get_in_range_info(stat: ValuesInRangeStat) -> str:
        percents = round(stat.share_in_range * 100, 3)
        return f"{stat.number_in_range} ({percents}%)"

    def render_html(self, obj: ColumnValueRangeMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        column_name = metric_result.column_name

        counters = [
            CounterData.string(label="Value range", value=f"[{metric_result.left}, {metric_result.right}]"),
            CounterData.string(label="In range (current)", value=self._get_in_range_info(metric_result.current)),
        ]

        if metric_result.reference is not None:
            counters.append(
                CounterData.string(
                    label="In range (reference)", value=self._get_in_range_info(metric_result.reference)
                ),
            )

        result: List[BaseWidgetInfo] = [
            header_text(
                label=f"Column '{column_name}'. Value range.",
            ),
            counter(counters=counters),
            self._get_tabs(metric_result),
        ]
        return result
