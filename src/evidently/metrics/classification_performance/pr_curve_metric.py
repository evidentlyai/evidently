from typing import List
from typing import Optional

import dataclasses
import pandas as pd
from sklearn import metrics

from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.utils.visualizations import get_pr_rec_plot_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import header_text


@dataclasses.dataclass
class ClassificationPRCurveResults:
    current_pr_curve: Optional[dict] = None
    reference_pr_curve: Optional[dict] = None


class ClassificationPRCurve(Metric[ClassificationPRCurveResults]):
    def calculate(self, data: InputData) -> ClassificationPRCurveResults:
        curr_predictions = get_prediction_data(data.current_data, data.column_mapping)
        curr_pr_curve = self.calculate_metrics(data.current_data[data.column_mapping.target], curr_predictions)
        ref_pr_curve = None
        if data.reference_data is not None:
            ref_predictions = get_prediction_data(data.reference_data, data.column_mapping)
            ref_pr_curve = self.calculate_metrics(data.reference_data[data.column_mapping.target], ref_predictions)
        return ClassificationPRCurveResults(
            current_pr_curve=curr_pr_curve,
            reference_pr_curve=ref_pr_curve,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData):
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("PR Curve can be calculated only on binary probabilistic predictions")
        binaraized_target = (target_data.values.reshape(-1, 1) == labels).astype(int)
        pr_curve = {}
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]
            pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target, prediction.prediction_probas[labels[0]])
            pr_curve[labels[0]] = {"pr": pr.tolist(), "rcl": rcl.tolist(), "thrs": thrs.tolist()}
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels
            for label in labels:

                pr, rcl, thrs = metrics.precision_recall_curve(
                    binaraized_target[label],
                    prediction.prediction_probas[label],
                )

                pr_curve[label] = {
                    "pr": pr.tolist(),
                    "rcl": rcl.tolist(),
                    "thrs": thrs.tolist(),
                }
        return pr_curve


@default_renderer(wrap_type=ClassificationPRCurve)
class ClassificationPRCurveRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationPRCurve) -> dict:
        return {}

    def render_html(self, obj: ClassificationPRCurve) -> List[BaseWidgetInfo]:
        current_pr_curve = obj.get_result().current_pr_curve
        reference_pr_curve = obj.get_result().reference_pr_curve
        if current_pr_curve is None:
            return []

        tab_data = get_pr_rec_plot_data(current_pr_curve, reference_pr_curve)
        if len(tab_data) == 1:
            return [
                header_text(label="Precision-Recall Curve"),
                tab_data[0][1]
            ]
        tabs = [TabData(name, widget) for name, widget in tab_data]
        return [
            header_text(label="Precision-Recall Curve"),
            widget_tabs(title="", tabs=tabs)
        ]
