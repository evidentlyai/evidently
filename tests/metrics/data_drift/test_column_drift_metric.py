from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.metrics import ColumnDriftMetric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, data_mapping, metric",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDriftMetric(column_name="col"),
        ),
    ),
)
def test_column_drift_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: ColumnDriftMetric,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    assert report.json()
    assert report.show()


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
