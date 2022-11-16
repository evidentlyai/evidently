from typing import Dict
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
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import get_histogram_for_distribution
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_column_type


@dataclasses.dataclass
class ColumnCorrelationsMetricResult:
    column_name: str
    current: Dict[str, ColumnCorrelations]
    reference: Optional[Dict[str, ColumnCorrelations]] = None


class ColumnCorrelationsMetric(Metric[ColumnCorrelationsMetricResult]):
    """Calculates correlations between the selected column and all the other columns.
    In the current and reference (if presented) datasets"""

    column_name: str

    def __init__(self, column_name: str) -> None:
        self.column_name = column_name

    @staticmethod
    def _calculate_correlation(
        column_name: str, dataset: pd.DataFrame, column_mapping: ColumnMapping
    ) -> Dict[str, ColumnCorrelations]:
        columns = process_columns(dataset, column_mapping)
        column_type = recognize_column_type(dataset=dataset, column_name=column_name, columns=columns)

        if column_type == "cat":
            correlation_columns = [name for name in columns.cat_feature_names if name != column_name]
            return calculate_category_column_correlations(column_name, dataset, correlation_columns)

        elif column_type == "num":
            correlation_columns = [name for name in columns.num_feature_names if name != column_name]
            return calculate_numerical_column_correlations(column_name, dataset, correlation_columns)

        else:
            raise ValueError(f"Cannot calculate correlations for '{column_type}' column type.")

    def calculate(self, data: InputData) -> ColumnCorrelationsMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(f"Column '{self.column_name}' was not found in current data.")

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column '{self.column_name}' was not found in reference data.")

        current_correlations = self._calculate_correlation(self.column_name, data.current_data, data.column_mapping)

        if data.reference_data is not None:
            reference_correlations: Optional[Dict[str, ColumnCorrelations]] = self._calculate_correlation(
                self.column_name, data.reference_data, data.column_mapping
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

    def _get_plots_correlations(self, metric_result: ColumnCorrelationsMetricResult) -> Optional[BaseWidgetInfo]:
        tabs = []

        for correlation_name, current_correlation in metric_result.current.items():
            reference_correlation_values = None

            if metric_result.reference and correlation_name in metric_result.reference:
                reference_correlation_values = metric_result.reference[correlation_name].values

            if current_correlation.values or reference_correlation_values:
                tabs.append(
                    TabData(
                        title=correlation_name,
                        widget=get_histogram_for_distribution(
                            title="",
                            current_distribution=current_correlation.values,
                            reference_distribution=reference_correlation_values,
                            xaxis_title="Columns",
                            yaxis_title="Correlation",
                            color_options=self.color_options,
                        ),
                    )
                )

        if tabs:
            return widget_tabs(tabs=tabs)

        else:
            return None

    def render_html(self, obj: ColumnCorrelationsMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        correlation_plots = self._get_plots_correlations(metric_result)

        if correlation_plots:
            return [header_text(label=f"Correlations for column '{metric_result.column_name}'."), correlation_plots]

        else:
            # no correlations, draw nothing
            return []
