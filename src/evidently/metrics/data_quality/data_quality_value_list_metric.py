from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data


@dataclass
class DataQualityValueListMetricsResults:
    column_name: str
    number_in_list: int
    number_not_in_list: int
    share_in_list: float
    share_not_in_list: float
    counts_of_value: Dict[str, pd.DataFrame]
    rows_count: int
    values: List[str]


class DataQualityValueListMetrics(Metric[DataQualityValueListMetricsResults]):
    """Calculates count and shares of values in the predefined values list"""

    column_name: str
    values: Optional[list]

    def __init__(self, column_name: str, values: Optional[list] = None) -> None:
        self.values = values
        self.column_name = column_name

    def calculate(self, data: InputData) -> DataQualityValueListMetricsResults:
        if self.values is None:
            if data.reference_data is None:
                raise ValueError("Reference or values list should be present")
            self.values = data.reference_data[self.column_name].unique()

        rows_count = data.current_data.shape[0]
        values_in_list = data.current_data[self.column_name].isin(self.values).sum()
        number_not_in_list = rows_count - values_in_list
        counts_of_value = {}
        current_counts = data.current_data[self.column_name].value_counts(dropna=False).reset_index()
        current_counts.columns = ["x", "count"]
        counts_of_value["current"] = current_counts

        if data.reference_data is not None and self.values is not None:
            reference_counts = data.reference_data[self.column_name].value_counts(dropna=False).reset_index()
            reference_counts.columns = ["x", "count"]
            counts_of_value["reference"] = reference_counts

        return DataQualityValueListMetricsResults(
            column_name=self.column_name,
            number_in_list=values_in_list,
            number_not_in_list=rows_count - values_in_list,
            share_in_list=values_in_list / rows_count,
            share_not_in_list=number_not_in_list / rows_count,
            counts_of_value=counts_of_value,
            rows_count=rows_count,
            values=[str(value) for value in self.values],
        )


@default_renderer(wrap_type=DataQualityValueListMetrics)
class DataQualityValueListMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueListMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("counts_of_value", None)
        return result

    @staticmethod
    def _get_table_stat(dataset_name: str, metrics: DataQualityValueListMetricsResults) -> BaseWidgetInfo:
        matched_stat = [
            ("Values from the list", metrics.number_in_list),
            ("Share from the list", np.round(metrics.share_in_list, 3)),
            ("Values not in the list", metrics.number_not_in_list),
            ("Share not in the list", np.round(metrics.share_not_in_list, 3)),
            ("Rows count", metrics.rows_count),
        ]

        matched_stat_headers = ["Metric", "Value"]
        return table_data(
            title=f"{dataset_name.capitalize()}: Values list statistic",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def render_html(self, obj: DataQualityValueListMetrics) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        values_list_info = ",".join(metric_result.values)
        result = [
            header_text(label=f"Data Value List Metrics for the column: {metric_result.column_name}"),
            header_text(label=f"Values: {values_list_info}"),
            self._get_table_stat(dataset_name="current", metrics=metric_result),
        ]
        return result
