import pandas as pd

from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring.monitors.classification_performance import ClassificationPerformanceMonitor
from evidently.pipeline.column_mapping import ColumnMapping

from tests.model_monitoring.helpers import collect_metrics_results


def test_classification_monitoring_metrics_with_binary_classification_data() -> None:
    reference_data = pd.DataFrame({"target": [1, 0, 1, 0], "prediction": [1, 1, 0, 1]})
    current_data = pd.DataFrame(
        {"target": [0, 1, 0, 1, 0, 1, 1, 0, 1, 1], "prediction": [1, 0, 1, 0, 0, 0, 0, 1, 0, 1]}
    )
    evidently_monitoring = ModelMonitoring(monitors=[ClassificationPerformanceMonitor()], options=None)
    evidently_monitoring.execute(
        reference_data=reference_data, current_data=current_data, column_mapping=ColumnMapping()
    )
    result = collect_metrics_results(evidently_monitoring.metrics())
    assert "classification_performance:quality" in result
    assert "classification_performance:class_quality" in result
    assert "classification_performance:class_representation" in result
    assert "classification_performance:confusion" in result
    quality_signals = result["classification_performance:quality"]
    assert quality_signals == [
        {"labels": {"dataset": "reference", "metric": "accuracy"}, "value": 0.25},
        {"labels": {"dataset": "reference", "metric": "precision"}, "value": 0.16666666666666666},
        {"labels": {"dataset": "reference", "metric": "recall"}, "value": 0.25},
        {"labels": {"dataset": "reference", "metric": "f1"}, "value": 0.2},
        {"labels": {"dataset": "current", "metric": "accuracy"}, "value": 0.2},
        {"labels": {"dataset": "current", "metric": "precision"}, "value": 0.20833333333333331},
        {"labels": {"dataset": "current", "metric": "recall"}, "value": 0.20833333333333331},
        {"labels": {"dataset": "current", "metric": "f1"}, "value": 0.2},
    ]
    class_quality_signals = result["classification_performance:class_quality"]
    assert class_quality_signals == [
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "precision"}, "value": 0.0},
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "recall"}, "value": 0.0},
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "f1"}, "value": 0.0},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "precision"}, "value": 0.3333333333333333},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "recall"}, "value": 0.5},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "f1"}, "value": 0.4},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "precision"}, "value": 0.16666666666666666},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "recall"}, "value": 0.25},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "f1"}, "value": 0.2},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "precision"}, "value": 0.25},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "recall"}, "value": 0.16666666666666666},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "f1"}, "value": 0.2},
    ]
    class_representation_signals = result["classification_performance:class_representation"]
    assert class_representation_signals == [
        {"labels": {"class_name": "0", "dataset": "reference", "type": "target"}, "value": 2},
        {"labels": {"class_name": "0", "dataset": "reference", "type": "prediction"}, "value": 1},
        {"labels": {"class_name": "1", "dataset": "reference", "type": "target"}, "value": 2},
        {"labels": {"class_name": "1", "dataset": "reference", "type": "prediction"}, "value": 3},
        {"labels": {"class_name": "0", "dataset": "current", "type": "target"}, "value": 4},
        {"labels": {"class_name": "0", "dataset": "current", "type": "prediction"}, "value": 6},
        {"labels": {"class_name": "1", "dataset": "current", "type": "target"}, "value": 6},
        {"labels": {"class_name": "1", "dataset": "current", "type": "prediction"}, "value": 4},
    ]

    confusion_signals = result["classification_performance:confusion"]
    assert confusion_signals == [
        {"labels": {"class_x_name": "0", "class_y_name": "0", "dataset": "reference"}, "value": 0},
        {"labels": {"class_x_name": "0", "class_y_name": "1", "dataset": "reference"}, "value": 2},
        {"labels": {"class_x_name": "1", "class_y_name": "0", "dataset": "reference"}, "value": 1},
        {"labels": {"class_x_name": "1", "class_y_name": "1", "dataset": "reference"}, "value": 1},
        {"labels": {"class_x_name": "0", "class_y_name": "0", "dataset": "current"}, "value": 1},
        {"labels": {"class_x_name": "0", "class_y_name": "1", "dataset": "current"}, "value": 3},
        {"labels": {"class_x_name": "1", "class_y_name": "0", "dataset": "current"}, "value": 5},
        {"labels": {"class_x_name": "1", "class_y_name": "1", "dataset": "current"}, "value": 1},
    ]
    class_confusion_signals = result["classification_performance:class_confusion"]
    assert class_confusion_signals == [
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "TP"}, "value": 0},
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "FP"}, "value": 1},
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "TN"}, "value": 1},
        {"labels": {"class_name": "0", "dataset": "reference", "metric": "FN"}, "value": 2},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "TP"}, "value": 1},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "FP"}, "value": 2},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "TN"}, "value": 0},
        {"labels": {"class_name": "1", "dataset": "reference", "metric": "FN"}, "value": 1},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "TP"}, "value": 1},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "FP"}, "value": 5},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "TN"}, "value": 1},
        {"labels": {"class_name": "0", "dataset": "current", "metric": "FN"}, "value": 3},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "TP"}, "value": 1},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "FP"}, "value": 3},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "TN"}, "value": 1},
        {"labels": {"class_name": "1", "dataset": "current", "metric": "FN"}, "value": 5},
    ]
