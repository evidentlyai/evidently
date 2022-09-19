from typing import Dict
from typing import List

import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class ConfusionMatrix:
    labels: List[str]
    values: list


def calculate_confusion_by_classes(confusion_matrix: pd.DataFrame, class_names: List[str]) -> Dict[str, Dict[str, int]]:
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
        confusion_by_classes[str(class_name)] = {
            "tp": true_positive[idx],
            "tn": true_negative[idx],
            "fp": false_positive[idx],
            "fn": false_negative[idx],
        }

    return confusion_by_classes
