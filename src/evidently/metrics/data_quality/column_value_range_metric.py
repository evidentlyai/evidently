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
from evidently.renderers.html_widgets import CounterData, counter
from evidently.renderers.html_widgets import HistogramData
from evidently.renderers.html_widgets import TabData
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
    def _get_table_stat(metrics: ValuesInRangeStat) -> BaseWidgetInfo:
        matched_stat = [
            ("Values in range", metrics.number_in_range),
            ("%", np.round(metrics.share_in_range * 100, 3)),
            ("Values out of range", metrics.number_not_in_range),
            ("%", np.round(metrics.share_not_in_range * 100, 3)),
            ("Values count", metrics.number_of_values),
        ]

        matched_stat_headers = ["Metric", "Value"]
        return table_data(
            title="",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def _get_tabs(
        self,
        dataset_name: str,
        stats: ValuesInRangeStat,
        distribution: Optional[Distribution],
        left: Numeric,
        right: Numeric,
    ) -> BaseWidgetInfo:
        if distribution is not None:
            figure = get_histogram_figure_with_range(
                primary_hist=HistogramData(
                    name=dataset_name.lower(),
                    x=list(distribution.x),
                    y=list(distribution.y),
                ),
                secondary_hist=None,
                color_options=self.color_options,
                left=left,
                right=right,
            )

            tabs: List[TabData] = [
                TabData(
                    title="Distribution",
                    widget=plotly_figure(title="", figure=figure),
                ),
            ]

        else:
            tabs = []

        tabs.append(
            TabData(
                title="Statistics",
                widget=self._get_table_stat(stats),
            )
        )
        return widget_tabs(
            title=f"{dataset_name.capitalize()} dataset",
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
            self._get_tabs(
                "current",
                metric_result.current,
                metric_result.current_distribution,
                metric_result.left,
                metric_result.right,
            ),
        ]

        if metric_result.reference is not None:
            result.append(
                self._get_tabs(
                    "reference",
                    metric_result.reference,
                    metric_result.reference_distribution,
                    metric_result.left,
                    metric_result.right,
                )
            )

        return result
