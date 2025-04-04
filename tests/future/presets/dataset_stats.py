import numpy as np
import pandas as pd
import pytest

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.metric_types import ByLabelCountValue
from evidently.core.report import Report
from evidently.presets import ValueStats


@pytest.mark.parametrize(
    "dataset,preset,expected_metric_count,unique_result",
    [
        (
            Dataset.from_pandas(
                pd.DataFrame(data=dict(column=[1, 1, 1, 1, 0])),
                data_definition=DataDefinition(categorical_columns=["column"]),
            ),
            ValueStats(column="column"),
            3,
            None,
        ),
        (
            Dataset.from_pandas(
                pd.DataFrame(data=dict(column=["a", "b", np.nan])),
                data_definition=DataDefinition(categorical_columns=["column"]),
            ),
            ValueStats(column="column"),
            3,
            {"a": 1, "b": 1},
        ),
        (
            Dataset.from_pandas(
                pd.DataFrame(data=dict(column=["a", "b", np.nan])),
                data_definition=DataDefinition(categorical_columns=["column"]),
            ),
            ValueStats(column="column", replace_nan="aaaa"),
            3,
            {"a": 1, "b": 1, "aaaa": 1},
        ),
    ],
)
def test_value_stats(dataset, preset, expected_metric_count, unique_result):
    report = Report([preset])
    snapshot = report.run(dataset, None)
    assert len(snapshot.dict()["metrics"]) == expected_metric_count
    if unique_result is not None:
        ur = snapshot._context.get_metric_result(preset._categorical_unique_value_count_metric())
        assert isinstance(ur, ByLabelCountValue)
        ur_counts = {k: v.value for k, v in ur.counts.items()}
        assert ur_counts == unique_result
