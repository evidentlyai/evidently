import numpy as np
import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics import DataIntegrityMetrics
from evidently.metrics import DataIntegrityNullValuesMetrics


def test_data_integrity_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.NAN, 1],
            "prediction": [1, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataIntegrityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.current_stats.number_of_columns == 4
    assert result.current_stats.number_of_rows == 3


def test_data_integrity_metrics_different_null_values() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature_1": ["", "n/a", "3"],
            "category_feature_2": ["", None, np.inf],
            "numerical_feature_1": [3, -9999, 0],
            "numerical_feature_2": [0, None, np.inf],
            "target": [None, np.NAN, 1],
            "prediction": [1, pd.NaT, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataIntegrityNullValuesMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    # expect na values and an empty string as null-values
    assert result.current_null_values.number_of_differently_encoded_nulls == 3
    assert result.current_null_values.number_of_null_values == 9
    assert result.current_null_values.number_of_null_values_by_columns == {
        "category_feature_1": 1,
        "category_feature_2": 3,
        "numerical_feature_1": 0,
        "numerical_feature_2": 2,
        "prediction": 1,
        "target": 2,
    }
    assert result.current_null_values.number_of_differently_encoded_nulls_by_columns == {
        "category_feature_1": 1,
        "category_feature_2": 3,
        "numerical_feature_1": 0,
        "numerical_feature_2": 2,
        "prediction": 1,
        "target": 1,
    }
    assert result.reference_null_values is None

    metric = DataIntegrityNullValuesMetrics(ignore_na=True)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    # expect empty string as null-values
    assert result.current_null_values.number_of_differently_encoded_nulls == 2
    assert result.current_null_values.number_of_null_values == 4
    assert result.reference_null_values is None

    # test custom list of null values with na values
    metric = DataIntegrityNullValuesMetrics(null_values=["", 0, "n/a", -9999])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.current_null_values.number_of_differently_encoded_nulls == 5
    assert result.current_null_values.number_of_null_values == 11
    assert result.reference_null_values is None

    # test custom list of null values and ignore na values
    metric = DataIntegrityNullValuesMetrics(null_values=["", 0, "n/a", -9999], ignore_na=True)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.current_null_values.number_of_differently_encoded_nulls == 4
    assert result.current_null_values.number_of_null_values == 6
    assert result.reference_null_values is None
