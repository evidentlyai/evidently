import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics import DataQualityMetrics
from evidently.v2.metrics import DataQualityStabilityMetrics
from evidently.v2.metrics import DataQualityValueListMetrics


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


def test_data_quality_stability_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [1, 1, 2, 2, 5],
            "feature2": [1, 1, 2, 2, 8],
            "target": [1, 0, 1, 1, 0],
            "prediction": [1, 0, 1, 0, 0]
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityStabilityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
    assert result.number_not_stable_target == 2
    assert result.number_not_stable_prediction == 4


def test_data_quality_values_in_list_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 2, 2, 432]
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityValueListMetrics(column="category_feature", values=["d"])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
    assert result.number_in_list == 1
    assert result.number_not_in_list == 3
    assert result.share_in_list == 0.25
    assert result.share_not_in_list == 0.75

    metric = DataQualityValueListMetrics(column="numerical_feature", values=[2])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
    assert result.number_in_list == 2
    assert result.number_not_in_list == 2
    assert result.share_in_list == 0.5
    assert result.share_not_in_list == 0.5

    reference_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "y", "n", "y"],
            "numerical_feature": [0, 2, 2, 432]
        }
    )

    metric = DataQualityValueListMetrics(column="category_feature")
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
        metrics={}
    )
    assert result is not None
    assert result.number_in_list == 2
    assert result.number_not_in_list == 2
    assert result.share_in_list == 0.5
    assert result.share_not_in_list == 0.5
