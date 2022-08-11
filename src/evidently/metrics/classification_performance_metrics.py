import dataclasses
from typing import Optional
from typing import List
from typing import Dict
from typing import Union

import numpy as np
import pandas as pd
import sklearn
from numpy import dtype
from pandas.core.dtypes.api import is_float_dtype
from pandas.core.dtypes.api import is_string_dtype
from pandas.core.dtypes.api import is_object_dtype

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
    metrics_matrix: dict
    confusion_matrix: ConfusionMatrix
    confusion_by_classes: Dict[str, Dict[str, int]]
    roc_auc: Optional[float] = None
    log_loss: Optional[float] = None
    roc_aucs: Optional[list] = None
    roc_curve: Optional[dict] = None
    pr_curve: Optional[dict] = None
    pr_table: Optional[Union[dict, list]] = None
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    rate_plots_data: Optional[dict] = None


@dataclasses.dataclass
class DataForPlots:
    """Class for Boxplots"""

    current: Optional[Dict[str, Dict[str, list]]] = None
    reference: Optional[Dict[str, Dict[str, list]]] = None


@dataclasses.dataclass
class ClassificationPerformanceMetricsResults:
    current_metrics: DatasetClassificationPerformanceMetrics
    current_by_k_metrics: Dict[Union[int, float], DatasetClassificationPerformanceMetrics]
    current_by_threshold_metrics: Dict[Union[int, float], DatasetClassificationPerformanceMetrics]
    dummy_metrics: DatasetClassificationPerformanceMetrics
    dummy_by_k_metrics: Dict[Union[int, float], DatasetClassificationPerformanceMetrics]
    dummy_by_threshold_metrics: Dict[Union[int, float], DatasetClassificationPerformanceMetrics]
    reference_metrics: Optional[DatasetClassificationPerformanceMetrics] = None
    reference_by_k_metrics: Optional[Dict[Union[int, float], DatasetClassificationPerformanceMetrics]] = None
    reference_by_threshold_metrics: Optional[Dict[Union[int, float], DatasetClassificationPerformanceMetrics]] = None
    data_for_plots: Optional[DataForPlots] = None


def k_probability_threshold(prediction_probas: pd.DataFrame, k: Union[int, float]) -> float:
    probas = prediction_probas.iloc[:, 0].sort_values(ascending=False)
    if isinstance(k, float):
        if k < 0.0 or k > 1.0:
            raise ValueError(f"K should be in range [0.0, 1.0] but was {k}")
        return probas.iloc[max(int(np.ceil(k * prediction_probas.shape[0])) - 1, 0)]
    if isinstance(k, int):
        return probas.iloc[min(k, prediction_probas.shape[0] - 1)]
    raise ValueError(f"K has unexpected type {type(k)}")


def threshold_probability_labels(
    prediction_probas: pd.DataFrame, pos_label: Union[str, int], neg_label: Union[str, int], threshold: float
) -> pd.Series:
    """Get prediction values by probabilities with the threshold apply"""
    return prediction_probas[pos_label].apply(lambda x: pos_label if x >= threshold else neg_label)


def _calculate_k_variants(
    target_data: pd.Series, prediction_probas: pd.DataFrame, labels: List[str], k_variants: List[Union[int, float]]
):
    by_k_results = {}
    for k in k_variants:
        # calculate metrics matrix
        if prediction_probas is None or len(labels) > 2:
            raise ValueError("Top K parameter can be used only with binary classification with probas")

        pos_label, neg_label = prediction_probas.columns
        prediction_labels = threshold_probability_labels(
            prediction_probas, pos_label, neg_label, k_probability_threshold(prediction_probas, k)
        )
        by_k_results[k] = classification_performance_metrics(
            target_data, prediction_labels, prediction_probas, pos_label
        )
    return by_k_results


def _calculate_thresholds(target_data: pd.Series, prediction_probas: pd.DataFrame, thresholds: List[float]):
    by_threshold_results = {}

    for threshold in thresholds:
        pos_label, neg_label = prediction_probas.columns
        prediction_labels = threshold_probability_labels(prediction_probas, pos_label, neg_label, threshold)
        by_threshold_results[threshold] = classification_performance_metrics(
            target_data, prediction_labels, prediction_probas, pos_label
        )
    return by_threshold_results


