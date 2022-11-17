import json

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummary
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetricResult
from evidently.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, metric, expected_result",
    (
        (
            pd.DataFrame({}),
            None,
            ColumnMapping(),
            DatasetSummaryMetric(),
            DatasetSummaryMetricResult(
                almost_duplicated_threshold=0.95,
                current=DatasetSummary(
                    target=None,
                    prediction=None,
                    date_column=None,
                    id_column=None,
                    number_of_columns=0,
                    number_of_rows=0,
                    number_of_missing_values=0,
                    number_of_categorical_columns=0,
                    number_of_numeric_columns=0,
                    number_of_datetime_columns=0,
                    number_of_constant_columns=0,
                    number_of_empty_columns=0,
                    number_of_almost_constant_columns=0,
                    number_of_duplicated_columns=0,
                    number_of_almost_duplicated_columns=0,
                    number_of_empty_rows=0,
                    number_of_duplicated_rows=0,
                    columns_type={},
                    nans_by_columns={},
                    number_uniques_by_columns={},
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"target": [1, "ff", 3], "prediction": ["a", "b", "c"]}),
            pd.DataFrame({"target": [1, 2, 3, 4, 5], "prediction": [np.NaN, 2, 3, 4, 5]}),
            ColumnMapping(),
            DatasetSummaryMetric(),
            DatasetSummaryMetricResult(
                almost_duplicated_threshold=0.95,
                current=DatasetSummary(
                    target="target",
                    prediction="prediction",
                    date_column=None,
                    id_column=None,
                    number_of_columns=2,
                    number_of_rows=3,
                    number_of_missing_values=0,
                    number_of_categorical_columns=0,
                    number_of_numeric_columns=0,
                    number_of_datetime_columns=0,
                    number_of_constant_columns=0,
                    number_of_almost_constant_columns=0,
                    number_of_duplicated_columns=0,
                    number_of_almost_duplicated_columns=0,
                    number_of_empty_rows=0,
                    number_of_empty_columns=0,
                    number_of_duplicated_rows=0,
                    columns_type={"target": np.dtype("O"), "prediction": np.dtype("O")},
                    nans_by_columns={"target": 0, "prediction": 0},
                    number_uniques_by_columns={"target": 3, "prediction": 3},
                ),
                reference=DatasetSummary(
                    target="target",
                    prediction="prediction",
                    date_column=None,
                    id_column=None,
                    number_of_columns=2,
                    number_of_rows=5,
                    number_of_missing_values=1,
                    number_of_categorical_columns=0,
                    number_of_numeric_columns=0,
                    number_of_datetime_columns=0,
                    number_of_constant_columns=0,
                    number_of_almost_constant_columns=0,
                    number_of_duplicated_columns=0,
                    number_of_almost_duplicated_columns=0,
                    number_of_empty_rows=0,
                    number_of_empty_columns=0,
                    number_of_duplicated_rows=0,
                    columns_type={"target": np.dtype("int64"), "prediction": np.dtype("float64")},
                    nans_by_columns={"target": 0, "prediction": 1},
                    number_uniques_by_columns={"target": 5, "prediction": 4},
                ),
            ),
        ),
    ),
)
def test_dataset_summary_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    metric: DatasetSummaryMetric,
    expected_result: DatasetSummaryMetricResult,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
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
            DatasetSummaryMetric(almost_duplicated_threshold=-0.1),
        ),
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            DatasetSummaryMetric(almost_duplicated_threshold=95),
        ),
    ),
)
def test_dataset_summary_metric_value_error(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    metric: DatasetSummaryMetric,
) -> None:
    with pytest.raises(ValueError):
        report = Report(metrics=[metric])
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
        metric.get_result()


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, metric, expected_json",
    (
        (
            pd.DataFrame(),
            None,
            ColumnMapping(),
            DatasetSummaryMetric(almost_duplicated_threshold=0.9),
            {
                "almost_duplicated_threshold": 0.9,
                "current": {
                    "date_column": None,
                    "id_column": None,
                    "nans_by_columns": {},
                    "number_of_almost_constant_columns": 0,
                    "number_of_almost_duplicated_columns": 0,
                    "number_of_categorical_columns": 0,
                    "number_of_columns": 0,
                    "number_of_constant_columns": 0,
                    "number_of_datetime_columns": 0,
                    "number_of_duplicated_columns": 0,
                    "number_of_duplicated_rows": 0,
                    "number_of_empty_columns": 0,
                    "number_of_empty_rows": 0,
                    "number_of_missing_values": 0.0,
                    "number_of_numeric_columns": 0,
                    "number_of_rows": 0,
                    "number_uniques_by_columns": {},
                    "prediction": None,
                    "target": None,
                },
                "reference": None,
            },
        ),
        (
            pd.DataFrame({"test1": [1, 2, 3], "test2": [1, 2, 3], "test3": [1, 1, 1]}),
            pd.DataFrame({"test4": [1, 2, 3], "test2": ["a", "a", "a"], "test3": [1, 1, 1]}),
            ColumnMapping(),
            DatasetSummaryMetric(almost_duplicated_threshold=0.9),
            {
                "almost_duplicated_threshold": 0.9,
                "current": {
                    "date_column": None,
                    "id_column": None,
                    "nans_by_columns": {"test1": 0, "test2": 0, "test3": 0},
                    "number_of_almost_constant_columns": 1,
                    "number_of_almost_duplicated_columns": 1,
                    "number_of_categorical_columns": 0,
                    "number_of_columns": 3,
                    "number_of_constant_columns": 1,
                    "number_of_datetime_columns": 0,
                    "number_of_duplicated_columns": 1,
                    "number_of_duplicated_rows": 0,
                    "number_of_empty_columns": 0,
                    "number_of_empty_rows": 0,
                    "number_of_missing_values": 0,
                    "number_of_numeric_columns": 3,
                    "number_of_rows": 3,
                    "number_uniques_by_columns": {"test1": 3, "test2": 3, "test3": 1},
                    "prediction": None,
                    "target": None,
                },
                "reference": {
                    "date_column": None,
                    "id_column": None,
                    "nans_by_columns": {"test2": 0, "test3": 0, "test4": 0},
                    "number_of_almost_constant_columns": 2,
                    "number_of_almost_duplicated_columns": 0,
                    "number_of_categorical_columns": 1,
                    "number_of_columns": 3,
                    "number_of_constant_columns": 2,
                    "number_of_datetime_columns": 0,
                    "number_of_duplicated_columns": 0,
                    "number_of_duplicated_rows": 0,
                    "number_of_empty_columns": 0,
                    "number_of_empty_rows": 0,
                    "number_of_missing_values": 0,
                    "number_of_numeric_columns": 2,
                    "number_of_rows": 3,
                    "number_uniques_by_columns": {"test2": 1, "test3": 1, "test4": 3},
                    "prediction": None,
                    "target": None,
                },
            },
        ),
    ),
)
def test_dataset_summary_metric_with_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    metric: DatasetSummaryMetric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    result = json.loads(json_result)
    assert result["results"][0]["metric"] == "DatasetSummaryMetric"
    assert result["results"][0]["result"] == expected_json
