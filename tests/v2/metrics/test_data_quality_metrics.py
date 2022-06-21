import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.data_quality_metrics import DataQualityMetrics
from evidently.v2.metrics.data_quality_metrics import DataStabilityMetrics


def test_data_quality_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 2, 2, 432]
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None


def test_data_stability_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "y", "n", "y"],
            "numerical_feature": [10, 20, 30, 50],
            "target": [1, 0, 1, 0]
        }
    )
    data_mapping = ColumnMapping()
    metric = DataStabilityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
