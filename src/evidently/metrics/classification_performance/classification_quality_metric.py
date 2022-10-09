import dataclasses
from typing import Optional
from typing import Union

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from evidently import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.base_classification_metric import ThresholdClassificationMetric
from evidently.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrix


@dataclasses.dataclass
class DatasetClassificationQualityResult:
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float] = None
    log_loss: Optional[float] = None
    roc_aucs: Optional[list] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None


@dataclasses.dataclass
class ClassificationQualityResult:
    current: DatasetClassificationQualityResult
    reference: Optional[DatasetClassificationQualityResult]


class ClassificationQuality(ThresholdClassificationMetric[ClassificationQualityResult]):
    confusion_matrix_metric: ClassificationConfusionMatrix

    def __init__(
        self,
        threshold: Optional[float] = None,
        k: Optional[Union[float, int]] = None,
        average: str = "macro",
    ):
        super().__init__(threshold, k)
        self.average = average
        self.confusion_matrix_metric = ClassificationConfusionMatrix(threshold, k)

    def calculate(self, data: InputData) -> ClassificationQualityResult:
        current = self.calculate_metrics(data.current_data, data.column_mapping)
        reference = None
        if data.reference_data is not None:
            reference = self.calculate_metrics(data.reference_data, data.column_mapping)
        return ClassificationQualityResult(
            current=current,
            reference=reference,
        )

    def calculate_metrics(
        self,
        data: pd.DataFrame,
        column_mapping: ColumnMapping,
    ) -> DatasetClassificationQualityResult:
        target, prediction = self.get_target_prediction_data(data, column_mapping)

        return DatasetClassificationQualityResult(
            accuracy=accuracy_score(target, prediction.predictions),
            precision=precision_score(target, prediction.predictions, average=self.average),
            recall=recall_score(target, prediction.predictions, average=self.average),
            f1=f1_score(target, prediction.predictions, average=self.average),
        )
