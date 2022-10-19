from typing import Optional
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from sklearn import metrics

from evidently import ColumnMapping
from evidently.calculations.classification_performance import ConfusionMatrix
from evidently.calculations.classification_performance import calculate_confusion_by_classes
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
    tpr: Optional[float] = None
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
        current = self.calculate_metrics(
            data.current_data,
            data.column_mapping,
            self.confusion_matrix_metric.get_result().current_matrix,
        )
        reference = None
        if data.reference_data is not None:
            ref_matrix = self.confusion_matrix_metric.get_result().reference_matrix
            if ref_matrix is None:
                raise ValueError(f"Dependency {self.confusion_matrix_metric.__class__} should have reference data")
            reference = self.calculate_metrics(
                data.reference_data,
                data.column_mapping,
                ref_matrix,
            )
        return ClassificationQualityResult(
            current=current,
            reference=reference,
        )

    def calculate_metrics(
        self,
        data: pd.DataFrame,
        column_mapping: ColumnMapping,
        confusion_matrix: ConfusionMatrix,
    ) -> DatasetClassificationQualityResult:
        target, prediction = self.get_target_prediction_data(data, column_mapping)

        tpr = None
        tnr = None
        fpr = None
        fnr = None
        roc_auc = None
        log_loss = None
        if len(prediction.labels) == 2:
            confusion_by_classes = calculate_confusion_by_classes(
                np.array(confusion_matrix.values),
                confusion_matrix.labels,
            )
            conf_by_pos_label = confusion_by_classes[confusion_matrix.labels[0]]
            tpr = conf_by_pos_label["tp"] / (conf_by_pos_label["tp"] + conf_by_pos_label["fn"])
            tnr = conf_by_pos_label["tn"] / (conf_by_pos_label["tn"] + conf_by_pos_label["fp"])
            fpr = conf_by_pos_label["fp"] / (conf_by_pos_label["fp"] + conf_by_pos_label["tn"])
            fnr = conf_by_pos_label["fn"] / (conf_by_pos_label["fn"] + conf_by_pos_label["tp"])
            if prediction.prediction_probas is not None:
                binaraized_target = (
                    target.astype(str).values.reshape(-1, 1) == list(prediction.prediction_probas.columns.astype(str))
                ).astype(int)
                prediction_probas_array = prediction.prediction_probas.to_numpy()
                roc_auc = metrics.roc_auc_score(binaraized_target, prediction_probas_array, average=self.average)
                log_loss = metrics.log_loss(binaraized_target, prediction_probas_array)

        return DatasetClassificationQualityResult(
            accuracy=metrics.accuracy_score(target, prediction.predictions),
            precision=metrics.precision_score(target, prediction.predictions, average=self.average),
            recall=metrics.recall_score(target, prediction.predictions, average=self.average),
            f1=metrics.f1_score(target, prediction.predictions, average=self.average),
            tpr=tpr,
            tnr=tnr,
            fpr=fpr,
            fnr=fnr,
            roc_auc=roc_auc,
            log_loss=log_loss,
        )