def classification_performance_metrics(
    target: pd.Series,
    prediction: pd.Series,
    prediction_probas: Optional[pd.DataFrame],
    pos_label: Optional[Union[str, int]],
) -> DatasetClassificationPerformanceMetrics:

    class_num = target.nunique()
    prediction_labels = prediction

    if class_num > 2:
        accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
        avg_precision = sklearn.metrics.precision_score(target, prediction_labels, average="macro")
        avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="macro")
        avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="macro")

    else:
        accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
        avg_precision = sklearn.metrics.precision_score(
            target, prediction_labels, average="binary", pos_label=pos_label
        )
        avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="binary", pos_label=pos_label)
        avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="binary", pos_label=pos_label)

    roc_auc: Optional[float] = None
    roc_aucs: Optional[list] = None
    log_loss: Optional[float] = None
    roc_curve: Optional[dict] = None

    if prediction_probas is not None:
        binaraized_target = (
            target.astype(str).values.reshape(-1, 1) == list(prediction_probas.columns.astype(str))
        ).astype(int)
        array_prediction = prediction_probas.to_numpy()
        roc_auc = sklearn.metrics.roc_auc_score(binaraized_target, array_prediction, average="macro")
        log_loss = sklearn.metrics.log_loss(binaraized_target, array_prediction)
        roc_aucs = sklearn.metrics.roc_auc_score(binaraized_target, array_prediction, average=None).tolist()  # noqa
        # roc curve
        roc_curve = {}
        binaraized_target = pd.DataFrame(binaraized_target)
        binaraized_target.columns = list(prediction_probas.columns)
        for label in binaraized_target.columns:
            fprs, tprs, thrs = sklearn.metrics.roc_curve(binaraized_target[label], prediction_probas[label])
            roc_curve[label] = {"fpr": fprs.tolist(), "tpr": tprs.tolist(), "thrs": thrs.tolist()}

    # calculate class support and metrics matrix
    metrics_matrix = sklearn.metrics.classification_report(target, prediction_labels, output_dict=True)

    # calculate confusion matrix
    # labels = target_names if target_names else sorted(set(target.unique()) | set(prediction.unique()))
    labels = sorted(set(target.unique()))
    conf_matrix = sklearn.metrics.confusion_matrix(target, prediction_labels)
    confusion_by_classes = calculate_confusion_by_classes(conf_matrix, labels)
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    rate_plots_data: Optional[dict] = None

    # calculate rates metrics and plot data
    if class_num == 2 and pos_label is not None:
        conf_by_pos_label = confusion_by_classes[str(pos_label)]
        tpr = conf_by_pos_label['tp'] / (conf_by_pos_label['tp'] + conf_by_pos_label['fn'])
        tnr = conf_by_pos_label['tn'] / (conf_by_pos_label['tn'] + conf_by_pos_label['fp'])
        fpr = conf_by_pos_label['fp'] / (conf_by_pos_label['fp'] + conf_by_pos_label['tn'])
        fnr = conf_by_pos_label['fn'] / (conf_by_pos_label['fn'] + conf_by_pos_label['tp'])

    if class_num == 2 and prediction_probas is not None and roc_curve is not None:
        rate_plots_data = {}
        rate_plots_data["thrs"] = roc_curve[pos_label]["thrs"]
        rate_plots_data["tpr"] = roc_curve[pos_label]["tpr"]
        rate_plots_data["fpr"] = roc_curve[pos_label]["fpr"]

        df = pd.DataFrame({'true': binaraized_target[pos_label].values, 'preds': prediction_probas[pos_label].values})
        tnrs = []
        fnrs = []
        for tr in rate_plots_data["thrs"]:
            if tr < 1:
                tn = df[(df.true == 0) & (df.preds < tr)].shape[0]
                fn = df[(df.true == 1) & (df.preds < tr)].shape[0]
                tp = df[(df.true == 1) & (df.preds >= tr)].shape[0]
                fp = df[(df.true == 0) & (df.preds >= tr)].shape[0]
                tnrs.append(tn / (tn + fp))
                fnrs.append(fn / (fn + tp))
            else:
                fnrs.append(1)
                tnrs.append(1)
        rate_plots_data["fnr"] = fnrs
        rate_plots_data["tnr"] = tnrs

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
        roc_curve=roc_curve,
        confusion_by_classes=confusion_by_classes,
        tpr=tpr,
        tnr=tnr,
        fpr=fpr,
        fnr=fnr,
        rate_plots_data=rate_plots_data
    )


