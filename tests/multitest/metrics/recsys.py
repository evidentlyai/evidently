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
        fingerprint="b12df34b6f19df9fcc5e6afafa22cf72",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def hit_rate_k_metric():
    return TestMetric(
        name="hit_rate_k_metric",
        metric=HitRateKMetric(k=3),
        fingerprint="db4ba352ec4ee25ce6e17064ffc88db3",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mrr_k_metric():
    return TestMetric(
        name="mrr_k_metric",
        metric=MRRKMetric(k=3),
        fingerprint="15101d7e1bc4c297ea73110eb00a5849",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def score_distribution():
    return TestMetric(
        name="score_distribution",
        metric=ScoreDistribution(k=3),
        fingerprint="2494b8495a3eeab169b922e6ea8cb7aa",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def f_beta_top_k():
    return TestMetric(
        name="f_beta_top_k",
        metric=FBetaTopKMetric(3),
        fingerprint="bd6bb194dd86ecb67069817dcee845ee",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_recall_calc():
    return TestMetric(
        name="precision_recall_calc",
        metric=PrecisionRecallCalculation(3),
        fingerprint="92213c8d5452e770e015d3487bd5dfa8",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def precision_top_k():
    return TestMetric(
        name="precision_top_k",
        metric=PrecisionTopKMetric(3),
        fingerprint="8a0240c04f778a84da2656a7e784c36e",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def recall_top_k():
    return TestMetric(
        name="recall_top_k",
        metric=RecallTopKMetric(3),
        fingerprint="c92e94241c1d58b49c2702edd682249a",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def map_k():
    return TestMetric(
        name="map_k",
        metric=MAPKMetric(3),
        fingerprint="9c57cf03761e3c0610345d3534ba8781",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def mar_k():
    return TestMetric(
        name="mar_k",
        metric=MARKMetric(3),
        fingerprint="5008d095662d6afdc234a1089ac29c5c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def ndcg():
    return TestMetric(
        name="ndcg",
        metric=NDCGKMetric(3),
        fingerprint="b23a1cc4f7ac59b81485fb6433afc54f",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def novelty():
    return TestMetric(
        name="novelty",
        metric=NoveltyMetric(k=3),
        fingerprint="0d8c3ff282f94cceb6184d4498b3d58f",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def pairwise_distance():
    return TestMetric(
        name="pairwise_distance",
        metric=PairwiseDistance(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="44070af355ca7e2cd18c1365226905e5",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def serendipity():
    return TestMetric(
        name="serendipity",
        metric=SerendipityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="2bfda8355c729f8ae0637b1d0f4d8246",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def personalization():
    return TestMetric(
        name="personalization",
        metric=PersonalizationMetric(k=3),
        fingerprint="692fa2b63855dde3054c193bdf461f16",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def popularity_bias():
    return TestMetric(
        name="popularity_bias",
        metric=PopularityBias(k=3),
        fingerprint="bf50156f95be7f38dccb2e975945bacb",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def train_stats():
    return TestMetric(
        name="train_stats",
        metric=TrainStats(),
        fingerprint="44febf74f2dbbb1ddc9c9f9c8c220fd6",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def user_bias():
    return TestMetric(
        name="user_bias",
        metric=UserBiasMetric(column_name="feature_1"),
        fingerprint="4f8880eebd359faf2c74c89fdd5a0242",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def item_bias():
    return TestMetric(
        name="item_bias",
        metric=ItemBiasMetric(k=3, column_name="feature_1"),
        fingerprint="0e3c204c5bb31fc109e45efe53ae03f7",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )


@metric
def diversity_bias():
    return TestMetric(
        name="diversity",
        metric=DiversityMetric(k=3, item_features=["feature_1", "feature_2"]),
        fingerprint="bb2ec1d0e2be57375a903bb3f49a46ab",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.RECSYS],
    )
