import numpy as np
import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics import ClassificationPerformanceMetrics
from evidently.v2.metrics import ProbClassificationPerformanceMetrics


def test_classification_performance_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.NAN, 1],
            "prediction": [1, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = ClassificationPerformanceMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
    assert result.current_metrics.accuracy == 1
    assert result.current_metrics.f1 == 1
    assert result.current_metrics.precision == 1
    assert result.current_metrics.recall == 1


def test_prob_classification_performance_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["label_a", "label_a", "label_b"],
            "label_a": [0.2, 0.1, 0.5],
            "label_b": [0.8, 0.9, 0.5],
        }
    )
    data_mapping = ColumnMapping(
        target="target",
        prediction=["label_a", "label_b"],
    )
    metric = ProbClassificationPerformanceMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
    assert result.accuracy == 0
    assert result.f1 == 0
    assert result.precision == 0
    assert result.recall == 0
    assert result.roc_auc == 0
    assert result.roc_aucs is None
    assert result.log_loss > 1.5