class ClassificationPerformanceMetrics(Metric[ClassificationPerformanceMetricsResults]):
    k_variants: List[Union[int, float]]
    thresholds: List[float]

    def __init__(self):
        self.k_variants = []
        self.thresholds = []

    def with_k(self, k: Union[int, float]) -> "ClassificationPerformanceMetrics":
        self.k_variants.append(k)
        return self

    def with_threshold(self, threshold: float) -> "ClassificationPerformanceMetrics":
        self.thresholds.append(threshold)
        return self

    def calculate(self, data: InputData, metrics: dict) -> ClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        current_data = _cleanup_data(data.current_data, data.column_mapping)
        target_data = current_data[data.column_mapping.target]
        predictions = get_prediction_data(current_data, data.column_mapping)
        prediction_data = predictions.predictions
        prediction_probas = predictions.prediction_probas

        labels = sorted(set(target_data.unique()))
        current_metrics = classification_performance_metrics(
            target_data, prediction_data, prediction_probas, data.column_mapping.pos_label
        )

        current_by_k_metrics = _calculate_k_variants(target_data, prediction_probas, labels, self.k_variants)

        current_by_thresholds_metrics = _calculate_thresholds(target_data, prediction_probas, self.thresholds)

        reference_metrics = None
        reference_by_k = None
        reference_by_threshold = None
        ref_probas = None

        if data.reference_data is not None:
            reference_data = _cleanup_data(data.reference_data, data.column_mapping)
            ref_predictions = get_prediction_data(reference_data, data.column_mapping)
            ref_prediction_data = ref_predictions.predictions
            ref_probas = ref_predictions.prediction_probas
            ref_target = reference_data[data.column_mapping.target]
            reference_metrics = classification_performance_metrics(
                ref_target,
                ref_prediction_data,
                ref_probas,
                data.column_mapping.pos_label,
            )
            reference_by_k = _calculate_k_variants(ref_target, ref_probas, labels, self.k_variants)
            reference_by_threshold = _calculate_thresholds(ref_target, ref_probas, self.thresholds)

        # dummy
        labels_ratio = target_data.value_counts(normalize=True)
        np.random.seed(0)
        dummy_preds = np.random.choice(labels_ratio.index, len(target_data), p=labels_ratio)
        dummy_metrics = classification_performance_metrics(
            target_data, dummy_preds, None, data.column_mapping.pos_label
        )

        # dummy log_loss
        if prediction_probas is not None:
            binaraized_target = (
                target_data.astype(str).values.reshape(-1, 1) == list(prediction_probas.columns.astype(str))
            ).astype(int)
            dummy_prediction = np.full(prediction_probas.shape, 1 / prediction_probas.shape[1])
            dummy_log_loss = sklearn.metrics.log_loss(binaraized_target, dummy_prediction)
            dummy_metrics.log_loss = dummy_log_loss
        threshold_dummy_results = {}

        for threshold in self.thresholds:
            threshold_dummy_results[threshold] = _dummy_threshold_metrics(threshold, dummy_metrics)

        k_dummy_results = {}

        for k in self.k_variants:
            threshold = k_probability_threshold(prediction_probas, k)
            k_dummy_results[k] = _dummy_threshold_metrics(threshold, dummy_metrics)

        dummy_metrics.roc_auc = 0.5

        # data for plots
        curr_for_plots = None
        ref_for_plots = None
        if prediction_probas is not None:
            curr_for_plots = _collect_plot_data(prediction_probas)
        if data.reference_data is not None and ref_probas is not None:
            ref_for_plots = _collect_plot_data(ref_probas)

        return ClassificationPerformanceMetricsResults(
            current_metrics=current_metrics,
            current_by_k_metrics=current_by_k_metrics,
            current_by_threshold_metrics=current_by_thresholds_metrics,
            reference_metrics=reference_metrics,
            reference_by_k_metrics=reference_by_k,
            reference_by_threshold_metrics=reference_by_threshold,
            dummy_metrics=dummy_metrics,
            dummy_by_k_metrics=k_dummy_results,
            dummy_by_threshold_metrics=threshold_dummy_results,
            data_for_plots=DataForPlots(current=curr_for_plots, reference=ref_for_plots),
        )


