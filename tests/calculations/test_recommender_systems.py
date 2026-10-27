import pandas as pd
import pytest

from evidently.legacy.calculations.recommender_systems import collect_dataset
from evidently.legacy.pipeline.column_mapping import RecomType


@pytest.mark.parametrize(
    "scores, expected",
    [
        ([0.5, 0.5, 0.5], [1, 2, 3]),
        ([0.9, 0.9, 0.1], [1, 2, 3]),
        ([0.5, 0.9, 0.5], [2, 1, 3]),
        ([0.1, 0.9, 0.5], [3, 1, 2]),
    ],
)
def test_score_ranks_break_ties_in_row_order(scores, expected):
    data = pd.DataFrame({"user": ["a"] * 3, "target": [0, 1, 1], "score": scores}, index=[8, 2, 5])
    original = data.copy(deep=True)
    result = collect_dataset(data.user, data.target, data.score, RecomType.SCORE, None, True, True)

    assert result.preds.tolist() == expected
    for k in (1, 2, 3):
        assert (result.preds <= k).sum() == k
    pd.testing.assert_frame_equal(data, original)


@pytest.mark.parametrize("recommendations_type", [RecomType.SCORE, RecomType.RANK])
def test_ranks_are_per_user_and_preserve_explicit_ranks(recommendations_type):
    data = pd.DataFrame(
        {"user": ["a", "b", "a", "c", "b", "a"], "target": [0, 1, 1, 1, 0, 0]},
        index=[4, 4, 2, 9, 1, 2],
    )
    expected = [1, 1, 2, 1, 2, 3] if recommendations_type == RecomType.SCORE else [3, 2, 1, 1, 1, 2]
    data["score"] = [0.5] * len(data) if recommendations_type == RecomType.SCORE else expected
    original = data.copy(deep=True)
    result = collect_dataset(data.user, data.target, data.score, recommendations_type, None, True, True)

    assert result.preds.tolist() == expected
    assert result.index.tolist() == data.index.tolist()
    for user, group in result.groupby("users"):
        for k in (1, 2, 3, 4):
            assert (group.preds <= k).sum() == min(k, len(group)), user
    pd.testing.assert_frame_equal(data, original)
