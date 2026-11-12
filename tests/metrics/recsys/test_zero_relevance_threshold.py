import math

import pandas as pd
import pytest

from evidently.legacy.calculations.recommender_systems import collect_dataset
from evidently.legacy.metrics import HitRateKMetric
from evidently.legacy.metrics import MRRKMetric
from evidently.legacy.metrics import NDCGKMetric
from evidently.legacy.metrics import PrecisionTopKMetric
from evidently.legacy.metrics import RecallTopKMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def _data(recommendations_type=RecomType.RANK):
    return pd.DataFrame(
        {
            "user_id": ["a", "a", "b", "b", "c", "c"],
            "target": [0, -1, -1, 1, -1, -1],
            "prediction": [1, 2] * 3 if recommendations_type == RecomType.RANK else [0.9, 0.1] * 3,
        }
    )


@pytest.mark.parametrize("bin_data", [False, True])
@pytest.mark.parametrize("no_feedback_users", [False, True])
@pytest.mark.parametrize(
    "threshold,expected_targets,feedback_users",
    [
        (0, [1, 0, 0, 1, 0, 0], ["a", "b"]),
        (-1, [1, 1, 1, 1, 1, 1], ["a", "b", "c"]),
        (1, [0, 0, 0, 1, 0, 0], ["b"]),
        (None, [0, -1, -1, 1, -1, -1], ["b"]),
    ],
)
def test_relevance_threshold_applies_before_binarizing_and_filtering_users(
    threshold, expected_targets, feedback_users, no_feedback_users, bin_data
):
    data = _data()
    original = data.copy(deep=True)

    result = collect_dataset(
        data.user_id,
        data.target,
        data.prediction,
        RecomType.RANK,
        threshold,
        no_feedback_users,
        bin_data,
    )

    expected = data.rename(columns={"user_id": "users", "prediction": "preds"})
    expected["target"] = expected_targets
    if threshold is None and bin_data:
        expected["target"] = [0, 0, 0, 1, 0, 0]
    if not no_feedback_users:
        expected = expected[expected.users.isin(feedback_users)]
    pd.testing.assert_frame_equal(result, expected)
    pd.testing.assert_frame_equal(data, original)


@pytest.mark.parametrize("recommendations_type", [RecomType.RANK, RecomType.SCORE])
@pytest.mark.parametrize("no_feedback_users", [False, True])
def test_zero_threshold_report_counts_zero_rated_items_as_relevant(recommendations_type, no_feedback_users):
    data = _data(recommendations_type)
    metrics = [
        PrecisionTopKMetric(k=1, min_rel_score=0, no_feedback_users=no_feedback_users),
        RecallTopKMetric(k=1, min_rel_score=0, no_feedback_users=no_feedback_users),
        HitRateKMetric(k=1, min_rel_score=0, no_feedback_users=no_feedback_users),
        MRRKMetric(k=2, min_rel_score=0, no_feedback_users=no_feedback_users),
        NDCGKMetric(k=2, min_rel_score=0, no_feedback_users=no_feedback_users),
    ]
    report = Report(metrics=metrics)

    report.run(
        current_data=data,
        reference_data=data.copy(),
        column_mapping=ColumnMapping(recommendations_type=recommendations_type),
    )

    # User a has its relevant item first; user b has it second. User c has none.
    user_count = 3 if no_feedback_users else 2
    expected = [1 / user_count] * 3 + [1.5 / user_count, (1 + 1 / math.log2(3)) / user_count]
    for metric, value in zip(metrics, expected):
        result = metric.get_result()
        assert result.current.iloc[metric.k - 1] == pytest.approx(value)
        assert result.reference.iloc[metric.k - 1] == pytest.approx(value)
