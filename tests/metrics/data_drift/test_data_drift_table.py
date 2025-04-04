import json

import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.legacy.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, data_mapping",
    (
        (
            pd.DataFrame(
                {
                    "category_feature": ["1", "2", "3"],
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
                    "category_feature": ["1", "2", "3"],
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
                    "category_feature": ["a", "b", "c"],
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
                    "category_feature": ["a", "b", "c"],
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
def test_data_drift_metrics_no_errors(
    current_dataset: pd.DataFrame, reference_dataset: pd.DataFrame, data_mapping: ColumnMapping
) -> None:
    report = Report(metrics=[DataDriftTable()])
    report.run(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_data_drift_metrics_value_error() -> None:
    test_data = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.nan, 1],
            "prediction": [1, np.nan, 1],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[DataDriftTable()])

    with pytest.raises(ValueError):
        report.run(current_data=test_data, reference_data=None, column_mapping=data_mapping)
        report.json()

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        report.run(current_data=None, reference_data=test_data, column_mapping=data_mapping)
        report.json()


def test_data_drift_metrics_with_options() -> None:
    current_dataset = pd.DataFrame(
        {
            "category_feature": ["a", "b", "a"],
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
    report = Report(metrics=[DataDriftTable(stattest_threshold=0.7)])
    report.run(current_data=current_dataset, reference_data=reference_dataset)
    assert report.show()
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "DataDriftTable"
    assert result["metrics"][0]["result"] == {
        "current_fi": None,
        "dataset_drift": False,
        "drift_by_columns": {
            "category_feature": {
                "column_name": "category_feature",
                "column_type": "cat",
                "drift_detected": False,
                "drift_score": 1.0,
                "stattest_name": "Z-test p_value",
                "stattest_threshold": 0.7,
                "current": {"small_distribution": {"x": ["a", "b"], "y": [2, 1]}},
                "reference": {"small_distribution": {"x": ["a", "b"], "y": [2, 1]}},
            },
            "prediction": {
                "column_name": "prediction",
                "column_type": "cat",
                "drift_detected": False,
                "drift_score": 1.0,
                "stattest_name": "Z-test p_value",
                "stattest_threshold": 0.7,
                "current": {"small_distribution": {"x": [0, 1], "y": [1, 2]}},
                "reference": {"small_distribution": {"x": [0, 1], "y": [1, 2]}},
            },
            "target": {
                "column_name": "target",
                "column_type": "cat",
                "drift_detected": True,
                "drift_score": 0.0,
                "stattest_name": "chi-square p_value",
                "stattest_threshold": 0.7,
                "current": {"small_distribution": {"x": [1, 2, 3, 4, 5], "y": [1, 1, 1, 0, 0]}},
                "reference": {"small_distribution": {"x": [1, 2, 3, 4, 5], "y": [1, 0, 0, 1, 1]}},
            },
        },
        "number_of_columns": 3,
        "number_of_drifted_columns": 1,
        "reference_fi": None,
        "share_of_drifted_columns": 0.3333333333333333,
    }


def test_data_drift_metrics_json_output() -> None:
    current_dataset = pd.DataFrame(
        {
            "category_feature": ["a", "b", "a", np.nan],
            "target": [np.nan, np.nan, 3, 4],
            "prediction": [1, 0, np.nan, 5],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "category_feature": ["a", "a", "b", "b"],
            "target": [1, 4, 5, 5],
            "prediction": [1, 5, 4, 4],
        }
    )
    report = Report(metrics=[DataDriftTable(stattest_threshold=0.7)])
    report.run(current_data=current_dataset, reference_data=reference_dataset)
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "DataDriftTable"
    assert result["metrics"][0]["result"] == {
        "current_fi": None,
        "dataset_drift": True,
        "drift_by_columns": {
            "category_feature": {
                "column_name": "category_feature",
                "column_type": "cat",
                "drift_detected": True,
                "drift_score": approx(0.66, abs=0.01),
                "stattest_name": "Z-test p_value",
                "stattest_threshold": 0.7,
                "current": {"small_distribution": {"x": ["a", "b"], "y": [2, 1]}},
                "reference": {"small_distribution": {"x": ["a", "b"], "y": [2, 2]}},
            },
            "prediction": {
                "column_name": "prediction",
                "column_type": "cat",
                "drift_detected": True,
                "drift_score": 0.0,
                "stattest_name": "chi-square p_value",
                "stattest_threshold": 0.7,
                "current": {"small_distribution": {"x": [0.0, 1.0, 4.0, 5.0], "y": [1, 1, 0, 1]}},
                "reference": {"small_distribution": {"x": [0, 1, 4, 5], "y": [0, 1, 2, 1]}},
            },
            "target": {
                "column_name": "target",
                "column_type": "cat",
                "drift_detected": True,
                "drift_score": 0.0,
                "stattest_name": "chi-square p_value",
                "stattest_threshold": 0.7,
                "current": {"small_distribution": {"x": [1.0, 3.0, 4.0, 5.0], "y": [0, 1, 1, 0]}},
                "reference": {"small_distribution": {"x": [1, 3, 4, 5], "y": [1, 0, 1, 2]}},
            },
        },
        "number_of_columns": 3,
        "number_of_drifted_columns": 3,
        "reference_fi": None,
        "share_of_drifted_columns": 1,
    }
