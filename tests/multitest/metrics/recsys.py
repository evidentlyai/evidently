from evidently.legacy.metrics.recsys.diversity import DiversityMetric
from evidently.legacy.metrics.recsys.f_beta_top_k import FBetaTopKMetric
from evidently.legacy.metrics.recsys.hit_rate_k import HitRateKMetric
from evidently.legacy.metrics.recsys.item_bias import ItemBiasMetric
from evidently.legacy.metrics.recsys.map_k import MAPKMetric
from evidently.legacy.metrics.recsys.mar_k import MARKMetric
from evidently.legacy.metrics.recsys.mrr import MRRKMetric
from evidently.legacy.metrics.recsys.ndcg_k import NDCGKMetric
from evidently.legacy.metrics.recsys.novelty import NoveltyMetric
from evidently.legacy.metrics.recsys.pairwise_distance import PairwiseDistance
from evidently.legacy.metrics.recsys.personalisation import PersonalizationMetric
from evidently.legacy.metrics.recsys.popularity_bias import PopularityBias
from evidently.legacy.metrics.recsys.precision_recall_k import PrecisionRecallCalculation
from evidently.legacy.metrics.recsys.precision_top_k import PrecisionTopKMetric
from evidently.legacy.metrics.recsys.rec_examples import RecCasesTable
from evidently.legacy.metrics.recsys.recall_top_k import RecallTopKMetric
from evidently.legacy.metrics.recsys.scores_distribution import ScoreDistribution
from evidently.legacy.metrics.recsys.serendipity import SerendipityMetric
from evidently.legacy.metrics.recsys.train_stats import TrainStats
from evidently.legacy.metrics.recsys.user_bias import UserBiasMetric
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def rec_cases_table():
    return TestMetric(
        name="rec_cases_table",
        metric=RecCasesTable(),
        fingerprint="a2c6bcd798b614ca2feb3a1af1bc6401",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def hit_rate_k_metric():
    return TestMetric(
        name="hit_rate_k_metric",
        metric=HitRateKMetric(k=3),
        fingerprint="95b3ffcf9690c0460e15d3d757f55490",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mrr_k_metric():
    return TestMetric(
        name="mrr_k_metric",
        metric=MRRKMetric(k=3),
        fingerprint="4fd63e982f25c21a634d25b4738936cf",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def score_distribution():
    return TestMetric(
        name="score_distribution",
        metric=ScoreDistribution(k=3),
        fingerprint="f17c85595a80a881bb2b8208ca3154e2",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def f_beta_top_k():
    return TestMetric(
        name="f_beta_top_k",
        metric=FBetaTopKMetric(3),
        fingerprint="8b76ec9a9bf30983cdc230f4d9253d80",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_recall_calc():
    return TestMetric(
        name="precision_recall_calc",
        metric=PrecisionRecallCalculation(3),
        fingerprint="f982a844e76b1a4673b62c61794de866",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_top_k():
    return TestMetric(
        name="precision_top_k",
        metric=PrecisionTopKMetric(3),
        fingerprint="a85a3a7c6140bb85f6ee8bdb46b71d9c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def recall_top_k():
    return TestMetric(
        name="recall_top_k",
        metric=RecallTopKMetric(3),
        fingerprint="86897f39c844d140a99a514b8ea17fe1",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def map_k():
    return TestMetric(
        name="map_k",
        metric=MAPKMetric(3),
        fingerprint="66e5ba8afccdbd3a67e796484fc40b74",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mar_k():
    return TestMetric(
        name="mar_k",
        metric=MARKMetric(3),
        fingerprint="1aea4a4c81bc95522233e8ee1f62a6ec",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def ndcg():
    return TestMetric(
        name="ndcg",
        metric=NDCGKMetric(3),
        fingerprint="9d5a1e94740388eb3d0755f05ef7dda1",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def novelty():
    return TestMetric(
        name="novelty",
        metric=NoveltyMetric(k=3),
        fingerprint="044733335050b4248b55f62597635c36",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def pairwise_distance():
    return TestMetric(
        name="pairwise_distance",
        metric=PairwiseDistance(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="e557fc4d799a2ad49abb8c1d666b454f",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def serendipity():
    return TestMetric(
        name="serendipity",
        metric=SerendipityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="ed7e0457899c3fb536b28acf4d582d6d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def personalization():
    return TestMetric(
        name="personalization",
        metric=PersonalizationMetric(k=3),
        fingerprint="f73a8464f74068c40dbb6adf35b9ede1",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def popularity_bias():
    return TestMetric(
        name="popularity_bias",
        metric=PopularityBias(k=3),
        fingerprint="fb8c86c8e3b0235bc0be86f470f4c4d7",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def train_stats():
    return TestMetric(
        name="train_stats",
        metric=TrainStats(),
        fingerprint="a6ca927a9ab136c097125117fa03c932",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def user_bias():
    return TestMetric(
        name="user_bias",
        metric=UserBiasMetric(column_name="feature_1"),
        fingerprint="266bfb05c179d6dff9981ad6d26444ae",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def item_bias():
    return TestMetric(
        name="item_bias",
        metric=ItemBiasMetric(k=3, column_name="feature_1"),
        fingerprint="04534fefcee85e3287ed86e890e31967",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def diversity_bias():
    return TestMetric(
        name="diversity",
        metric=DiversityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="395fd112bdae7587b741d4cb20fed72a",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )
