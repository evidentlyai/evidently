from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently.calculations.data_quality import calculate_cramer_v_correlations
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
    column_type: str
    current: Dict[str, Dict[str, float]]
    reference: Optional[Dict[str, Dict[str, float]]] = None


class ColumnCorrelationsMetric(Metric[ColumnCorrelationsMetricResult]):
    """Calculates correlations between the selected column and all the other columns.
    In the current and reference (if presented) datasets"""

    column_name: str

    def __init__(self, column_name: str) -> None:
        self.column_name = column_name

    def _calculate_correlation(self, data: pd.DataFrame):
        pass

    def calculate(self, data: InputData) -> ColumnCorrelationsMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column {self.column_name} is not in current data.")

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column {self.column_name} is not in reference data.")

            column_type_recognize_data = data.reference_data

        else:
            column_type_recognize_data = data.current_data

        columns = process_columns(column_type_recognize_data, data.column_mapping)
        column_type = recognize_column_type(
            dataset=column_type_recognize_data, column_name=self.column_name, columns=columns
        )

        reference_correlations = None

        if column_type == "cat":
            current_correlations = {
                "cramer_v": calculate_cramer_v_correlations(
                    self.column_name, data.current_data, columns.cat_feature_names
                )
            }

            if data.reference_data is not None:
                reference_correlations = {
                    "cramer_v": calculate_cramer_v_correlations(
                        self.column_name, data.reference_data, columns.cat_feature_names
                    )
                }

        elif column_type == "num":
            pass

        else:
            raise ValueError(f"Cannot calculate correlations for '{column_type}' column type.")

        return ColumnCorrelationsMetricResult(
            column_name=self.column_name,
            column_type=column_type,
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
