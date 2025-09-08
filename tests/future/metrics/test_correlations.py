import pandas as pd

from evidently import Dataset
from evidently import Report
from evidently.core.metric_types import DataframeValue
from evidently.metrics import ColumnCorrelations


def test_column_correlations():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    ds = Dataset.from_pandas(df)

    metric = ColumnCorrelations(column_name="a")
    report = Report(metrics=[metric])

    run = report.run(ds)

    result = run.context.get_metric_result(metric)
    assert isinstance(result, DataframeValue)
    pd.testing.assert_frame_equal(result.value, pd.DataFrame([{"kind": "cramer_v", "column_name": "b", "value": 1.0}]))
