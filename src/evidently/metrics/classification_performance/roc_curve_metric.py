from typing import Optional

import dataclasses
import pandas as pd
from sklearn import metrics

from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric


@dataclasses.dataclass
class ClassificationRocCurveResults:
    current_roc_curve: Optional[dict] = None
    reference_roc_curve: Optional[dict] = None


class ClassificationRocCurve(Metric[ClassificationRocCurveResults]):
    def calculate(self, data: InputData) -> ClassificationRocCurveResults:
        curr_predictions = get_prediction_data(data.current_data, data.column_mapping)
        if curr_predictions.prediction_probas is None:
            raise ValueError("Roc Curve can be calculated only on binary probabilistic predictions")
        curr_roc_curve = self.calculate_metrics(data.current_data[data.column_mapping.target], curr_predictions)
        ref_roc_curve = None
        if data.reference_data is not None:
            ref_predictions = get_prediction_data(data.reference_data, data.column_mapping)
            ref_roc_curve = self.calculate_metrics(data.reference_data[data.column_mapping.target], ref_predictions)
        return ClassificationRocCurveResults(
            current_roc_curve=curr_roc_curve,
            reference_roc_curve=ref_roc_curve,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData):
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("Roc Curve can be calculated only on binary probabilistic predictions")
        binaraized_target = (target_data.values.reshape(-1, 1) == labels).astype(int)
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]

            fpr, tpr, thrs = metrics.roc_curve(binaraized_target, prediction.prediction_probas[labels[0]])
            roc_curve: dict = {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "thrs": thrs.tolist()}
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels

            roc_curve = {}
            for label in labels:
                fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], prediction.prediction_probas[label])
                roc_curve[label] = {
                    "fpr": fpr.tolist(),
                    "tpr": tpr.tolist(),
                    "thrs": thrs.tolist(),
                }
        return roc_curve