def _dummy_threshold_metrics(
    threshold: float, dummy_results: DatasetClassificationPerformanceMetrics
) -> DatasetClassificationPerformanceMetrics:
    if threshold == 1.0:
        mult_precision = 1.0
    else:
        mult_precision = min(1.0, 0.5 / (1 - threshold))
    mult_recall = min(1.0, (1 - threshold) / 0.5)

    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    if (
        dummy_results.tpr is not None
        and dummy_results.tnr is not None
        and dummy_results.fpr is not None
        and dummy_results.fnr is not None
    ):
        tpr = dummy_results.tpr * mult_recall
        tnr = dummy_results.tnr * mult_precision
        fpr = dummy_results.fpr * mult_recall
        fnr = dummy_results.fnr * mult_precision

    return DatasetClassificationPerformanceMetrics(
        accuracy=dummy_results.accuracy,
        precision=dummy_results.precision * mult_precision,
        recall=dummy_results.recall * mult_recall,
        f1=2
        * dummy_results.precision
        * mult_precision
        * dummy_results.recall
        * mult_recall
        / (dummy_results.precision * mult_precision + dummy_results.recall * mult_recall),
        roc_auc=None,
        log_loss=dummy_results.log_loss,
        metrics_matrix=dummy_results.metrics_matrix,
        confusion_matrix=dummy_results.confusion_matrix,
        confusion_by_classes=dummy_results.confusion_by_classes,
        tpr=tpr,
        tnr=tnr,
        fpr=fpr,
        fnr=fnr
    )


def _cleanup_data(data: pd.DataFrame, mapping: ColumnMapping) -> pd.DataFrame:
    target = mapping.target
    prediction = mapping.prediction
    subset = []
    if target is not None:
        subset.append(target)
    if prediction is not None and isinstance(prediction, list):
        subset += prediction
    if prediction is not None and isinstance(prediction, str):
        subset.append(prediction)
    if len(subset) > 0:
        return data.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any", subset=subset)
    return data


@dataclasses.dataclass
class PredictionData:
    predictions: pd.Series
    prediction_probas: Optional[pd.DataFrame]


