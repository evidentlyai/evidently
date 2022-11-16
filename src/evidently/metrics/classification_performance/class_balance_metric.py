from typing import Dict
from typing import List

import dataclasses

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns
from evidently.utils.visualizations import make_hist_for_cat_plot
from evidently.utils.visualizations import plot_distr_subplots


@dataclasses.dataclass
class ClassificationClassBalanceResult:
    plot_data: Dict[str, int]


class ClassificationClassBalance(Metric[ClassificationClassBalanceResult]):
    def calculate(self, data: InputData) -> ClassificationClassBalanceResult:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        ref_target = None
        if data.reference_data is not None:
            ref_target = data.reference_data[target_name]
        plot_data = make_hist_for_cat_plot(data.current_data[target_name], ref_target)

        return ClassificationClassBalanceResult(plot_data=plot_data)


@default_renderer(wrap_type=ClassificationClassBalance)
class ClassificationClassBalanceRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationClassBalance) -> dict:
        return {}

    def render_html(self, obj: ClassificationClassBalance) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        current_plot_data = metric_result.plot_data["current"]
        reference_plot_data = None
        if "reference" in metric_result.plot_data.keys():
            reference_plot_data = metric_result.plot_data["reference"]

        fig = plot_distr_subplots(
            hist_curr=current_plot_data,
            hist_ref=reference_plot_data,
            xaxis_name="Class",
            yaxis_name="Number Of Objects",
            same_color=True,
            color_options=self.color_options,
        )
        return [
            header_text(label="Class Representation"),
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            ),
        ]
