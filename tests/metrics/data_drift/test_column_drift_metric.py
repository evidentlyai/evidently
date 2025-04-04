from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculation_engine.python_engine import PythonEngine
from evidently.legacy.calculations.stattests import StatTest
from evidently.legacy.calculations.stattests import psi_stat_test
from evidently.legacy.calculations.stattests.registry import _impls
from evidently.legacy.calculations.stattests.registry import add_stattest_impl
from evidently.legacy.core import ColumnType
from evidently.legacy.metrics import ColumnDriftMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report

test_stattest = StatTest(
    name="test_stattest",
    display_name="test stattest",
    allowed_feature_types=[ColumnType.Numerical],
    default_threshold=0.05,
)

add_stattest_impl(test_stattest, PythonEngine, _impls[psi_stat_test][PythonEngine])


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
