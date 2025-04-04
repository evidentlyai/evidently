import json

import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.legacy.metrics.data_drift.dataset_drift_metric import DatasetDriftMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, data_mapping",
    (
        (
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [3, 2, 1],
                    "target": [None, np.nan, 1],
                    "prediction": [1, np.nan, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["1", "2", "3"],
                    "numerical_feature": [3, 2, 1],
                    "target": [None, np.nan, 1],
                    "prediction": [1, np.nan, 1],
                }
            ),
            ColumnMapping(),
        ),
        (
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [3, 2, 1],
                    "target": [None, np.nan, 1],
                    "prediction": [1, np.nan, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c", "a", "b", "c"],
                    "numerical_feature": [6, 6, 6, 9, 9, 9],
                    "target": [5, 4, 3, 2, 1, 0],
                    "prediction": [1, 2, 3, 4, 5, 6],
                }
            ),
            ColumnMapping(),
        ),
        # binary classification
        (
            pd.DataFrame(
                {
                    "category_feature": ["aa", "bb", "cc"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.3, 0.2, 0.1],
                    "label_b": [0.5, 0.5, 1],
                    "target": [1, 1, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.9, 0.5, 0.3],
                    "label_b": [0.2, 0.5, 0.7],
                    "target": [0, 0, 0],
                }
            ),
            ColumnMapping(prediction=["label_a", "label_b"]),
        ),
        # multi classification
        (
            pd.DataFrame(
                {
                    "category_feature": ["az", "bz", "cz"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.3, 0.2, 0.1],
                    "label_b": [0.5, 0.5, 1],
                    "label_c": [0.2, 0.5, 0.7],
                    "my_target": [1, 1, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.9, 0.5, 0.3],
                    "label_b": [0.2, 0.5, 0.7],
                    "label_c": [0.3, 0.2, 0.1],
                    "my_target": [0, 0, 0],
                }
            ),
            ColumnMapping(target="my_target", prediction=["label_a", "label_b", "label_c"]),
        ),
    ),
)
def test_dataset_drift_metric_no_errors(
    current_dataset: pd.DataFrame, reference_dataset: pd.DataFrame, data_mapping: ColumnMapping
) -> None:
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_dataset_drift_metric_value_error() -> None:
    test_data = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.nan, 1],
            "prediction": [1, np.nan, 1],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[DatasetDriftMetric()])

    with pytest.raises(ValueError):
        report.run(current_data=test_data, reference_data=None, column_mapping=data_mapping)
        report.json()

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        report.run(current_data=None, reference_data=test_data, column_mapping=data_mapping)
        report.json()


def test_dataset_drift_metric_with_options() -> None:
    current_dataset = pd.DataFrame(
        {
            "category_feature": ["az", "bz", "az"],
            "target": [1, 2, 3],
            "prediction": [1, 0, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "category_feature": ["a", "a", "b"],
            "target": [1, 4, 5],
            "prediction": [1, 0, 1],
        }
    )
    report = Report(metrics=[DatasetDriftMetric(stattest_threshold=0.7)])
    report.run(current_data=current_dataset, reference_data=reference_dataset)
    assert report.show()
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "DatasetDriftMetric"
    assert result["metrics"][0]["result"] == {
        "dataset_drift": True,
        "number_of_columns": 3,
        "number_of_drifted_columns": 2,
        "share_of_drifted_columns": approx(0.67, abs=0.01),
        "drift_share": 0.5,
    }


def test_dataset_drift_metric_json_output() -> None:
    current_dataset = pd.DataFrame(
        {
            "category_feature": ["a", "b", None],
            "target": [1, np.nan, 3],
            "prediction": [1, 0, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "category_feature": ["a", "a", "b", "b"],
            "target": [1, 4, 5, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    report = Report(metrics=[DatasetDriftMetric(stattest_threshold=0.7)])
    report.run(current_data=current_dataset, reference_data=reference_dataset)
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "DatasetDriftMetric"
    assert result["metrics"][0]["result"] == {
        "dataset_drift": True,
        "number_of_columns": 3,
        "number_of_drifted_columns": 2,
        "share_of_drifted_columns": approx(0.67, abs=0.01),
        "drift_share": 0.5,
    }
