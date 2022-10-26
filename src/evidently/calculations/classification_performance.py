from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass
from numpy import dtype
from pandas.core.dtypes.common import is_float_dtype
from pandas.core.dtypes.common import is_integer_dtype
from pandas.core.dtypes.common import is_object_dtype
from pandas.core.dtypes.common import is_string_dtype

from evidently.utils.data_operations import DatasetColumns


@dataclass
class ConfusionMatrix:
    labels: Sequence[Union[str, int]]
    values: list


def calculate_confusion_by_classes(
    confusion_matrix: np.ndarray,
    class_names: Sequence[Union[str, int]],
) -> Dict[Union[str, int], Dict[str, int]]:
    """Calculate metrics
        TP (true positive)
        TN (true negative)
        FP (false positive)
        FN (false negative)
    for each class from confusion matrix.

    Returns a dict like:
    {
        "class_1_name": {
            "tp": 1,
            "tn": 5,
            "fp": 0,
            "fn": 3,
        },
        ...
    }
    """
    true_positive = np.diag(confusion_matrix)
    false_positive = confusion_matrix.sum(axis=0) - np.diag(confusion_matrix)
    false_negative = confusion_matrix.sum(axis=1) - np.diag(confusion_matrix)
    true_negative = confusion_matrix.sum() - (false_positive + false_negative + true_positive)
    confusion_by_classes = {}

    for idx, class_name in enumerate(class_names):
        confusion_by_classes[class_name] = {
            "tp": true_positive[idx],
            "tn": true_negative[idx],
            "fp": false_positive[idx],
            "fn": false_negative[idx],
        }

    return confusion_by_classes


def k_probability_threshold(prediction_probas: pd.DataFrame, k: Union[int, float]) -> float:
    probas = prediction_probas.iloc[:, 0].sort_values(ascending=False)
    if isinstance(k, float):
        if k < 0.0 or k > 1.0:
            raise ValueError(f"K should be in range [0.0, 1.0] but was {k}")
        return probas.iloc[max(int(np.ceil(k * prediction_probas.shape[0])) - 1, 0)]
    if isinstance(k, int):
        return probas.iloc[min(k, prediction_probas.shape[0] - 1)]
    raise ValueError(f"K has unexpected type {type(k)}")


@dataclasses.dataclass
class PredictionData:
    predictions: pd.Series
    prediction_probas: Optional[pd.DataFrame]
    labels: List[Union[str, int]]


