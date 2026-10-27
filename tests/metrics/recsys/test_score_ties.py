import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy import metrics
from evidently.legacy.metrics.recsys.pairwise_distance import PairwiseDistance
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report
from evidently.legacy.utils import NumpyEncoder


@pytest.fixture
def tied_data():
    # Interleaved users and reversed reference rows make the two rankings independent.
    current = pd.DataFrame(
        {
            "user_id": ["a", "b", "a", "b", "a", "b"],
            "item_id": [0, 2, 1, 3, 2, 4],
            "prediction": [0.5] * 6,
            "target": [1, 0, 0, 1, 1, 1],
            "feature": [1, 3, 2, 4, 3, 5],
            "other_feature": [5, 3, 4, 2, 3, 1],
        },
        index=[9, 1, 6, 3, 2, 5],
    )
    return current, current.iloc[::-1].copy()


@pytest.mark.parametrize(
    "metric_type, kwargs",
    [
        (metrics.PrecisionTopKMetric, {}),
        (metrics.RecallTopKMetric, {}),
        (metrics.FBetaTopKMetric, {}),
        (metrics.MAPKMetric, {}),
        (metrics.MARKMetric, {}),
        (metrics.HitRateKMetric, {}),
        (metrics.MRRKMetric, {}),
        (metrics.NDCGKMetric, {}),
        (metrics.DiversityMetric, {"item_features": ["feature", "other_feature"]}),
        (metrics.NoveltyMetric, {}),
        (metrics.SerendipityMetric, {"item_features": ["feature", "other_feature"]}),
        (metrics.PersonalizationMetric, {}),
        (metrics.PopularityBias, {}),
        (metrics.ItemBiasMetric, {"column_name": "feature"}),
    ],
)
@pytest.mark.parametrize("k", [1, 2])
def test_score_metrics_match_explicit_stable_ranks(tied_data, metric_type, kwargs, k):
    current, reference = tied_data
    originals = [df.copy(deep=True) for df in tied_data]
    results = []
    for recommendations_type in (RecomType.SCORE, RecomType.RANK):
        frames = [df.copy(deep=True) for df in tied_data]
        if recommendations_type == RecomType.RANK:
            for df in frames:
                df["prediction"] = [1, 1, 2, 2, 3, 3]
        frame_copies = [df.copy(deep=True) for df in frames]
        metric = metric_type(k=k, **kwargs)
        Report(metrics=[metric]).run(
            current_data=frames[0],
            reference_data=frames[1],
            column_mapping=ColumnMapping(recommendations_type=recommendations_type),
            additional_data={"current_train_data": current, "reference_train_data": reference},
        )
        results.append(metric.get_result())
        for actual, original in zip(frames, frame_copies):
            pd.testing.assert_frame_equal(actual, original)

    # Serialization includes the per-K curves, distributions and current/reference values.
    assert json.dumps(results[0].dict(), cls=NumpyEncoder, sort_keys=True) == json.dumps(
        results[1].dict(), cls=NumpyEncoder, sort_keys=True
    )
    for actual, original in zip(tied_data, originals):
        pd.testing.assert_frame_equal(actual, original)


@pytest.mark.parametrize("include_reference", [False, True])
@pytest.mark.parametrize("recommendations_type", [RecomType.SCORE, RecomType.RANK])
def test_pairwise_candidates_include_each_dataset_top_k(tied_data, include_reference, recommendations_type):
    current, reference = [df.copy(deep=True) for df in tied_data]
    if recommendations_type == RecomType.RANK:
        current["prediction"] = [1, 1, 2, 2, 3, 3]
        reference["prediction"] = [1, 1, 2, 2, 3, 3]
    originals = [df.copy(deep=True) for df in (current, reference)]
    metric = PairwiseDistance(k=1, item_features=["feature", "other_feature"])
    Report(metrics=[metric]).run(
        current_data=current,
        reference_data=reference if include_reference else None,
        column_mapping=ColumnMapping(recommendations_type=recommendations_type),
    )
    # The distance cache takes k+1 candidates per user from each dataset.
    assert set(metric.get_result().name_dict) == ({0, 1, 2, 3, 4} if include_reference else {0, 1, 2, 3})
    for actual, original in zip((current, reference), originals):
        pd.testing.assert_frame_equal(actual, original)


@pytest.mark.parametrize("k", [1, 2])
def test_score_distribution_selects_exactly_k_per_user(tied_data, k):
    current, reference = tied_data
    originals = [df.copy(deep=True) for df in tied_data]
    metric = metrics.ScoreDistribution(k=k)
    Report(metrics=[metric]).run(
        current_data=current,
        reference_data=reference,
        column_mapping=ColumnMapping(recommendations_type=RecomType.SCORE),
    )
    result = metric.get_result()
    for prefix in ("current", "reference"):
        assert sum(getattr(result, prefix + "_top_k_distr").y) == 2 * k
        assert sum(getattr(result, prefix + "_other_distr").y) == 2 * (3 - k)
        assert getattr(result, prefix + "_entropy") == pytest.approx(np.log(2 * k))
    for actual, original in zip(tied_data, originals):
        pd.testing.assert_frame_equal(actual, original)


@pytest.mark.parametrize(
    "scores, current_items, reference_items",
    [
        ([0.5] * 20, [0, 1, 2], [19, 18, 17]),
        ([0.5, 0.9, 0.5, 0.1] * 5, [1, 5, 9], [17, 13, 9]),
    ],
)
def test_recommendation_examples_use_the_same_score_tie_order(scores, current_items, reference_items):
    current = pd.DataFrame(
        {
            "user_id": ["a", "b"] * 20,
            "item_id": [i + offset for i in range(20) for offset in (0, 100)],
            "prediction": np.repeat(scores, 2),
        },
        index=range(39, -1, -1),
    )
    reference = current.iloc[::-1].copy()
    originals = [df.copy(deep=True) for df in (current, reference)]
    metric = metrics.RecCasesTable(user_ids=["a", "b"], item_num=3)
    Report(metrics=[metric]).run(
        current_data=current,
        reference_data=reference,
        column_mapping=ColumnMapping(recommendations_type=RecomType.SCORE),
    )
    result = metric.get_result()
    for user, offset in (("a", 0), ("b", 100)):
        assert result.current[user].item_id.tolist() == [str(i + offset) for i in current_items]
        assert result.reference[user].item_id.tolist() == [str(i + offset) for i in reference_items]
    for actual, original in zip((current, reference), originals):
        pd.testing.assert_frame_equal(actual, original)
