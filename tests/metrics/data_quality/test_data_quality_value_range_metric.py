import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import DataQualityValueRangeMetric
from evidently.metrics.base_metric import InputData


def test_data_quality_values_in_range_metrics() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueRangeMetric(column_name="numerical_feature", left=0, right=10.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_range == 3
    assert result.number_not_in_range == 1
    assert result.share_in_range == 0.75
    assert result.share_not_in_range == 0.25

    reference_dataset = pd.DataFrame({"numerical_feature": [0, 1, 1, 1]})

    metric = DataQualityValueRangeMetric(column_name="numerical_feature")
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_range == 1
    assert result.number_not_in_range == 3
    assert result.share_in_range == 0.25
    assert result.share_not_in_range == 0.75

    metric = DataQualityValueRangeMetric(column_name="numerical_feature", right=5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_range == 3
    assert result.number_not_in_range == 1
    assert result.share_in_range == 0.75
    assert result.share_not_in_range == 0.25
