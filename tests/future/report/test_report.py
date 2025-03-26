import pandas as pd
import pytest

from evidently.future.datasets import Dataset
from evidently.future.metrics import CategoryCount
from evidently.future.metrics import MinValue
from evidently.future.report import Report
from evidently.future.report import Snapshot
from evidently.future.tests import lt


@pytest.mark.parametrize(
    "current,reference",
    [
        (Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})), None),
        (
            Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})),
            Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})),
        ),
        (pd.DataFrame(data={"a": [1, 2, 3]}), None),
        (pd.DataFrame(data={"a": [1, 2, 3]}), pd.DataFrame(data={"a": [1, 2, 3]})),
        (Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})), pd.DataFrame(data={"a": [1, 2, 3]})),
        (pd.DataFrame(data={"a": [1, 2, 3]}), Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]}))),
    ],
)
def test_report_run(current, reference):
    report = Report(
        [
            MinValue(column="a", tests=[lt(1)]),
            CategoryCount(column="a", category=1),
        ]
    )

    snapshot = report.run(current_data=current, reference_data=reference)
    assert snapshot is not None

    data = snapshot.dumps()
    snapshot_2 = Snapshot.loads(data)
    assert snapshot_2 is not None
    assert snapshot.dumps() == snapshot_2.dumps()
    snapshot.json()
