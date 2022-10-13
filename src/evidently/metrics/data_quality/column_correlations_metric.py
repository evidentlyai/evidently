from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently import ColumnMapping
from evidently.calculations.data_quality import ColumnCorrelations
from evidently.calculations.data_quality import calculate_category_column_correlations
from evidently.calculations.data_quality import calculate_numerical_column_correlations
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_column_type


@dataclasses.dataclass
class ColumnCorrelationsMetricResult:
    column_name: str
    current: List[ColumnCorrelations]
    reference: Optional[List[ColumnCorrelations]] = None


class ColumnCorrelationsMetric(Metric[ColumnCorrelationsMetricResult]):
    """Calculates correlations between the selected column and all the other columns.
    In the current and reference (if presented) datasets"""

    column_name: str

    def __init__(self, column_name: str) -> None:
        self.column_name = column_name

    def _calculate_correlation(self, dataset: pd.DataFrame, column_mapping: ColumnMapping) -> List[ColumnCorrelations]:
        columns = process_columns(dataset, column_mapping)
        column_type = recognize_column_type(dataset=dataset, column_name=self.column_name, columns=columns)

        if column_type == "cat":
            return calculate_category_column_correlations(self.column_name, dataset, columns.cat_feature_names)

        elif column_type == "num":
            return calculate_numerical_column_correlations(self.column_name, dataset, columns.num_feature_names)

        else:
            raise ValueError(f"Cannot calculate correlations for '{column_type}' column type.")

    def calculate(self, data: InputData) -> ColumnCorrelationsMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column '{self.column_name}' was not found in current data.")

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column '{self.column_name}' was not found in reference data.")

        current_correlations = self._calculate_correlation(data.current_data, data.column_mapping)

        if data.reference_data is not None:
            reference_correlations: Optional[List[ColumnCorrelations]] = self._calculate_correlation(
                data.reference_data, data.column_mapping
            )

        else:
            reference_correlations = None

        return ColumnCorrelationsMetricResult(
            column_name=self.column_name,
            current=current_correlations,
            reference=reference_correlations,
        )


@default_renderer(wrap_type=ColumnCorrelationsMetric)
class ColumnCorrelationsMetricRenderer(MetricRenderer):
    def render_json(self, obj: ColumnCorrelationsMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        return result

    def render_html(self, obj: ColumnCorrelationsMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label=f"Correlations for column '{metric_result.column_name}'."),
        ]
        return result
