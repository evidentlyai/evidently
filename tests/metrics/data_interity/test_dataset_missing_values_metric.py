import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import DatasetMissingValuesMetric
from evidently.metrics.base_metric import InputData
from evidently.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, metric",
    (
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            None,
            DatasetMissingValuesMetric(missing_values=[None]),
        ),
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "feature": [" a", np.nan, "\tb", pd.NaT, np.inf],
                }
            ),
            DatasetMissingValuesMetric(missing_values=[None]),
        ),
    ),
)
def test_dataset_missing_values_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: DatasetMissingValuesMetric
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data)
    assert report.show()
    assert report.json()


def test_dataset_missing_values_metric_different_missing_values() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature_1": ["", "n/a", "3"],
            "category_feature_2": ["", None, np.inf],
            "numerical_feature_1": [3, -9999, 0],
            "numerical_feature_2": [0, None, -np.inf],
            "prediction": [1, pd.NaT, 1],
            "target": [None, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = DatasetMissingValuesMetric()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    # expect na values and an empty string as null-values
    assert result.current.different_missing_values == {None: 5, -np.inf: 1, np.inf: 1, "": 2}
    assert result.current.number_of_different_missing_values == 4
    assert result.current.number_of_missing_values == 9
    assert result.current.number_of_rows_with_missing_values == 3
    assert result.current.different_missing_values_by_column == {
        "category_feature_1": {None: 0, -np.inf: 0, np.inf: 0, "": 1},
        "category_feature_2": {None: 1, -np.inf: 0, np.inf: 1, "": 1},
        "numerical_feature_1": {None: 0, -np.inf: 0, np.inf: 0, "": 0},
        "numerical_feature_2": {None: 1, -np.inf: 1, np.inf: 0, "": 0},
        "prediction": {None: 1, -np.inf: 0, np.inf: 0, "": 0},
        "target": {None: 2, -np.inf: 0, np.inf: 0, "": 0},
    }
    assert result.current.number_of_different_missing_values_by_column == {
        "category_feature_1": 1,
        "category_feature_2": 3,
        "numerical_feature_1": 0,
        "numerical_feature_2": 2,
        "prediction": 1,
        "target": 1,
    }
    assert result.current.number_of_missing_values_by_column == {
        "category_feature_1": 1,
        "category_feature_2": 3,
        "numerical_feature_1": 0,
        "numerical_feature_2": 2,
        "prediction": 1,
        "target": 2,
    }
    assert result.reference is None

    metric = DatasetMissingValuesMetric(missing_values=["n/a"], replace=False)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    # expect n/a and other defaults as null-values
    assert result.current.number_of_different_missing_values == 5
    assert result.current.number_of_missing_values == 10
    assert result.reference is None

    # test custom list of missing values, no default, but with Pandas null-like values
    metric = DatasetMissingValuesMetric(missing_values=["", 0, "n/a", -9999, None], replace=True)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current.number_of_different_missing_values == 5
    assert result.current.number_of_missing_values == 11
    assert result.reference is None

    # test custom list of null values and ignore pandas null-like values
    metric = DatasetMissingValuesMetric(missing_values=["", 0, "n/a", -9999], replace=True)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current.number_of_different_missing_values == 4
    assert result.current.number_of_missing_values == 6
    assert result.reference is None


@pytest.mark.parametrize(
    "current_data, reference_data, metric",
    (
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            DatasetMissingValuesMetric(missing_values=[], replace=True),
        ),
    ),
)
def test_dataset_missing_values_metrics_value_error(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    metric: DatasetMissingValuesMetric,
) -> None:
    with pytest.raises(ValueError):
        metric.calculate(
            data=InputData(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
        )
