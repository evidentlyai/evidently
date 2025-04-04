import numpy as np
import pandas as pd
import pytest

from evidently.core.datasets import Dataset
from evidently.core.metric_types import CountValue
from evidently.core.report import Report
from evidently.metrics import DatasetMissingValueCount


@pytest.mark.parametrize(
    "data,metric,result",
    [(pd.DataFrame({"a": [1, 2, np.nan, np.nan]}), DatasetMissingValueCount(), {"count": 2, "share": 0.5})],
)
def test_missing_count(data, metric, result):
    dataset = Dataset.from_pandas(data)
    report = Report([metric])
    run = report.run(dataset, None)
    res = run._context.get_metric_result(metric)
    assert isinstance(res, CountValue)
    assert res.count.value == result["count"]
    assert res.share.value == result["share"]