def get_prediction_data(
    data: pd.DataFrame, mapping: ColumnMapping, threshold: float = 0.5
) -> PredictionData:
    """Get predicted values and optional prediction probabilities from source data.
    Also take into account a threshold value - if a probability is less than the value, do not take it into account.

    Return and object with predicted values and an optional prediction probabilities.
    """
    # binary or multiclass classification
    # for binary prediction_probas has column order [pos_label, neg_label]
    # for multiclass classification return just values and probas
    if isinstance(mapping.prediction, list) and len(mapping.prediction) > 2:
        # list of columns with prediction probas, should be same as target labels
        return PredictionData(
            predictions=data[mapping.prediction].idxmax(axis=1),
            prediction_probas=data[mapping.prediction]
        )

    # calculate labels as np.array - for better negative label calculations for binary classification
    if mapping.target_names is not None:
        # if target_names is specified, get labels from it
        labels = np.array(mapping.target_names)

    else:
        # if target_names is not specified, try to get labels from target and/or prediction
        if isinstance(mapping.prediction, str) and not is_float_dtype(data[mapping.prediction]):
            # if prediction is not probas, get unique values from it and target
            labels = np.union1d(data[mapping.target].unique(), data[mapping.prediction].unique())

        else:
            # if prediction is probas, get unique values from target only
            labels = data[mapping.target].unique()

    # binary classification
    # prediction in mapping is a list of two columns:
    # one is positive value probabilities, second is negative value probabilities
    if isinstance(mapping.prediction, list) and len(mapping.prediction) == 2:
        if mapping.pos_label not in labels or mapping.pos_label is None:
            raise ValueError("Undefined pos_label.")

        # get negative label for binary classification
        neg_label = labels[labels != mapping.pos_label][0]

        predictions = threshold_probability_labels(data[mapping.prediction], mapping.pos_label, neg_label, threshold)
        return PredictionData(predictions=predictions, prediction_probas=data[[mapping.pos_label, neg_label]])

    # binary classification
    # target is strings or other values, prediction is a string with positive label name, one column with probabilities
    if (
        isinstance(mapping.prediction, str)
        and (is_string_dtype(data[mapping.target]) or is_object_dtype(data[mapping.target]))
        and is_float_dtype(data[mapping.prediction])
    ):
        if mapping.pos_label is None or mapping.pos_label not in labels:
            raise ValueError("Undefined pos_label.")

        if mapping.prediction not in labels:
            raise ValueError(
                "No prediction for the target labels were found. "
                "Consider to rename columns with the prediction to match target labels."
            )

        # get negative label for binary classification
        neg_label = labels[labels != mapping.pos_label][0]

        if mapping.pos_label == mapping.prediction:
            pos_preds = data[mapping.prediction]

        else:
            pos_preds = data[mapping.prediction].apply(lambda x: 1.0 - x)

        prediction_probas = pd.DataFrame.from_dict(
            {
                mapping.pos_label: pos_preds,
                neg_label: pos_preds.apply(lambda x: 1.0 - x),
            }
        )
        predictions = threshold_probability_labels(prediction_probas, mapping.pos_label, neg_label, threshold)
        return PredictionData(predictions=predictions, prediction_probas=prediction_probas)

    # binary target and preds are numbers and prediction is a label
    if not isinstance(mapping.prediction, list) and mapping.prediction in [0, 1, "0", "1"] and mapping.pos_label == 0:
        if mapping.prediction in [0, "0"]:
            pos_preds = data[mapping.prediction]
        else:
            pos_preds = data[mapping.prediction].apply(lambda x: 1.0 - x)
        predictions = pos_preds.apply(lambda x: 0 if x >= threshold else 1)
        prediction_probas = pd.DataFrame.from_dict(
            {
                0: pos_preds,
                1: pos_preds.apply(lambda x: 1.0 - x),
            }
        )
        return PredictionData(predictions=predictions, prediction_probas=prediction_probas)

    # binary target and preds are numbers
    elif (
        isinstance(mapping.prediction, str)
        and data[mapping.target].dtype == dtype("int")
        and data[mapping.prediction].dtype == dtype("float")
    ):
        predictions = (data[mapping.prediction] >= threshold).astype(int)
        prediction_probas = pd.DataFrame.from_dict(
            {
                1: data[mapping.prediction],
                0: data[mapping.prediction].apply(lambda x: 1.0 - x),
            }
        )
        return PredictionData(predictions=predictions, prediction_probas=prediction_probas)

    # for other cases return just prediction values, probabilities are None by default
    return PredictionData(predictions=data[mapping.prediction], prediction_probas=None)


def _collect_plot_data(prediction_probas: pd.DataFrame):
    res = {}
    mins = []
    lowers = []
    means = []
    uppers = []
    maxs = []
    for col in prediction_probas.columns:
        mins.append(np.percentile(prediction_probas[col], 0))
        lowers.append(np.percentile(prediction_probas[col], 25))
        means.append(np.percentile(prediction_probas[col], 50))
        uppers.append(np.percentile(prediction_probas[col], 75))
        maxs.append(np.percentile(prediction_probas[col], 100))
    res["mins"] = mins
    res["lowers"] = lowers
    res["means"] = means
    res["uppers"] = uppers
    res["maxs"] = maxs
    return res
