from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import AnyOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text


class CategoryStat(MetricResult):
    all_num: int
    category_num: int
    category_ratio: float


class ColumnCategoryMetricResult(MetricResult):
    column_name: str
    category: Union[int, float, str]
    current: CategoryStat
    reference: Optional[CategoryStat] = None
    counts_of_values: Optional[Dict[str, pd.DataFrame]]


class ColumnCategoryMetric(Metric[ColumnCategoryMetricResult]):
    """Calculates count and shares of values in the predefined values list"""

    column_name: str
    category: Union[int, float, str]

    def __init__(self, column_name: str, category: Union[int, float, str], options: AnyOptions = None) -> None:
        self.column_name = column_name
        self.category = category
        super().__init__(options=options)

    def calculate(self, data: InputData) -> ColumnCategoryMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column '{self.column_name}' is not in current data.")

        if data.reference_data is not None and self.column_name not in data.reference_data:
            raise ValueError(f"Column '{self.column_name}' is not in reference data.")

        counts_of_values = None
        counts_of_values = {}
        current_counts = data.current_data[self.column_name].value_counts(dropna=False).reset_index()
        current_counts.columns = ["x", "count"]
        counts_of_values["current"] = current_counts.head(10)
        if data.reference_data is not None:
            reference_counts = data.reference_data[self.column_name].value_counts(dropna=False).reset_index()
            reference_counts.columns = ["x", "count"]
            counts_of_values["reference"] = reference_counts.head(10)

        reference: Optional[CategoryStat] = None
        if data.reference_data is not None:
            reference = CategoryStat(
                all_num=data.reference_data.shape[0],
                category_num=(data.reference_data[self.column_name] == self.category).sum(),
                category_ratio=(data.reference_data[self.column_name] == self.category).mean(),
            )
        return ColumnCategoryMetricResult(
            column_name=self.column_name,
            category=self.category,
            current=CategoryStat(
                all_num=data.current_data.shape[0],
                category_num=(data.current_data[self.column_name] == self.category).sum(),
                category_ratio=(data.current_data[self.column_name] == self.category).mean(),
            ),
            reference=reference,
            counts_of_values=counts_of_values,
        )


@default_renderer(wrap_type=ColumnCategoryMetric)
class ColumnCategoryMetricRenderer(MetricRenderer):
    def _get_count_info(self, stat: CategoryStat):
        percents = round(stat.category_ratio * 100, 3)
        return f"{stat.category_num} out of {stat.all_num} ({percents}%)"

    def render_html(self, obj: ColumnCategoryMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [header_text(label=f"Column '{metric_result.column_name}'. Сategory '{metric_result.category}'.")]
        counters = [
            CounterData.string(
                label="current",
                value=self._get_count_info(metric_result.current),
            ),
        ]

        if metric_result.reference is not None:
            counters.append(
                CounterData.string(
                    label="reference",
                    value=self._get_count_info(metric_result.reference),
                ),
            )
        result.append(counter(counters=counters))
        return result
