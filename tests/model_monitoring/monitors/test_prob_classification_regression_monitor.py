import pandas as pd
import pytest

from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring.monitors.prob_classification_performance import ProbClassificationPerformanceMonitor
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.tests.utils import approx
from tests.model_monitoring.helpers import collect_metrics_results


def test_monitor_id():
    assert ProbClassificationPerformanceMonitor().monitor_id() == "prob_classification_performance"


def test_probability_classification_with_multi_classes() -> None:
    reference_data = pd.DataFrame(
        {
            "target": [
                "label_a",
                "label_a",
                "label_a",
                "label_b",
                "label_c",
                "label_c",
            ],
            "label_a": [0.1, 0.1, 0.3, 0.4, 0.4, 0.1],
            "label_b": [0.2, 0.1, 0.7, 0.5, 0.5, 0.1],
            "label_c": [0.7, 0.8, 0.0, 0.1, 0.1, 0.8],
        }
    )
    current_data = pd.DataFrame(
        {
            "target": [
                "label_c",
                "label_b",
                "label_a",
                "label_c",
                "label_b",
                "label_a",
            ],
            "label_a": [0.2, 0.2, 0.9, 0.2, 0.2, 0.35],
            "label_b": [0.1, 0.6, 0.1, 0.4, 0.5, 0.35],
            "label_c": [0.7, 0.2, 0.0, 0.4, 0.3, 0.3],
        }
    )
    mapping = ColumnMapping(
        target="target",
        prediction=["label_a", "label_c", "label_b"],
    )
    evidently_monitoring = ModelMonitoring(
        monitors=[ProbClassificationPerformanceMonitor()],
        options=None,
    )
    evidently_monitoring.execute(reference_data, current_data, column_mapping=mapping)
    result = collect_metrics_results(evidently_monitoring.metrics())

    assert "prob_classification_performance:quality" in result
    quality = result["prob_classification_performance:quality"]
    assert quality == [
        {
            "labels": {"dataset": "reference", "metric": "accuracy"},
            "value": 0.3333333333333333,
        },
        {
            "labels": {"dataset": "reference", "metric": "precision"},
            "value": 0.2222222222222222,
        },
        {"labels": {"dataset": "reference", "metric": "recall"}, "value": 0.5},
        {"labels": {"dataset": "reference", "metric": "f1"}, "value": 0.3},
        {
            "labels": {"dataset": "reference", "metric": "roc_auc"},
            "value": 0.5157407407407407,
        },
        {
            "labels": {"dataset": "reference", "metric": "log_loss"},
            "value": 1.5046698025303715,
        },
        {"labels": {"dataset": "current", "metric": "accuracy"}, "value": 1.0},
        {"labels": {"dataset": "current", "metric": "precision"}, "value": 1.0},
        {"labels": {"dataset": "current", "metric": "recall"}, "value": 1.0},
        {"labels": {"dataset": "current", "metric": "f1"}, "value": 1.0},
        {"labels": {"dataset": "current", "metric": "roc_auc"}, "value": 1.0},
        {
            "labels": {"dataset": "current", "metric": "log_loss"},
            "value": approx(0.6053535200492214),
        },
    ]
    assert "prob_classification_performance:class_representation" in result
    class_representation = result["prob_classification_performance:class_representation"]
    assert class_representation == [
        {
            "labels": {
                "class_name": "label_a",
                "dataset": "reference",
                "type": "target",
            },
            "value": 3,
        },
        {
            "labels": {
                "class_name": "label_a",
                "dataset": "reference",
                "type": "prediction",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_name": "label_b",
                "dataset": "reference",
                "type": "target",
            },
            "value": 1,
        },
        {
            "labels": {
                "class_name": "label_b",
                "dataset": "reference",
                "type": "prediction",
            },
            "value": 3,
        },
        {
            "labels": {
                "class_name": "label_c",
                "dataset": "reference",
                "type": "target",
            },
            "value": 2,
        },
        {
            "labels": {
                "class_name": "label_c",
                "dataset": "reference",
                "type": "prediction",
            },
            "value": 3,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "current", "type": "target"},
            "value": 2,
        },
        {
            "labels": {
                "class_name": "label_a",
                "dataset": "current",
                "type": "prediction",
            },
            "value": 2,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "current", "type": "target"},
            "value": 2,
        },
        {
            "labels": {
                "class_name": "label_b",
                "dataset": "current",
                "type": "prediction",
            },
            "value": 2,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "current", "type": "target"},
            "value": 2,
        },
        {
            "labels": {
                "class_name": "label_c",
                "dataset": "current",
                "type": "prediction",
            },
            "value": 2,
        },
    ]
    assert "prob_classification_performance:confusion" in result
    confusion = result["prob_classification_performance:confusion"]
    assert confusion == [
        {
            "labels": {
                "class_x_name": "label_a",
                "class_y_name": "label_a",
                "dataset": "reference",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_a",
                "class_y_name": "label_b",
                "dataset": "reference",
            },
            "value": 1,
        },
        {
            "labels": {
                "class_x_name": "label_a",
                "class_y_name": "label_c",
                "dataset": "reference",
            },
            "value": 2,
        },
        {
            "labels": {
                "class_x_name": "label_b",
                "class_y_name": "label_a",
                "dataset": "reference",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_b",
                "class_y_name": "label_b",
                "dataset": "reference",
            },
            "value": 1,
        },
        {
            "labels": {
                "class_x_name": "label_b",
                "class_y_name": "label_c",
                "dataset": "reference",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_c",
                "class_y_name": "label_a",
                "dataset": "reference",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_c",
                "class_y_name": "label_b",
                "dataset": "reference",
            },
            "value": 1,
        },
        {
            "labels": {
                "class_x_name": "label_c",
                "class_y_name": "label_c",
                "dataset": "reference",
            },
            "value": 1,
        },
        {
            "labels": {
                "class_x_name": "label_a",
                "class_y_name": "label_a",
                "dataset": "current",
            },
            "value": 2,
        },
        {
            "labels": {
                "class_x_name": "label_a",
                "class_y_name": "label_b",
                "dataset": "current",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_a",
                "class_y_name": "label_c",
                "dataset": "current",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_b",
                "class_y_name": "label_a",
                "dataset": "current",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_b",
                "class_y_name": "label_b",
                "dataset": "current",
            },
            "value": 2,
        },
        {
            "labels": {
                "class_x_name": "label_b",
                "class_y_name": "label_c",
                "dataset": "current",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_c",
                "class_y_name": "label_a",
                "dataset": "current",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_c",
                "class_y_name": "label_b",
                "dataset": "current",
            },
            "value": 0,
        },
        {
            "labels": {
                "class_x_name": "label_c",
                "class_y_name": "label_c",
                "dataset": "current",
            },
            "value": 2,
        },
    ]
    assert "prob_classification_performance:class_confusion" in result
    class_confusion = result["prob_classification_performance:class_confusion"]
    assert class_confusion == [
        {
            "labels": {"class_name": "label_a", "dataset": "reference", "metric": "TP"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "reference", "metric": "FP"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "reference", "metric": "TN"},
            "value": 3,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "reference", "metric": "FN"},
            "value": 3,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "reference", "metric": "TP"},
            "value": 1,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "reference", "metric": "FP"},
            "value": 2,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "reference", "metric": "TN"},
            "value": 3,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "reference", "metric": "FN"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "reference", "metric": "TP"},
            "value": 1,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "reference", "metric": "FP"},
            "value": 2,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "reference", "metric": "TN"},
            "value": 2,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "reference", "metric": "FN"},
            "value": 1,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "current", "metric": "TP"},
            "value": 2,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "current", "metric": "FP"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "current", "metric": "TN"},
            "value": 4,
        },
        {
            "labels": {"class_name": "label_a", "dataset": "current", "metric": "FN"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "current", "metric": "TP"},
            "value": 2,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "current", "metric": "FP"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "current", "metric": "TN"},
            "value": 4,
        },
        {
            "labels": {"class_name": "label_b", "dataset": "current", "metric": "FN"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "current", "metric": "TP"},
            "value": 2,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "current", "metric": "FP"},
            "value": 0,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "current", "metric": "TN"},
            "value": 4,
        },
        {
            "labels": {"class_name": "label_c", "dataset": "current", "metric": "FN"},
            "value": 0,
        },
    ]
