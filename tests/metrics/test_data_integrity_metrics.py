import numpy as np
import pandas as pd
import pytest

from evidently.metrics import DataIntegrityMetrics
from evidently.metrics import DataIntegrityValueByRegexpMetrics
from evidently.metrics import DataIntegrityNullValuesMetrics
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.data_integrity_metrics import DataIntegrityValueByRegexpMetricResult
from evidently.metrics.data_integrity_metrics import DataIntegrityValueByRegexpStat
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


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
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current.number_of_columns == 4
    assert result.current.number_of_rows == 3


@pytest.mark.parametrize(
    "current_data, reference_data, column_name, reg_exp, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "category_feature": ["3", "a", "b5", "a", np.nan],
                    "target": [1, 2, 1, 2, 1],
                    "prediction": [1, 1, 1, 2, 2],
                }
            ),
            None,
            "category_feature",
            r".*\d+.*",
            DataIntegrityValueByRegexpMetricResult(
                column_name="category_feature",
                reg_exp=r".*\d+.*",
                current=DataIntegrityValueByRegexpStat(
                    number_of_matched=2,
                    number_of_not_matched=2,
                    number_of_rows=5,
                    table_of_matched={"3": 1, "b5": 1},
                    table_of_not_matched={"a": 2},
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "feature": ["a", "a", "c"],
                }
            ),
            "feature",
            r"^\s+.*",
            DataIntegrityValueByRegexpMetricResult(
                column_name="feature",
                reg_exp=r"^\s+.*",
                current=DataIntegrityValueByRegexpStat(
                    number_of_matched=2,
                    number_of_not_matched=1,
                    number_of_rows=5,
                    table_of_matched={" a": 1, "\tb": 1},
                    table_of_not_matched={"a": 1},
                ),
                reference=DataIntegrityValueByRegexpStat(
                    number_of_matched=0,
                    number_of_not_matched=3,
                    number_of_rows=3,
                    table_of_matched={},
                    table_of_not_matched={"a": 2, "c": 1},
                ),
            ),
        ),
    ),
)
def test_data_integrity_value_by_regexp_metric(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    reg_exp: str,
    expected_result: DataIntegrityValueByRegexpMetricResult,
) -> None:
    metric = DataIntegrityValueByRegexpMetrics(column_name=column_name, reg_exp=reg_exp)
    result = metric.calculate(
        data=InputData(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "metric_object",
    (
        DataIntegrityMetrics(),
        DataIntegrityValueByRegexpMetrics(column_name="feature", reg_exp=r".*a.*"),
        DataIntegrityNullValuesMetrics(null_values=[None]),
    ),
)
def test_data_integrity_metrics_with_report(metric_object: Metric) -> None:
    test_dataset = pd.DataFrame(
        {
            "feature": [" a", "a", "\tb", np.nan, np.nan],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[metric_object])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    assert report.show()
    assert report.json()

    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_data_integrity_metrics_different_null_values() -> None:
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
    metric = DataIntegrityNullValuesMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    # expect na values and an empty string as null-values
    assert result.current_null_values.different_nulls == {None: 5, -np.inf: 1, np.inf: 1, "": 2}
    assert result.current_null_values.number_of_different_nulls == 4
    assert result.current_null_values.number_of_nulls == 9
    assert result.current_null_values.different_nulls_by_column == {
        "category_feature_1": {None: 0, -np.inf: 0, np.inf: 0, "": 1},
        "category_feature_2": {None: 1, -np.inf: 0, np.inf: 1, "": 1},
        "numerical_feature_1": {None: 0, -np.inf: 0, np.inf: 0, "": 0},
        "numerical_feature_2": {None: 1, -np.inf: 1, np.inf: 0, "": 0},
        "prediction": {None: 1, -np.inf: 0, np.inf: 0, "": 0},
        "target": {None: 2, -np.inf: 0, np.inf: 0, "": 0},
    }
    assert result.current_null_values.number_of_different_nulls_by_column == {
        "category_feature_1": 1,
        "category_feature_2": 3,
        "numerical_feature_1": 0,
        "numerical_feature_2": 2,
        "prediction": 1,
        "target": 1,
    }
    assert result.current_null_values.number_of_nulls_by_column == {
        "category_feature_1": 1,
        "category_feature_2": 3,
        "numerical_feature_1": 0,
        "numerical_feature_2": 2,
        "prediction": 1,
        "target": 2,
    }
    assert result.reference_null_values is None

    metric = DataIntegrityNullValuesMetrics(null_values=["n/a"], replace=False)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    # expect n/a and other defaults as null-values
    assert result.current_null_values.number_of_different_nulls == 5
    assert result.current_null_values.number_of_nulls == 10
    assert result.reference_null_values is None

    # test custom list of null values, no default, but with Pandas nulls
    metric = DataIntegrityNullValuesMetrics(null_values=["", 0, "n/a", -9999, None], replace=True)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current_null_values.number_of_different_nulls == 5
    assert result.current_null_values.number_of_nulls == 11
    assert result.reference_null_values is None

    # test custom list of null values and ignore pandas null values
    metric = DataIntegrityNullValuesMetrics(null_values=["", 0, "n/a", -9999], replace=True)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current_null_values.number_of_different_nulls == 4
    assert result.current_null_values.number_of_nulls == 6
    assert result.reference_null_values is None
