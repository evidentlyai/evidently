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
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.types import Numeric
from evidently.utils.visualizations import get_distribution_for_column
from evidently.utils.visualizations import plot_distribution_with_range


@dataclasses.dataclass
class ValuesInRangeStat:
    number_in_range: int
    number_not_in_range: int
    share_in_range: float
    share_not_in_range: float
    # number of rows without null-like values
    number_of_values: int


@dataclasses.dataclass
class DataQualityValueRangeMetricResult:
    column_name: str
    range_left_value: Numeric
    range_right_value: Numeric
    current: ValuesInRangeStat
    reference: Optional[ValuesInRangeStat] = None
    # distributions for the column
    current_distribution: Optional[pd.Series] = None
    reference_distribution: Optional[pd.Series] = None


class DataQualityValueRangeMetric(Metric[DataQualityValueRangeMetricResult]):
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
        number_in_range = column.between(left=float(left), right=float(right), inclusive="both").sum()
        number_not_in_range = rows_count - number_in_range
        return ValuesInRangeStat(
            number_in_range=number_in_range,
            number_not_in_range=number_not_in_range,
            share_in_range=number_in_range / rows_count,
            share_not_in_range=number_not_in_range / rows_count,
            number_of_values=rows_count,
        )

    def calculate(self, data: InputData) -> DataQualityValueRangeMetricResult:
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

        if left is None or right is None:
            raise ValueError("Cannot define one or both of range parameters")

        current = self._calculate_in_range_stats(data.current_data[self.column_name], left, right)

        if data.reference_data is None:
            reference_column = None
            reference = None

        else:
            reference_column = data.reference_data[self.column_name]
            reference = self._calculate_in_range_stats(data.reference_data[self.column_name], left, right)

        # calculate distribution for visualisation
        current_column = data.current_data[self.column_name]
        distribution_for_plot = get_distribution_for_column(
            column_name=self.column_name,
            column_type="num",
            current=current_column,
            reference=reference_column,
        )

        return DataQualityValueRangeMetricResult(
            column_name=self.column_name,
            range_left_value=left,
            range_right_value=right,
            current=current,
            reference=reference,
            current_distribution=distribution_for_plot["current"],
            reference_distribution=distribution_for_plot.get("reference", None),
        )


@default_renderer(wrap_type=DataQualityValueRangeMetric)
class DataQualityValueRangeMetricRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueRangeMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("distr_for_plot", None)
        return result

    @staticmethod
    def _get_table_stat(metrics: ValuesInRangeStat) -> BaseWidgetInfo:
        matched_stat = [
            ("Values in the range", metrics.number_in_range),
            ("Share in the range", np.round(metrics.share_in_range, 3)),
            ("Values not in the range", metrics.number_not_in_range),
            ("Share not in the range", np.round(metrics.share_not_in_range, 3)),
            ("Values count", metrics.number_of_values),
        ]

        matched_stat_headers = ["Metric", "Value"]
        return table_data(
            title="",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def render_html(self, obj: DataQualityValueRangeMetric) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        column_name = result.column_name
        left = result.range_left_value
        right = result.range_right_value
        number_in_range = result.current.number_in_range
        distribution = plot_distribution_with_range(
            current=result.current_distribution,
            reference=result.reference_distribution,
            left=result.range_left_value,
            right=result.range_right_value,
        )
        percents = round(result.current.share_in_range * 100, 3)
        details_tabs = [
            TabData(
                title="Distribution",
                widget=plotly_figure(
                    title="",
                    figure=distribution,
                ),
            ),
            TabData(
                title="Current Statistics Table",
                widget=self._get_table_stat(result.current),
            ),
        ]

        if result.reference is not None:
            details_tabs.append(
                TabData(
                    title="Reference Statistics Table",
                    widget=self._get_table_stat(result.reference),
                ),
            )

        return [
            header_text(
                title=f"Value range for column '{column_name}'",
                label=f"The number of values in range [{left}, {right}] is {number_in_range} ({percents}%)",
            ),
            widget_tabs(tabs=details_tabs),
        ]
