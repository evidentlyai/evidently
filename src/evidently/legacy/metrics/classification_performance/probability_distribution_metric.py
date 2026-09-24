from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from plotly import figure_factory as ff

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.calculations.classification_performance import get_prediction_data
from evidently.legacy.core import IncludeTags
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.pipeline.column_mapping import TargetNames
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import GraphData
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import plotly_graph_tabs
from evidently.legacy.utils.data_operations import process_columns


class ClassificationProbDistributionResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ClassificationProbDistributionResults"
        dict_include = False
        pd_include = False
        tags = {IncludeTags.Render}

        field_tags = {"current_distribution": {IncludeTags.Current}, "reference_distribution": {IncludeTags.Reference}}

    current_distribution: Optional[Dict[str, list]]  # todo use DistributionField?
    reference_distribution: Optional[Dict[str, list]]
    target_names: Optional[TargetNames] = None


class ClassificationProbDistribution(Metric[ClassificationProbDistributionResults]):
    class Config:
        type_alias = "evidently:metric:ClassificationProbDistribution"

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

        if prediction is None:
            raise ValueError("Prediction column should be present")

        curr_predictions = get_prediction_data(data.current_data, columns, data.column_mapping.pos_label)
        if curr_predictions.prediction_probas is None:
            current_distribution = None
            reference_distribution = None

        else:
            current_data_copy = data.current_data.copy()
            for col in curr_predictions.prediction_probas.columns:
                current_data_copy[col] = curr_predictions.prediction_probas[col]

            current_distribution = self.get_distribution(
                current_data_copy, target, curr_predictions.prediction_probas.columns
            )

            if data.reference_data is not None:
                ref_predictions = get_prediction_data(data.reference_data, columns, data.column_mapping.pos_label)
                if ref_predictions.prediction_probas is None:
                    reference_distribution = None
                else:
                    reference_data_copy = data.reference_data.copy()
                    for col in ref_predictions.prediction_probas.columns:
                        reference_data_copy[col] = ref_predictions.prediction_probas[col]
                    reference_distribution = self.get_distribution(
                        reference_data_copy, target, ref_predictions.prediction_probas.columns
                    )

            else:
                reference_distribution = None

        return ClassificationProbDistributionResults(
            current_distribution=current_distribution,
            reference_distribution=reference_distribution,
            target_names=columns.target_names,
        )


@default_renderer(wrap_type=ClassificationProbDistribution)
class ClassificationProbDistributionRenderer(MetricRenderer):
    @staticmethod
    def _resolve_target_name(label, target_names: Optional[TargetNames]) -> str:
        if target_names is not None and isinstance(target_names, dict):
            resolved = target_names.get(label) or target_names.get(int(label)) if isinstance(label, str) else target_names.get(label)  # type: ignore[arg-type]
            if resolved is not None:
                return str(resolved)
        return str(label)

    def _plot(self, distribution: Dict[str, list], target_names: Optional[TargetNames] = None):
        # plot distributions
        graphs = []

        for label in distribution:
            display_name = self._resolve_target_name(label, target_names)
            pred_distr = ff.create_distplot(
                distribution[label],
                [display_name, "other"],
                colors=[
                    self.color_options.primary_color,
                    self.color_options.secondary_color,
                ],
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
                    "title": display_name,
                    "data": pred_distr_json["data"],
                    "layout": pred_distr_json["layout"],
                }
            )
        return graphs

    def render_html(self, obj: ClassificationProbDistribution) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        reference_distribution = metric_result.reference_distribution
        current_distribution = metric_result.current_distribution
        target_names = metric_result.target_names
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
                        for graph in self._plot(current_distribution, target_names)
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
                        for graph in self._plot(reference_distribution, target_names)
                    ],
                )
            )

        return result
