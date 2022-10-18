from typing import Optional
from typing import Union

import dataclasses
import pandas as pd

from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import calculate_pr_table
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric


@dataclasses.dataclass
class ClassificationPRTableResults:
    current_pr_table: Optional[Union[dict, list]] = None
    reference_pr_table: Optional[Union[dict, list]] = None


class ClassificationPRTable(Metric[ClassificationPRTableResults]):
    def calculate(self, data: InputData) -> ClassificationPRTableResults:
        curr_prediction = get_prediction_data(data.current_data, data.column_mapping)
        curr_pr_table = self.calculate_metrics(data.current_data[data.column_mapping.target], curr_prediction)
        ref_pr_table = None
        if data.reference_data is not None:
            ref_prediction = get_prediction_data(data.reference_data, data.column_mapping)
            ref_pr_table = self.calculate_metrics(data.reference_data[data.column_mapping.target], ref_prediction)
        return ClassificationPRTableResults(
            current_pr_table=curr_pr_table,
            reference_pr_table=ref_pr_table,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData):
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("PR Table can be calculated only on binary probabilistic predictions")
        binaraized_target = (target_data.values.reshape(-1, 1) == labels).astype(int)
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]

            binded = list(zip(binaraized_target["target"].tolist(), prediction.prediction_probas[labels[0]].tolist()))
            pr_table = calculate_pr_table(binded)
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels

            pr_table = []

            for label in labels:
                binded = list(zip(binaraized_target[label].tolist(), prediction.prediction_probas[label]))
                pr_table = calculate_pr_table(binded)
        return pr_table
