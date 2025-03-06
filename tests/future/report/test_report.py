import pandas as pd
import pytest

from evidently.future.datasets import Dataset
from evidently.future.metrics import MinValue
from evidently.future.report import Report


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
    report = Report([MinValue(column="a")])

    snapshot = report.run(current_data=current, reference_data=reference)
    assert snapshot is not None
