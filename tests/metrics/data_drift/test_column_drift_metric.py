import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.metrics import ColumnDriftMetric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


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
                "threshold": 0.05,
            },
        ),
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
                "threshold": 0.05,
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
    "current_data, reference_data, data_mapping, metric",
    (
        # no reference dataset
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            None,
            ColumnDriftMetric(column_name="col"),
        ),
        # no column in reference dataset
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
        ),
        # no column in current dataset
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
        ),
        # no not-nan values in the column
        (
            pd.DataFrame({"col": [None, np.inf, -np.inf]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
        ),
    ),
)
def test_column_drift_metric_errors(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: ColumnDriftMetric,
) -> None:
    report = Report(metrics=[metric])

    with pytest.raises(ValueError):
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
        report.json()
