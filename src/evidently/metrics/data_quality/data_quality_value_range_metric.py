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
    left: Numeric
    right: Numeric
    current: ValuesInRangeStat
    reference: Optional[ValuesInRangeStat] = None
    # distributions for the column
    current_distribution: Optional[pd.Series] = None
    reference_distribution: Optional[pd.Series] = None

    def __eq__(self, other):
        return (
            self.column_name == other.column_name
            and self.left == other.left
            and self.right == other.right
            and self.current == other.current
            and self.reference == other.reference
        )


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

    def calculate(self, data: InputData) -> DataQualityValueRangeMetricResult:
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
        distribution_for_plot = get_distribution_for_column(
            column_name=self.column_name,
            column_type="num",
            current=current_column,
            reference=reference_column,
        )

        return DataQualityValueRangeMetricResult(
            column_name=self.column_name,
            left=left,
            right=right,
            current=current,
            reference=reference,
            current_distribution=distribution_for_plot["current"],
            reference_distribution=distribution_for_plot.get("reference", None),
        )


@default_renderer(wrap_type=DataQualityValueRangeMetric)
class DataQualityValueRangeMetricRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueRangeMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("current_distribution", None)
        result.pop("reference_distribution", None)
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
        metric_result = obj.get_result()
        column_name = metric_result.column_name
        left = metric_result.left
        right = metric_result.right
        number_in_range = metric_result.current.number_in_range
        percents = round(metric_result.current.share_in_range * 100, 3)

        result: List[BaseWidgetInfo] = [
            header_text(
                title=f"Value range for column '{column_name}'",
                label=f"The number of values in range [{left}, {right}] is {number_in_range} ({percents}%)",
            ),
            widget_tabs(
                title="Current dataset",
                tabs=[
                    TabData(
                        title="Distribution",
                        widget=plotly_figure(
                            title="",
                            figure=plot_distribution_with_range(
                                distribution_data=metric_result.current_distribution,
                                left=metric_result.left,
                                right=metric_result.right,
                            ),
                        ),
                    ),
                    TabData(
                        title="Statistics",
                        widget=self._get_table_stat(metric_result.current),
                    ),
                ],
            ),
        ]
        if metric_result.reference:
            result.append(
                widget_tabs(
                    title="Reference dataset",
                    tabs=[
                        TabData(
                            title="Distribution",
                            widget=plotly_figure(
                                title="",
                                figure=plot_distribution_with_range(
                                    distribution_data=metric_result.reference_distribution,
                                    left=metric_result.left,
                                    right=metric_result.right,
                                ),
                            ),
                        ),
                        TabData(
                            title="Statistics",
                            widget=self._get_table_stat(metric_result.reference),
                        ),
                    ],
                )
            )
        return result
