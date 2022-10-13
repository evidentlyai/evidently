from typing import Any
from typing import Dict
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
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs_for_more_than_one


@dataclasses.dataclass
class ValueListStat:
    number_in_list: int
    number_not_in_list: int
    share_in_list: float
    share_not_in_list: float
    values_count: Dict[Any, int]
    rows_count: int


@dataclasses.dataclass
class DataQualityValueListMetricsResult:
    column_name: str
    values: List[Any]
    current: ValueListStat
    reference: Optional[ValueListStat] = None


class DataQualityValueListMetric(Metric[DataQualityValueListMetricsResult]):
    """Calculates count and shares of values in the predefined values list"""

    column_name: str
    values: Optional[list]

    def __init__(self, column_name: str, values: Optional[list] = None) -> None:
        self.values = values
        self.column_name = column_name

    @staticmethod
    def _calculate_stats(values: list, column: pd.Series) -> ValueListStat:
        rows_count = get_rows_count(column)

        if rows_count == 0:
            values_in_list = 0
            number_not_in_list = 0
            share_in_list = 0.0
            share_not_in_list = 0.0
            current_counts = {}

        else:
            values_in_list = column.isin(values).sum()
            share_in_list = values_in_list / rows_count
            number_not_in_list = rows_count - values_in_list
            share_not_in_list = number_not_in_list / rows_count
            current_counts = dict(column.value_counts(dropna=True))

        return ValueListStat(
            number_in_list=values_in_list,
            number_not_in_list=number_not_in_list,
            share_in_list=share_in_list,
            share_not_in_list=share_not_in_list,
            values_count=current_counts,
            rows_count=rows_count,
        )

    def calculate(self, data: InputData) -> DataQualityValueListMetricsResult:
        if self.values is None:
            if data.reference_data is None:
                raise ValueError("Reference or values list should be present")
            values = data.reference_data[self.column_name].unique()

        else:
            values = self.values

        current_stats = self._calculate_stats(values, data.current_data[self.column_name])

        if data.reference_data is not None:
            reference_stats: Optional[ValueListStat] = self._calculate_stats(
                values, data.reference_data[self.column_name]
            )

        else:
            reference_stats = None

        return DataQualityValueListMetricsResult(
            column_name=self.column_name,
            values=list(values),
            current=current_stats,
            reference=reference_stats,
        )


@default_renderer(wrap_type=DataQualityValueListMetric)
class DataQualityValueListMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueListMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("counts_of_value", None)
        return result

    @staticmethod
    def _get_table_stat(dataset_name: str, stats: ValueListStat) -> BaseWidgetInfo:
        matched_stat = [
            ("Values from the list", stats.number_in_list),
            ("Share from the list", np.round(stats.share_in_list, 3)),
            ("Values not in the list", stats.number_not_in_list),
            ("Share not in the list", np.round(stats.share_not_in_list, 3)),
            ("Rows count", stats.rows_count),
        ]

        matched_stat_headers = ["Metric", "Value"]
        return table_data(
            title=f"{dataset_name.capitalize()}: Values list statistic",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def render_html(self, obj: DataQualityValueListMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        values_list_info = ",".join(map(str, metric_result.values))
        result = [
            header_text(label=f"Data Value List Metrics for the column '{metric_result.column_name}'"),
            header_text(label=f"Values: {values_list_info}"),
        ]

        tabs = [
            TabData(title="Current", widget=self._get_table_stat(dataset_name="current", stats=metric_result.current))
        ]

        if metric_result.reference:
            tabs.append(
                TabData(
                    title="Reference",
                    widget=self._get_table_stat(dataset_name="reference", stats=metric_result.reference),
                )
            )

        result.append(widget_tabs_for_more_than_one(tabs=tabs))
        return result
