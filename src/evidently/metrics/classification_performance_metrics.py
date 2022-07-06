import dataclasses
from typing import Optional, Tuple, List, Dict, Union

import numpy as np
import pandas as pd
from numpy import dtype
import sklearn

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import ConfusionMatrix
from evidently.analyzers.utils import calculate_confusion_by_classes
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric


@dataclasses.dataclass
class DatasetClassificationPerformanceMetrics:
    """Class for performance metrics values"""

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    log_loss: float
    metrics_matrix: dict
    confusion_matrix: ConfusionMatrix
    confusion_by_classes: Dict[str, Dict[str, int]]
    roc_aucs: Optional[list] = None
    roc_curve: Optional[dict] = None
    pr_curve: Optional[dict] = None
    pr_table: Optional[Union[dict, list]] = None


@dataclasses.dataclass
class ClassificationPerformanceMetricsResults:
    reference_metrics: Optional[DatasetClassificationPerformanceMetrics] = None
    current_metrics: Optional[DatasetClassificationPerformanceMetrics] = None
    dummy_metrics: Optional[DatasetClassificationPerformanceMetrics] = None


def classification_performance_metrics(
    target: pd.Series,
    prediction: pd.Series,
    prediction_probas: Optional[pd.DataFrame],
    target_names: Optional[List[str]],
) -> DatasetClassificationPerformanceMetrics:
    # calculate metrics matrix
    labels = target_names if target_names else sorted(set(target) | set(prediction))
    binaraized_target = (target.values.reshape(-1, 1) == labels).astype(int)

    prediction_labels = prediction

    labels = sorted(set(target))

    # calculate quality metrics
    accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
    avg_precision = sklearn.metrics.precision_score(target, prediction_labels, average="macro")
    avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="macro")
    avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="macro")

    if prediction_probas is not None:
        array_prediction = prediction_probas.to_numpy()
        roc_auc = sklearn.metrics.roc_auc_score(binaraized_target, array_prediction, average="macro")
        log_loss = sklearn.metrics.log_loss(binaraized_target, array_prediction)

        roc_aucs = sklearn.metrics.roc_auc_score(binaraized_target, array_prediction, average=None).tolist()

    else:
        roc_aucs = None
        roc_auc = None
        log_loss = None

    # calculate class support and metrics matrix
    metrics_matrix = sklearn.metrics.classification_report(target, prediction_labels, output_dict=True)

    # calculate confusion matrix
    conf_matrix = sklearn.metrics.confusion_matrix(target, prediction_labels)
    confusion_by_classes = calculate_confusion_by_classes(conf_matrix, labels)

    return DatasetClassificationPerformanceMetrics(
        accuracy=accuracy_score,
        precision=avg_precision,
        recall=avg_recall,
        f1=avg_f1,
        roc_auc=roc_auc,
        log_loss=log_loss,
        metrics_matrix=metrics_matrix,
        confusion_matrix=ConfusionMatrix(labels=labels, values=conf_matrix.tolist()),
        roc_aucs=roc_aucs,
        confusion_by_classes=confusion_by_classes,
    )


class ClassificationPerformanceMetrics(Metric[ClassificationPerformanceMetricsResults]):
    def __init__(self):
        pass

    def calculate(self, data: InputData, metrics: dict) -> ClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        results = ClassificationPerformanceMetricsResults()
        current_data = _cleanup_data(data.current_data)
        target_data = current_data[data.column_mapping.target]
        prediction_data, prediction_probas = get_prediction_data(current_data, data.column_mapping)
        results.current_metrics = classification_performance_metrics(
            target_data, prediction_data, prediction_probas, data.column_mapping.target_names
        )

        if data.reference_data is not None:
            reference_data = _cleanup_data(data.reference_data)
            ref_prediction_data, ref_probas = get_prediction_data(reference_data, data.column_mapping)
            results.reference_metrics = classification_performance_metrics(
                reference_data[data.column_mapping.target],
                ref_prediction_data,
                ref_probas,
                data.column_mapping.target_names,
            )

        dummy_preds = pd.Series([target_data.value_counts().idxmax()] * len(target_data))
        results.dummy_metrics = classification_performance_metrics(
            target_data, dummy_preds, None, data.column_mapping.target_names
        )
        return results


def _cleanup_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any")


def get_prediction_data(data: pd.DataFrame, mapping: ColumnMapping) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
    if isinstance(mapping.prediction, list):
        # list of columns with prediction probas, should be same as target labels
        return data[mapping.prediction].idxmax(axis=1), data[mapping.prediction]

    if (
        isinstance(mapping.prediction, str)
        and data[mapping.prediction].dtype == dtype("float64")
        and mapping.target_names is not None
    ):
        predictions = data[mapping.prediction].apply(
            lambda x: mapping.target_names[1] if x > 0.5 else mapping.target_names[0]
        )
        prediction_probas = pd.DataFrame.from_dict(
            {
                mapping.target_names[1]: data[mapping.prediction],
                mapping.target_names[0]: data[mapping.prediction].apply(lambda x: 1.0 - x),
            }
        )
        return predictions, prediction_probas
    return data[mapping.prediction], None
