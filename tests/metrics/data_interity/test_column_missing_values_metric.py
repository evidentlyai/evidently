import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics.data_integrity.column_missing_values_metric import ColumnMissingValues
from evidently.legacy.metrics.data_integrity.column_missing_values_metric import ColumnMissingValuesMetric
from evidently.legacy.metrics.data_integrity.column_missing_values_metric import ColumnMissingValuesMetricResult
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "category_feature": ["3", "a", "b5", "a", "None"],
                    "target": [1, 2, 1, 2, 1],
                    "prediction": [1, 1, 1, 2, 2],
                }
            ),
            None,
            ColumnMissingValuesMetric("category_feature"),
            ColumnMissingValuesMetricResult(
                column_name="category_feature",
                current=ColumnMissingValues(
                    number_of_rows=5,
                    different_missing_values={None: 0, -np.inf: 0, np.inf: 0, "": 0},
                    number_of_different_missing_values=0,
                    number_of_missing_values=0,
                    share_of_missing_values=0,
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
            ColumnMissingValuesMetric(column_name="feature", missing_values=["a"], replace=False),
            ColumnMissingValuesMetricResult(
                column_name="feature",
                current=ColumnMissingValues(
                    number_of_rows=5,
                    different_missing_values={None: 2, "a": 1, "": 0, np.inf: 0, -np.inf: 0},
                    number_of_different_missing_values=2,
                    number_of_missing_values=3,
                    share_of_missing_values=0.6,
                ),
                reference=ColumnMissingValues(
                    number_of_rows=3,
                    different_missing_values={"a": 2, "": 0, None: 0, np.inf: 0, -np.inf: 0},
                    number_of_different_missing_values=1,
                    number_of_missing_values=2,
                    share_of_missing_values=0.6666666666666666,
                ),
            ),
        ),
    ),
)
def test_column_missing_values_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    metric: ColumnMissingValuesMetric,
    expected_result: ColumnMissingValuesMetricResult,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    result = metric.get_result()
    assert result == expected_result


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
            ColumnMissingValuesMetric(column_name="test"),
        ),
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "test": ["a", "a", "c"],
                }
            ),
            ColumnMissingValuesMetric(column_name="feature"),
        ),
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "test": ["a", "a", "c"],
                }
            ),
            ColumnMissingValuesMetric(column_name="test"),
        ),
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnMissingValuesMetric(column_name="col", missing_values=[], replace=True),
        ),
    ),
)
def test_column_missing_values_metric_value_error(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnMissingValuesMetric
) -> None:
    with pytest.raises(ValueError):
        report = Report(metrics=[metric])
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
        metric.get_result()


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_json",
    (
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnMissingValuesMetric(column_name="col"),
            {
                "column_name": "col",
                "current": {
                    "different_missing_values": {"": 0, "-Infinity": 0, "Infinity": 0, "null": 0},
                    "number_of_different_missing_values": 0,
                    "number_of_missing_values": 0,
                    "number_of_rows": 5,
                    "share_of_missing_values": 0.0,
                },
                "reference": None,
            },
        ),
        (
            pd.DataFrame(
                {
                    "feature": [np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "feature": ["a", "a", "c"],
                }
            ),
            ColumnMissingValuesMetric(column_name="feature", missing_values=["a"]),
            {
                "column_name": "feature",
                "current": {
                    "different_missing_values": {"a": 0},
                    "number_of_different_missing_values": 0,
                    "number_of_missing_values": 0,
                    "number_of_rows": 2,
                    "share_of_missing_values": 0.0,
                },
                "reference": {
                    "different_missing_values": {"a": 2},
                    "number_of_different_missing_values": 1,
                    "number_of_missing_values": 2,
                    "number_of_rows": 3,
                    "share_of_missing_values": 0.6666666666666666,
                },
            },
        ),
        (
            pd.DataFrame(
                {
                    "col": [1, np.nan, 3, None, 5, "a", "b", "c", 1, 1234567890, "a", "a", "d", "e", "f"],
                }
            ),
            None,
            ColumnMissingValuesMetric(column_name="col", missing_values=["a"], replace=False),
            {
                "column_name": "col",
                "current": {
                    "different_missing_values": {"": 0, "-Infinity": 0, "Infinity": 0, "a": 3, "null": 2},
                    "number_of_different_missing_values": 2,
                    "number_of_missing_values": 5,
                    "number_of_rows": 15,
                    "share_of_missing_values": 0.3333333333333333,
                },
                "reference": None,
            },
        ),
    ),
)
def test_column_missing_values_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnMissingValuesMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data)
    assert report.show()
    json_result = report.json()
    result = json.loads(json_result)
    assert result["metrics"][0]["metric"] == "ColumnMissingValuesMetric"
    assert result["metrics"][0]["result"] == expected_json
