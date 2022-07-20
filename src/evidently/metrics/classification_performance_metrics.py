import dataclasses
import math
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
import logging

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
    current_metrics: DatasetClassificationPerformanceMetrics
    dummy_metrics: DatasetClassificationPerformanceMetrics
    by_k_metrics: Dict[Union[int, float], DatasetClassificationPerformanceMetrics]
    by_threshold_metrics: Dict[float, DatasetClassificationPerformanceMetrics]
    reference_metrics: Optional[DatasetClassificationPerformanceMetrics] = None


def classification_performance_metrics(
        target: pd.Series,
        prediction: pd.Series,
        prediction_probas: Optional[pd.DataFrame],
        target_names: Optional[List[str]],
) -> DatasetClassificationPerformanceMetrics:

    class_num = target.nunique()
    prediction_labels = prediction
    if class_num > 2:
        accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
        avg_precision = sklearn.metrics.precision_score(target, prediction_labels, average="macro")
        avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="macro")
        avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="macro")
    
    else:
        pos_label = 1
        if target.dtype == dtype("str") and prediction_probas is not None:
            pos_label = prediction_probas.columns[0]
        if target.dtype == dtype("str") and target_names is not None:
            pos_label = target_names[0]
        accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
        avg_precision = sklearn.metrics.precision_score(target, prediction_labels, average="binary", pos_label=pos_label)
        avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="binary", pos_label=pos_label)
        avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="binary", pos_label=pos_label)

    # calculate metrics matrix
    # labels = target_names if target_names else sorted(set(target.unique()) | set(prediction.unique()))
        # binaraized_target = (target.values.reshape(-1, 1) == labels).astype(int)

    # prediction_labels = prediction

    # labels = sorted(set(target))

    if prediction_probas is not None:
        binaraized_target = (target.values.reshape(-1, 1) == list(prediction_probas.columns)).astype(int)
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
    labels = target_names if target_names else sorted(set(target.unique()) | set(prediction.unique()))
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
    k_variants: List[Union[int, float]]
    thresholds: List[float]

    def __init__(self):
        self.k_variants = []
        self.thresholds = []

    def with_k(self, k: Union[int, float]) -> 'ClassificationPerformanceMetrics':
        self.k_variants.append(k)
        return self

    def with_threshold(self, threshold: float) -> 'ClassificationPerformanceMetrics':
        self.thresholds.append(threshold)
        return self

    def calculate(self, data: InputData, metrics: dict) -> ClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        current_data = _cleanup_data(data.current_data, data.column_mapping)
        target_data = current_data[data.column_mapping.target]
        prediction_data, prediction_probas = get_prediction_data(current_data, data.column_mapping)

        target_names = data.column_mapping.target_names
        labels = sorted(target_names if target_names else
                        sorted(set(target_data.unique()) | set(prediction_data.unique())))

        by_k_results = {}
        by_threshold_results = {}

        for k in self.k_variants:
            # calculate metrics matrix
            if prediction_probas is None or len(labels) != 2:
                raise ValueError("Top K parameter can be used only with binary classification with probas")
            if isinstance(k, float):
                threshold = prediction_probas[labels[1]].sort_values(ascending=False)[int(math.ceil(k * prediction_probas.shape[0]))]
            elif isinstance(k, int):
                threshold = prediction_probas[labels[1]].sort_values(ascending=False)[k]
            else:
                raise ValueError(f"Unexpected k type {type(k)}")
            k_prediction_data, k_probas = get_prediction_data(current_data, data.column_mapping, threshold)
            by_k_results[k] = classification_performance_metrics(target_data, k_prediction_data, k_probas, labels)

        for threshold in self.thresholds:
            k_prediction_data, k_probas = get_prediction_data(current_data, data.column_mapping, threshold)
            by_threshold_results[threshold] = classification_performance_metrics(target_data, k_prediction_data, k_probas, labels)

        current_metrics = classification_performance_metrics(
            target_data, prediction_data, prediction_probas, labels
        )

        reference_metrics = None
        if data.reference_data is not None:
            reference_data = _cleanup_data(data.reference_data, data.column_mapping)
            ref_prediction_data, ref_probas = get_prediction_data(reference_data, data.column_mapping)
            reference_metrics = classification_performance_metrics(
                reference_data[data.column_mapping.target],
                ref_prediction_data,
                ref_probas,
                target_names,
            )

        dummy_preds = pd.Series([target_data.value_counts().idxmax()] * len(target_data))
        dummy_metrics = classification_performance_metrics(
            target_data, dummy_preds, None, target_names
        )
        return ClassificationPerformanceMetricsResults(
            current_metrics=current_metrics,
            reference_metrics=reference_metrics,
            dummy_metrics=dummy_metrics,
            by_k_metrics=by_k_results,
            by_threshold_metrics=by_threshold_results,
        )


def _cleanup_data(data: pd.DataFrame, mapping: ColumnMapping) -> pd.DataFrame:
    target = mapping.target
    prediction = mapping.prediction
    subset = []
    if target is not None:
        subset.append(target)
    if prediction is not None and isinstance(mapping.prediction, list):
        subset +=  prediction
    if prediction is not None and isinstance(mapping.prediction, str):
        subset.append(prediction)
    if len(subset) > 0:
        return data.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any", subset=subset)
    return data


def get_prediction_data(
        data: pd.DataFrame,
        mapping: ColumnMapping,
        threshold: float = 0.5) -> Tuple[pd.Series, Optional[pd.DataFrame]]:

    # multiclass + probas
    if (
        isinstance(mapping.prediction, list)
        and len(mapping.prediction) > 2
    ):
        # list of columns with prediction probas, should be same as target labels
        return data[mapping.prediction].idxmax(axis=1), data[mapping.prediction]
 
    # binary + probas
    if (
        isinstance(mapping.prediction, list)
        and len(mapping.prediction) == 2
    ):
        predictions = data[mapping.prediction[0]].apply(
            lambda x: mapping.prediction[0] if x >= threshold else mapping.prediction[1]
        )
        return predictions, data[mapping.prediction]

    # # binary + one column probas
    # if (
    #         isinstance(mapping.prediction, str)
    #         and data[mapping.target].dtype == dtype("str")
    #         and data[mapping.prediction].dtype == dtype("float")
    #         and mapping.target_names is not None
    # ):
    #     predictions = data[mapping.prediction].apply(
    #         lambda x: mapping.target_names[0] if x >= threshold else mapping.target_names[1]
    #     )
    #     prediction_probas = pd.DataFrame.from_dict(
    #         {
    #             mapping.target_names[0]: data[mapping.prediction],
    #             mapping.target_names[1]: data[mapping.prediction].apply(lambda x: 1.0 - x),
    #         }
    #     )
    #     return predictions, prediction_probas

    # binary target and preds are numbers
    if (
            isinstance(mapping.prediction, str)
            and data[mapping.target].dtype == dtype("int")
            and data[mapping.prediction].dtype == dtype("float")
    ):
        predictions = data[mapping.prediction] >= threshold
        prediction_probas = pd.DataFrame.from_dict(
            {
                1: data[mapping.prediction],
                0: data[mapping.prediction].apply(lambda x: 1.0 - x),
            }
        )
        return predictions, prediction_probas
    return data[mapping.prediction], None
