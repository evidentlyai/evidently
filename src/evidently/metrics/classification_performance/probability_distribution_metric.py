from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
from plotly import figure_factory as ff

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import GraphData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_graph_tabs
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ClassificationProbDistributionResults:
    current_distribution: Optional[Dict[str, list]]
    reference_distribution: Optional[Dict[str, list]]


class ClassificationProbDistribution(Metric[ClassificationProbDistributionResults]):
    @staticmethod
    def get_distribution(dataset: pd.DataFrame, target_name: str, prediction_labels: Iterable) -> Dict[str, list]:
        result = {}
        dataset.replace([np.inf, -np.inf], np.nan, inplace=True)

        for label in prediction_labels:
            result[label] = [
                dataset[dataset[target_name] == label][label],
                dataset[dataset[target_name] != label][label],
            ]

        return result

    def calculate(self, data: InputData) -> ClassificationProbDistributionResults:
        columns = process_columns(data.current_data, data.column_mapping)
        prediction = columns.utility_columns.prediction
        target = columns.utility_columns.target

        if target is None:
            raise ValueError("Target column should be present")

        if not isinstance(prediction, Iterable) or isinstance(prediction, str):
            current_distribution = None
            reference_distribution = None

        else:
            current_data_copy = data.current_data.copy()
            current_distribution = self.get_distribution(current_data_copy, target, prediction)

            if data.reference_data is not None:
                reference_data_copy = data.reference_data.copy()
                reference_distribution = self.get_distribution(reference_data_copy, target, prediction)

            else:
                reference_distribution = None

        return ClassificationProbDistributionResults(
            current_distribution=current_distribution,
            reference_distribution=reference_distribution,
        )


@default_renderer(wrap_type=ClassificationProbDistribution)
class ClassificationProbDistributionRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationProbDistribution) -> dict:
        return {}

    def _plot(self, distribution: Dict[str, list]):
        # plot distributions
        graphs = []

        for label in distribution:
            pred_distr = ff.create_distplot(
                distribution[label],
                [str(label), "other"],
                colors=[self.color_options.primary_color, self.color_options.secondary_color],
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

    def render_html(self, obj: ClassificationProbDistribution) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        reference_distribution = metric_result.reference_distribution
        current_distribution = metric_result.current_distribution
        result = []
        size = WidgetSize.FULL

        if reference_distribution is not None:
            size = WidgetSize.HALF

        if current_distribution is not None:
            result.append(
                plotly_graph_tabs(
                    title="Current: Probability Distribution",
                    size=size,
                    figures=[
                        GraphData(graph["title"], graph["data"], graph["layout"])
                        for graph in self._plot(current_distribution)
                    ],
                )
            )

        if reference_distribution is not None:
            result.append(
                plotly_graph_tabs(
                    title="Reference: Probability Distribution",
                    size=size,
                    figures=[
                        GraphData(graph["title"], graph["data"], graph["layout"])
                        for graph in self._plot(reference_distribution)
                    ],
                )
            )

        return result
