import numpy as np

from evidently.calculations.classification_performance import (
    calculate_confusion_by_classes,
)


def test_calculate_confusion_by_classes():
    confusion_matrix = np.array([[4, 1], [2, 5]])
    labels = ["a", "b"]
    confusion_by_classes = calculate_confusion_by_classes(confusion_matrix, labels)
    assert confusion_by_classes[labels[0]] == {"tp": 4, "fn": 1, "fp": 2, "tn": 5}
    assert confusion_by_classes[labels[1]] == {"tp": 5, "fn": 2, "fp": 1, "tn": 4}
