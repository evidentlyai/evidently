from typing import List
from typing import Optional
from typing import Union

import dataclasses

from evidently.calculations.classification_performance import ConfusionMatrix
from evidently.calculations.classification_performance import calculate_matrix
from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.base_classification_metric import ThresholdClassificationMetric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.visualizations import plot_conf_mtrx

DEFAULT_THRESHOLD = 0.5


@dataclasses.dataclass
class ClassificationConfusionMatrixResult:
    current_matrix: ConfusionMatrix
    reference_matrix: Optional[ConfusionMatrix]


class ClassificationConfusionMatrix(ThresholdClassificationMetric[ClassificationConfusionMatrixResult]):
    probas_threshold: Optional[float]
    k: Optional[Union[float, int]]

    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[Union[float, int]] = None,
    ):
        super().__init__(probas_threshold=probas_threshold, k=k)

    def calculate(self, data: InputData) -> ClassificationConfusionMatrixResult:
        current_target_data, current_pred = self.get_target_prediction_data(data.current_data, data.column_mapping)

        current_results = calculate_matrix(
            current_target_data,
            current_pred.predictions,
            current_pred.labels,
        )

        reference_results = None
        if data.reference_data is not None:
            ref_target_data, ref_pred = self.get_target_prediction_data(data.reference_data, data.column_mapping)
            reference_results = calculate_matrix(
                ref_target_data,
                ref_pred.predictions,
                ref_pred.labels,
            )

        return ClassificationConfusionMatrixResult(
            current_matrix=current_results,
            reference_matrix=reference_results,
        )


@default_renderer(wrap_type=ClassificationConfusionMatrix)
class ClassificationConfusionMatrixRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationConfusionMatrix) -> dict:
        return {}

    def render_html(self, obj: ClassificationConfusionMatrix) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        fig = plot_conf_mtrx(metric_result.current_matrix, metric_result.reference_matrix)
        fig.for_each_xaxis(lambda axis: axis.update(title_text="Predicted Value"))
        fig.update_layout(yaxis_title="Actual Value")
        return [header_text(label="Confusion Matrix"), plotly_figure(figure=fig, title="")]
