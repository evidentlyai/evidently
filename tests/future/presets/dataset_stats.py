import pandas as pd
import pytest

from evidently.future.datasets import DataDefinition
from evidently.future.datasets import Dataset
from evidently.future.presets import ValueStats
from evidently.future.report import Report


@pytest.mark.parametrize(
    "dataset,column,expected_metric_count",
    [
        (
            Dataset.from_pandas(
                pd.DataFrame(data=dict(column=[1, 1, 1, 1, 0])),
                data_definition=DataDefinition(categorical_columns=["column"]),
            ),
            "column",
            3,
        ),
    ],
)
def test_value_stats(dataset, column, expected_metric_count):
    report = Report([ValueStats(column=column)])
    snapshot = report.run(dataset, None)
    assert len(snapshot.dict()["metrics"]) == expected_metric_count
