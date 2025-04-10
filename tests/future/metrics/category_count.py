import pandas as pd
import pytest

from evidently.core.datasets import Dataset
from evidently.core.metric_types import CountValue
from evidently.core.report import Report
from evidently.metrics import CategoryCount


@pytest.mark.parametrize(
    "data,category,expected_count",
    [
        (["a", "a", "a"], "a", 3),
        (["a", "a", "a"], "b", 0),
        ([True, True, True], True, 3),
        ([True, True, True], False, 0),
        ([True, True, None], True, 2),
        ([True, True, None], False, 0),
        ([False, False, None], False, 2),
    ],
)
def test_category_count_metric(data, category, expected_count):
    dataset = Dataset.from_pandas(pd.DataFrame(data=dict(column=data)))
    metric = CategoryCount("column", category=category)
    report = Report([metric])
    snapshot = report.run(dataset, None)
    metric_result = snapshot._context.get_metric_result(metric.metric_id)
    assert isinstance(metric_result, CountValue)
    assert metric_result.count == expected_count
