from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from sklearn import metrics

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.calculations.classification_performance import get_prediction_data
from evidently.legacy.core import IncludeTags
from evidently.legacy.metric_results import PRCurve
from evidently.legacy.metric_results import PRCurveData
from evidently.legacy.metric_results import PredictionData
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import TabData
from evidently.legacy.renderers.html_widgets import get_pr_rec_plot_data
from evidently.legacy.renderers.html_widgets import header_text
from evidently.legacy.renderers.html_widgets import widget_tabs
from evidently.legacy.utils.data_operations import process_columns

PR_CURVE_MAX_POINTS = 1000


class ClassificationPRCurveResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ClassificationPRCurveResults"
        pd_include = False

        field_tags = {"current_pr_curve": {IncludeTags.Current}, "reference_pr_curve": {IncludeTags.Reference}}

    current_pr_curve: Optional[PRCurve] = None
    reference_pr_curve: Optional[PRCurve] = None


class ClassificationPRCurve(Metric[ClassificationPRCurveResults]):
    class Config:
        type_alias = "evidently:metric:ClassificationPRCurve"

    def calculate(self, data: InputData) -> ClassificationPRCurveResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' should be present")
        curr_predictions = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        curr_pr_curve = self.calculate_metrics(data.current_data[target_name], curr_predictions)
        ref_pr_curve = None
        if data.reference_data is not None:
            ref_predictions = get_prediction_data(data.reference_data, dataset_columns, data.column_mapping.pos_label)
            ref_pr_curve = self.calculate_metrics(data.reference_data[target_name], ref_predictions)
        return ClassificationPRCurveResults(
            current_pr_curve=curr_pr_curve,
            reference_pr_curve=ref_pr_curve,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData) -> PRCurve:
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("PR Curve can be calculated only on binary probabilistic predictions")
        binaraized_target = (target_data.to_numpy().reshape(-1, 1) == labels).astype(int)
        pr_curve: PRCurve = {}
        idx: np.ndarray
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]
            pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target, prediction.prediction_probas.iloc[:, 0])
            if len(pr) > PR_CURVE_MAX_POINTS:
                idx = np.linspace(0, len(thrs) - 1, PR_CURVE_MAX_POINTS).astype(int)
                pr = pr[idx + 1]
                rcl = rcl[idx + 1]
                thrs = thrs[idx]
            pr_curve[prediction.prediction_probas.columns[0]] = PRCurveData(
                pr=pr.tolist(),
                rcl=rcl.tolist(),
                thrs=thrs.tolist(),
            )
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels
            for label in labels:
                pr, rcl, thrs = metrics.precision_recall_curve(
                    binaraized_target[label],
                    prediction.prediction_probas[label],
                )
                if len(pr) > PR_CURVE_MAX_POINTS:
                    idx = np.linspace(0, len(thrs) - 1, PR_CURVE_MAX_POINTS).astype(int)
                    pr = pr[idx + 1]
                    rcl = rcl[idx + 1]
                    thrs = thrs[idx]

                pr_curve[label] = PRCurveData(
                    pr=pr.tolist(),
                    rcl=rcl.tolist(),
                    thrs=thrs.tolist(),
                )
        return pr_curve


@default_renderer(wrap_type=ClassificationPRCurve)
class ClassificationPRCurveRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationPRCurve) -> List[BaseWidgetInfo]:
        current_pr_curve: Optional[PRCurve] = obj.get_result().current_pr_curve
        reference_pr_curve: Optional[PRCurve] = obj.get_result().reference_pr_curve
        if current_pr_curve is None:
            return []

        tab_data = get_pr_rec_plot_data(current_pr_curve, reference_pr_curve, color_options=self.color_options)
        if len(tab_data) == 1:
            return [header_text(label="Precision-Recall Curve"), tab_data[0][1]]
        tabs = [TabData(name, widget) for name, widget in tab_data]
        return [
            header_text(label="Precision-Recall Curve"),
            widget_tabs(title="", tabs=tabs),
        ]
