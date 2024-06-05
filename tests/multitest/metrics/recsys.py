from evidently.metrics.recsys.diversity import DiversityMetric
from evidently.metrics.recsys.f_beta_top_k import FBetaTopKMetric
from evidently.metrics.recsys.hit_rate_k import HitRateKMetric
from evidently.metrics.recsys.item_bias import ItemBiasMetric
from evidently.metrics.recsys.map_k import MAPKMetric
from evidently.metrics.recsys.mar_k import MARKMetric
from evidently.metrics.recsys.mrr import MRRKMetric
from evidently.metrics.recsys.ndcg_k import NDCGKMetric
from evidently.metrics.recsys.novelty import NoveltyMetric
from evidently.metrics.recsys.pairwise_distance import PairwiseDistance
from evidently.metrics.recsys.personalisation import PersonalizationMetric
from evidently.metrics.recsys.popularity_bias import PopularityBias
from evidently.metrics.recsys.precision_recall_k import PrecisionRecallCalculation
from evidently.metrics.recsys.precision_top_k import PrecisionTopKMetric
from evidently.metrics.recsys.rec_examples import RecCasesTable
from evidently.metrics.recsys.recall_top_k import RecallTopKMetric
from evidently.metrics.recsys.scores_distribution import ScoreDistribution
from evidently.metrics.recsys.serendipity import SerendipityMetric
from evidently.metrics.recsys.train_stats import TrainStats
from evidently.metrics.recsys.user_bias import UserBiasMetric
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def rec_cases_table():
    return TestMetric(
        name="rec_cases_table",
        metric=RecCasesTable(),
        fingerprint="234c05012bb41475e9bfaf7c8ff01266",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def hit_rate_k_metric():
    return TestMetric(
        name="hit_rate_k_metric",
        metric=HitRateKMetric(k=3),
        fingerprint="f32f93bb6017764e9edab3210dd5ed40",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mrr_k_metric():
    return TestMetric(
        name="mrr_k_metric",
        metric=MRRKMetric(k=3),
        fingerprint="30777887cbfe1f4fbe957d6826e53f88",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def score_distribution():
    return TestMetric(
        name="score_distribution",
        metric=ScoreDistribution(k=3),
        fingerprint="73cdbc96f84034610ab15da41eb64ba7",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def f_beta_top_k():
    return TestMetric(
        name="f_beta_top_k",
        metric=FBetaTopKMetric(3),
        fingerprint="c653392cd09d48a0f6279c7b9ae006e6",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_recall_calc():
    return TestMetric(
        name="precision_recall_calc",
        metric=PrecisionRecallCalculation(3),
        fingerprint="e85f92f2ef10fbbe7c201ef20da9ac62",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_top_k():
    return TestMetric(
        name="precision_top_k",
        metric=PrecisionTopKMetric(3),
        fingerprint="78ed2114805b22800a74b1f5a0f74a9d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def recall_top_k():
    return TestMetric(
        name="recall_top_k",
        metric=RecallTopKMetric(3),
        fingerprint="8f04c9b73e28d1afe0f61fb90f74dd34",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def map_k():
    return TestMetric(
        name="map_k",
        metric=MAPKMetric(3),
        fingerprint="0b308d0a0565058820a1f6b3c77f7527",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mar_k():
    return TestMetric(
        name="mar_k",
        metric=MARKMetric(3),
        fingerprint="3193ffd5a10a6dacf60a8b85206d1c22",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def ndcg():
    return TestMetric(
        name="ndcg",
        metric=NDCGKMetric(3),
        fingerprint="6ed8a484a7983f171c68b34cd2f881ff",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def novelty():
    return TestMetric(
        name="novelty",
        metric=NoveltyMetric(k=3),
        fingerprint="d8a4050e28087b83b47367a256e93596",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def pairwise_distance():
    return TestMetric(
        name="pairwise_distance",
        metric=PairwiseDistance(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="b626e2dd647e6025a30cefeaaf0e2369",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def serendipity():
    return TestMetric(
        name="serendipity",
        metric=SerendipityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="aa7a21afe21808c8fc0fa0d0e8c74cbb",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def personalization():
    return TestMetric(
        name="personalization",
        metric=PersonalizationMetric(k=3),
        fingerprint="7238e23ed6b2fec63e9dbfdd9c1b3ffc",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def popularity_bias():
    return TestMetric(
        name="popularity_bias",
        metric=PopularityBias(k=3),
        fingerprint="9aa0f47daca6f8fa8f70a0cb4f7e6d8c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def train_stats():
    return TestMetric(
        name="train_stats",
        metric=TrainStats(),
        fingerprint="baa0bab492bfa496febe7679e2f2add2",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def user_bias():
    return TestMetric(
        name="user_bias",
        metric=UserBiasMetric(column_name="feature_1"),
        fingerprint="1677725eda5bd97f16d9ec09bd2ffe90",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def item_bias():
    return TestMetric(
        name="item_bias",
        metric=ItemBiasMetric(k=3, column_name="feature_1"),
        fingerprint="482066fdc33e22c3718461fa7aba4706",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def diversity_bias():
    return TestMetric(
        name="diversity",
        metric=DiversityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="79ed7eb531e5c6e168653463e5c1fb29",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )
