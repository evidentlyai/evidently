import dataclasses
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
from sklearn.metrics import confusion_matrix

from evidently.calculations.classification_performance import ConfusionMatrix
from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.base_classification_metric import ThresholdClassificationMetric

DEFAULT_THRESHOLD = 0.5


@dataclasses.dataclass
class ClassificationConfusionMatrixResult:
    current_matrix: ConfusionMatrix
    reference_matrix: Optional[ConfusionMatrix]


class ClassificationConfusionMatrix(ThresholdClassificationMetric[ClassificationConfusionMatrixResult]):
    def calculate(self, data: InputData) -> ClassificationConfusionMatrixResult:
        current_target_data, current_pred = self.get_target_prediction_data(data.current_data, data.column_mapping)

        current_results = self._calculate_matrix(
            current_target_data,
            current_pred.predictions,
            current_pred.labels,
        )

        reference_results = None
        if data.reference_data is not None:
            ref_target_data, ref_pred = self.get_target_prediction_data(data.reference_data, data.column_mapping)
            reference_results = self._calculate_matrix(
                ref_target_data,
                ref_pred.predictions,
                ref_pred.labels,
            )

        return ClassificationConfusionMatrixResult(
            current_matrix=current_results,
            reference_matrix=reference_results,
        )

    @staticmethod
    def _calculate_matrix(
        target: pd.Series,
        prediction: pd.Series,
        labels: List[Union[str, int]],
    ) -> ConfusionMatrix:
        matrix = confusion_matrix(target, prediction, labels=labels)
        return ConfusionMatrix(labels, [row.tolist() for row in matrix])
