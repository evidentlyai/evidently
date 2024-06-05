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
        fingerprint="44eafc04aec9383112d84c00336f85bd",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def hit_rate_k_metric():
    return TestMetric(
        name="hit_rate_k_metric",
        metric=HitRateKMetric(k=3),
        fingerprint="d8fa4cc38ab8186761466a721da37dd8",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mrr_k_metric():
    return TestMetric(
        name="mrr_k_metric",
        metric=MRRKMetric(k=3),
        fingerprint="4f2f417258da3d4903ace38be8f3a6e7",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def score_distribution():
    return TestMetric(
        name="score_distribution",
        metric=ScoreDistribution(k=3),
        fingerprint="3140f96ff8783bb20962250e922c5c90",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def f_beta_top_k():
    return TestMetric(
        name="f_beta_top_k",
        metric=FBetaTopKMetric(3),
        fingerprint="04c9d41016f1fa7c01a12c121c3df025",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_recall_calc():
    return TestMetric(
        name="precision_recall_calc",
        metric=PrecisionRecallCalculation(3),
        fingerprint="6f41fd746f06fdd1889144765c0b676d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_top_k():
    return TestMetric(
        name="precision_top_k",
        metric=PrecisionTopKMetric(3),
        fingerprint="e7f79adaf7299d33183dafd87a6ecaef",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def recall_top_k():
    return TestMetric(
        name="recall_top_k",
        metric=RecallTopKMetric(3),
        fingerprint="68cdfee1c3b35ea5a1d120bf7afb4edc",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def map_k():
    return TestMetric(
        name="map_k",
        metric=MAPKMetric(3),
        fingerprint="41d43e8d7e0db237da914e87e9473663",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mar_k():
    return TestMetric(
        name="mar_k",
        metric=MARKMetric(3),
        fingerprint="9cb5f219a450bbbba19431075ac06c49",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def ndcg():
    return TestMetric(
        name="ndcg",
        metric=NDCGKMetric(3),
        fingerprint="6596e75b036e10a6d4c267d713915786",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def novelty():
    return TestMetric(
        name="novelty",
        metric=NoveltyMetric(k=3),
        fingerprint="7d2d2d71db346238f88512b2fec7ca48",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def pairwise_distance():
    return TestMetric(
        name="pairwise_distance",
        metric=PairwiseDistance(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="5b556a55e64275074963c5b14ef7fb69",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def serendipity():
    return TestMetric(
        name="serendipity",
        metric=SerendipityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="db3c99c694321a6ce0d3d488d7e12513",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def personalization():
    return TestMetric(
        name="personalization",
        metric=PersonalizationMetric(k=3),
        fingerprint="8041b8216dcf1a60978a8bad4d47d37c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def popularity_bias():
    return TestMetric(
        name="popularity_bias",
        metric=PopularityBias(k=3),
        fingerprint="284e5b0bcf8d753100ce85158ac4c4b4",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def train_stats():
    return TestMetric(
        name="train_stats",
        metric=TrainStats(),
        fingerprint="f1fac5fef69a38c045460c5bb8412c1d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def user_bias():
    return TestMetric(
        name="user_bias",
        metric=UserBiasMetric(column_name="feature_1"),
        fingerprint="1f4df2ac6cbe2db99ead087a5a4a632c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def item_bias():
    return TestMetric(
        name="item_bias",
        metric=ItemBiasMetric(k=3, column_name="feature_1"),
        fingerprint="69491170c389588095c8a24d47b66f29",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def diversity_bias():
    return TestMetric(
        name="diversity",
        metric=DiversityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="91786e415edff87e4038f77b3b88a3c4",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )
