import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.calculations.stattests import StatTest
from evidently.calculations.stattests import psi_stat_test
from evidently.metrics import ColumnDriftMetric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report

test_stattest = StatTest(
    name="test_stattest",
    display_name="test stattest",
    func=psi_stat_test.func,
    allowed_feature_types=["num"],
    default_threshold=0.05,
)


@pytest.mark.parametrize(
    "current_data, reference_data, data_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
            {
                "column_name": "col",
                "column_type": "num",
                "drift_detected": False,
                "drift_score": 1.0,
                "stattest_name": "chi-square p_value",
                "stattest_threshold": 0.05,
            },
        ),
        (
            pd.DataFrame({"col": [5, 8, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
            {
                "column_name": "col",
                "column_type": "num",
                "drift_detected": True,
                "drift_score": 0.0,
                "stattest_name": "chi-square p_value",
                "stattest_threshold": 0.05,
            },
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [3, 2, 2]}),
            None,
            ColumnDriftMetric(column_name="col", stattest="psi", stattest_threshold=0.1),
            {
                "column_name": "col",
                "column_type": "num",
                "drift_detected": True,
                "drift_score": approx(2.93, abs=0.01),
                "stattest_name": "PSI",
                "stattest_threshold": 0.1,
            },
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [3, 2, 2]}),
            None,
            ColumnDriftMetric(column_name="col", stattest=test_stattest, stattest_threshold=0.1),
            {
                "column_name": "col",
                "column_type": "num",
                "drift_detected": True,
                "drift_score": approx(2.93, abs=0.01),
                "stattest_name": "test stattest",
                "stattest_threshold": 0.1,
            },
        ),
    ),
)
def test_column_drift_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: ColumnDriftMetric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    assert report.show()
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "ColumnDriftMetric"
    assert result["metrics"][0]["result"] == expected_json


@pytest.mark.parametrize(
    "current_data, reference_data, data_mapping, metric, expected_error",
    (
        # no reference dataset
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            None,
            ColumnDriftMetric(column_name="col"),
            "Reference dataset should be present",
        ),
        # no column in reference dataset
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
            "Cannot find column 'col' in current dataset",
        ),
        # no column in current dataset
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
            "Cannot find column 'col' in reference dataset",
        ),
        # no meaningful values in the column in current
        (
            pd.DataFrame({"col": [None, np.inf, -np.inf]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
            "An empty column 'col' was provided for drift calculation in the current dataset.",
        ),
        # no meaningful values in the column in reference
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [None, np.inf, -np.inf]}),
            None,
            ColumnDriftMetric(column_name="col"),
            "An empty column 'col' was provided for drift calculation in the reference dataset.",
        ),
    ),
)
def test_column_drift_metric_errors(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: ColumnDriftMetric,
    expected_error: str,
) -> None:
    report = Report(metrics=[metric])

    with pytest.raises(ValueError, match=expected_error):
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
        report.json()
