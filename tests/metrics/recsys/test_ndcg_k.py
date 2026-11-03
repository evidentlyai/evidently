import math

import pandas as pd
import pytest

from evidently.legacy.metrics import NDCGKMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_ndcg_values():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = NDCGKMetric(k=2)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[1] == 0.5
    assert results.current[2] == 0.5
    assert results.current[3] == 0.75


def test_ndcg_scores():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = NDCGKMetric(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[1] == 0.5
    assert results.current[2] == 0.5
    assert results.current[3] == 0.75


@pytest.mark.parametrize(
    "index",
    [
        pd.RangeIndex(5),
        pd.Index([0.5, 1.5, 2.5, 3.5, 4.5]),
        pd.Index([6.0, 0.0, 3.0, 0.0, 3.0]),
        pd.Index([8, 2, 9, 2, 8], name="row"),
        pd.Index(["e", "a", "d", "b", "c"]),
    ],
    ids=["range", "float", "duplicate-float", "duplicate-integer", "string"],
)
@pytest.mark.parametrize("recommendations_type", [RecomType.SCORE, RecomType.RANK])
def test_ndcg_ideal_ranking_uses_positions(index, recommendations_type):
    current = pd.DataFrame(
        {
            "user_id": ["a", "a", "a", "b", "b"],
            "target": [0, 3, 1, 2, 0],
            "prediction": [0.9, 0.8, 0.7, 0.9, 0.8] if recommendations_type == RecomType.SCORE else [1, 2, 3, 1, 2],
        },
        index=index,
    )
    before = current.copy(deep=True)
    metric = NDCGKMetric(k=3)
    report = Report(metrics=[metric])
    report.run(
        current_data=current,
        reference_data=current.copy(deep=True),
        column_mapping=ColumnMapping(recommendations_type=recommendations_type),
    )

    # User b has an ideal ranking. User a's ideal relevance order is [3, 1, 0].
    discount = 1 / math.log2(3)
    ideal = 3 + discount
    expected = pd.Series([0.5, (3 * discount / ideal + 1) / 2, ((3 * discount + 0.5) / ideal + 1) / 2], index=[1, 2, 3])
    result = metric.get_result()
    pd.testing.assert_series_equal(result.current, expected)
    pd.testing.assert_series_equal(result.reference, expected)
    pd.testing.assert_frame_equal(current, before)
