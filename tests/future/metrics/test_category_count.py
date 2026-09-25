import pandas as pd
import pytest

from evidently.core.datasets import Dataset
from evidently.core.metric_types import CountValue
from evidently.core.report import Report
from evidently.metrics import CategoryCount


@pytest.mark.parametrize(
    "data,categories,expected_count,expected_share",
    [
        (["a", "b", "c", "a"], ["a", "b"], 3, 0.75),
        (["a", "b", "c", "a"], ["a", "z"], 2, 0.5),
        ([True, True, False, False], [True], 2, 0.5),
        ([True, True, False, False], [True, False], 4, 1.0),
        ([True, True, False, None], [False, True], 3, 1.0),
        ([True, True, True], [True, False], 3, 1.0),
    ],
)
def test_category_count_multiple_categories(data, categories, expected_count, expected_share):
    dataset = Dataset.from_pandas(pd.DataFrame(data=dict(column=data)))
    metric = CategoryCount("column", categories=categories)
    snapshot = Report([metric]).run(dataset, None)
    metric_result = snapshot._context.get_metric_result(metric.metric_id)
    assert isinstance(metric_result, CountValue)
    assert metric_result.count.value == expected_count
    assert metric_result.share.value == pytest.approx(expected_share)
