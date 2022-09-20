import typing
from typing import List
from typing import Optional

import dataclasses
import numpy as np
from plotly import figure_factory as ff

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.options import ColorOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import GraphData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_graph_tabs
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ProbabilityDistributionResults:
    ref_distplot: Optional[List[dict]]
    curr_distplot: List[dict]


class ProbabilityDistributionMetric(Metric[ProbabilityDistributionResults]):
    def calculate(self, data: InputData) -> ProbabilityDistributionResults:
        columns = process_columns(data.reference_data, data.column_mapping)

        return ProbabilityDistributionResults(
            ref_distplot=_plot(data.reference_data.copy(), columns) if data.reference_data is not None else None,
            curr_distplot=_plot(data.current_data.copy(), columns),
        )


def _plot(dataset_to_plot, columns: DatasetColumns, color_options: Optional[ColorOptions] = None):
    utility_columns = columns.utility_columns
    color_options = color_options if color_options is not None else ColorOptions()

    dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)

    # plot distributions
    graphs = []
    if not isinstance(utility_columns.prediction, typing.Iterable) or isinstance(utility_columns.prediction, str):
        return None

    for label in utility_columns.prediction:
        pred_distr = ff.create_distplot(
            [
                dataset_to_plot[dataset_to_plot[utility_columns.target] == label][label],
                dataset_to_plot[dataset_to_plot[utility_columns.target] != label][label],
            ],
            [str(label), "other"],
            colors=[color_options.primary_color, color_options.secondary_color],
            bin_size=0.05,
            show_curve=False,
            show_rug=True,
        )

        pred_distr.update_layout(
            xaxis_title="Probability",
            yaxis_title="Share",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        pred_distr_json = pred_distr.to_plotly_json()
        graphs.append(
            {
                "title": str(label),
                "data": pred_distr_json["data"],
                "layout": pred_distr_json["layout"],
            }
        )
    return graphs


@default_renderer(wrap_type=ProbabilityDistributionMetric)
class CatTargetDriftRenderer(MetricRenderer):
    def render_json(self, obj: ProbabilityDistributionMetric) -> dict:
        return {}

    def render_html(self, obj: ProbabilityDistributionMetric) -> List[MetricHtmlInfo]:
        ref = obj.get_result().ref_distplot
        curr = obj.get_result().curr_distplot
        result = []
        size = WidgetSize.FULL
        if ref is not None:
            size = WidgetSize.HALF
            result.append(
                MetricHtmlInfo(
                    name="",
                    info=plotly_graph_tabs(
                        title="Reference: Probability Distribution",
                        size=size,
                        figures=[GraphData(graph["title"], graph["data"], graph["layout"]) for graph in ref],
                    ),
                )
            )
        if curr is not None:
            result.append(
                MetricHtmlInfo(
                    name="",
                    info=plotly_graph_tabs(
                        title="Current: Probability Distribution",
                        size=size,
                        figures=[GraphData(graph["title"], graph["data"], graph["layout"]) for graph in curr],
                    ),
                )
            )
        return result
