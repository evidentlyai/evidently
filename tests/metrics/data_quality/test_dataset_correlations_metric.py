import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import DatasetCorrelationsMetric
from evidently.metrics.base_metric import InputData


def test_data_quality_correlation_metrics() -> None:
    current_dataset = pd.DataFrame(
        {
            "numerical_feature_1": [0, 2, 2, 2, 0],
            "numerical_feature_2": [0, 2, 2, 2, 0],
            "category_feature": [1, 2, 4, 2, 1],
            "target": [0, 2, 2, 2, 0],
            "prediction": [0, 2, 2, 2, 0],
        }
    )
    data_mapping = ColumnMapping()
    metric = DatasetCorrelationsMetric()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current.num_features == ["numerical_feature_1", "numerical_feature_2", "category_feature"]
    assert result.current.correlation_matrix is not None
    assert result.current.target_prediction_correlation == 1.0
    assert result.current.abs_max_target_features_correlation == 1.0
    assert result.current.abs_max_prediction_features_correlation == 1.0
    assert result.current.abs_max_correlation == 1.0
    assert result.current.abs_max_num_features_correlation == 1.0

    assert result.reference is None
