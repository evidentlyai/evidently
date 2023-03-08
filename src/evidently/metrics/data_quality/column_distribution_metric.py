import dataclasses
from typing import List, Optional

from evidently.base_metric import InputData, Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer, default_renderer
from evidently.renderers.html_widgets import WidgetSize, header_text, plotly_figure
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.utils.data_operations import process_columns, recognize_column_type
from evidently.utils.visualizations import Distribution, get_distribution_for_column


@dataclasses.dataclass
class ColumnDistributionMetricResult:
    column_name: str
    current: Distribution
    reference: Optional[Distribution] = None


class ColumnDistributionMetric(Metric[ColumnDistributionMetricResult]):
    """Calculates distribution for the column"""

    column_name: str

    def __init__(
        self,
        column_name: str,
    ) -> None:
        self.column_name = column_name

    def calculate(self, data: InputData) -> ColumnDistributionMetricResult:
        if self.column_name not in data.current_data:
            raise ValueError(
                f"Column '{self.column_name}' was not found in current data."
            )

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(
                    f"Column '{self.column_name}' was not found in reference data."
                )

        columns = process_columns(data.current_data, data.column_mapping)
        column_type = recognize_column_type(
            dataset=data.current_data, column_name=self.column_name, columns=columns
        )
        current_column = data.current_data[self.column_name]
        reference_column = None
        if data.reference_data is not None:
            reference_column = data.reference_data[self.column_name]
        current, reference = get_distribution_for_column(
            column_type=column_type,
            current=current_column,
            reference=reference_column,
        )

        return ColumnDistributionMetricResult(
            column_name=self.column_name,
            current=current,
            reference=reference,
        )


@default_renderer(wrap_type=ColumnDistributionMetric)
class ColumnDistributionMetricRenderer(MetricRenderer):
    def render_json(self, obj: ColumnDistributionMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("current", None)
        result.pop("reference", None)
        return result

    def render_html(self, obj: ColumnDistributionMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        distr_fig = get_distribution_plot_figure(
            current_distribution=metric_result.current,
            reference_distribution=metric_result.reference,
            color_options=self.color_options,
        )

        result = [
            header_text(
                label=f"Distribution for column '{metric_result.column_name}'."
            ),
            plotly_figure(title="", figure=distr_fig, size=WidgetSize.FULL),
        ]
        return result