def get_prediction_data(
    data: pd.DataFrame,
    data_columns: DatasetColumns,
    pos_label: Optional[Union[str, int]],
    threshold: float = 0.5,
) -> PredictionData:
    """Get predicted values and optional prediction probabilities from source data.
    Also take into account a threshold value - if a probability is less than the value, do not take it into account.

    Return and object with predicted values and an optional prediction probabilities.
    """
    # binary or multiclass classification
    # for binary prediction_probas has column order [pos_label, neg_label]
    # for multiclass classification return just values and probas
    prediction = data_columns.utility_columns.prediction
    target = data_columns.utility_columns.target
    if isinstance(prediction, list) and len(prediction) > 2:
        # list of columns with prediction probas, should be same as target labels
        return PredictionData(
            predictions=data[prediction].idxmax(axis=1),
            prediction_probas=data[prediction],
            labels=prediction,
        )

    # calculate labels as np.array - for better negative label calculations for binary classification
    if data_columns.target_names is not None:
        # if target_names is specified, get labels from it
        labels = np.array(data_columns.target_names)

    else:
        # if target_names is not specified, try to get labels from target and/or prediction
        if isinstance(prediction, str) and not is_float_dtype(data[prediction]):
            # if prediction is not probas, get unique values from it and target
            labels = np.union1d(data[target].unique(), data[prediction].unique())

        else:
            # if prediction is probas, get unique values from target only
            labels = data[target].unique()

    # binary classification
    # prediction in mapping is a list of two columns:
    # one is positive value probabilities, second is negative value probabilities
    if isinstance(prediction, list) and len(prediction) == 2:
        pos_label = _check_pos_labels(pos_label, labels)

        # get negative label for binary classification
        neg_label = labels[labels != pos_label][0]

        predictions = threshold_probability_labels(data[prediction], pos_label, neg_label, threshold)
        return PredictionData(
            predictions=predictions,
            prediction_probas=data[[pos_label, neg_label]],
            labels=[pos_label, neg_label],
        )

    # binary classification
    # target is strings or other values, prediction is a string with positive label name, one column with probabilities
    if (
        isinstance(prediction, str)
        and (is_string_dtype(data[target]) or is_object_dtype(data[target]))
        and is_float_dtype(data[prediction])
    ):
        pos_label = _check_pos_labels(pos_label, labels)

        if prediction not in labels:
            raise ValueError(
                "No prediction for the target labels were found. "
                "Consider to rename columns with the prediction to match target labels."
            )

        # get negative label for binary classification
        neg_label = labels[labels != pos_label][0]

        if pos_label == prediction:
            pos_preds = data[prediction]

        else:
            pos_preds = data[prediction].apply(lambda x: 1.0 - x)

        prediction_probas = pd.DataFrame.from_dict(
            {
                pos_label: pos_preds,
                neg_label: pos_preds.apply(lambda x: 1.0 - x),
            }
        )
        predictions = threshold_probability_labels(prediction_probas, pos_label, neg_label, threshold)
        return PredictionData(
            predictions=predictions,
            prediction_probas=prediction_probas,
            labels=[pos_label, neg_label],
        )

    # binary target and preds are numbers and prediction is a label
    if not isinstance(prediction, list) and prediction in [0, 1, "0", "1"] and pos_label == 0:
        if prediction in [0, "0"]:
            pos_preds = data[prediction]
        else:
            pos_preds = data[prediction].apply(lambda x: 1.0 - x)
        predictions = pos_preds.apply(lambda x: 0 if x >= threshold else 1)
        prediction_probas = pd.DataFrame.from_dict(
            {
                0: pos_preds,
                1: pos_preds.apply(lambda x: 1.0 - x),
            }
        )
        return PredictionData(
            predictions=predictions,
            prediction_probas=prediction_probas,
            labels=[0, 1],
        )

    # binary target and preds are numbers
    elif (
        isinstance(prediction, str)
        and is_integer_dtype(data[target].dtype)
        and data[prediction].dtype == dtype("float")
    ):
        predictions = (data[prediction] >= threshold).astype(dtype("int64"))
        prediction_probas = pd.DataFrame.from_dict(
            {
                1: data[prediction],
                0: data[prediction].apply(lambda x: 1.0 - x),
            }
        )
        return PredictionData(
            predictions=predictions,
            prediction_probas=prediction_probas,
            labels=[0, 1],
        )

    # for other cases return just prediction values, probabilities are None by default
    return PredictionData(
        predictions=data[prediction],
        prediction_probas=None,
        labels=data[prediction].unique().tolist(),
    )


def _check_pos_labels(pos_label: Optional[Union[str, int]], labels: List[str]) -> Union[str, int]:
    if pos_label is None:
        raise ValueError("Undefined pos_label.")

    if pos_label not in labels:
        raise ValueError(f"Cannot find pos_label '{pos_label}' in labels {labels}")

    return pos_label


def threshold_probability_labels(
    prediction_probas: pd.DataFrame, pos_label: Union[str, int], neg_label: Union[str, int], threshold: float
) -> pd.Series:
    """Get prediction values by probabilities with the threshold apply"""
    return prediction_probas[pos_label].apply(lambda x: pos_label if x >= threshold else neg_label)


STEP_SIZE = 0.05


def calculate_pr_table(binded):
    result = []
    binded.sort(key=lambda item: item[1], reverse=True)
    data_size = len(binded)
    target_class_size = sum([x[0] for x in binded])
    offset = max(round(data_size * STEP_SIZE), 1)

    for step in np.arange(offset, data_size + offset, offset):
        count = min(step, data_size)
        prob = round(binded[min(step, data_size - 1)][1], 2)
        top = round(100.0 * min(step, data_size) / data_size, 1)
        tp = sum([x[0] for x in binded[: min(step, data_size)]])
        fp = count - tp
        precision = round(100.0 * tp / count, 1)
        recall = round(100.0 * tp / target_class_size, 1)
        result.append([top, int(count), prob, int(tp), int(fp), precision, recall])
    return result
