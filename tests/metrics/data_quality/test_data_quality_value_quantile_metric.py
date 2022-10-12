import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import DataQualityValueQuantileMetric
from evidently.metrics.base_metric import InputData


def test_data_quality_quantile_metrics() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueQuantileMetric(column_name="numerical_feature", quantile=0.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.quantile == 0.5
    assert result.value == 2
