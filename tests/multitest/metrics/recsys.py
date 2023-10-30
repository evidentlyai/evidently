from evidently.metrics.recsys.diversity import DiversityMetric
from evidently.metrics.recsys.f_beta_top_k import FBetaTopKMetric
from evidently.metrics.recsys.item_bias import ItemBiasMetric
from evidently.metrics.recsys.map_k import MAPKMetric
from evidently.metrics.recsys.mar_k import MARKMetric
from evidently.metrics.recsys.ndcg_k import NDCGKMetric
from evidently.metrics.recsys.novelty import NoveltyMetric
from evidently.metrics.recsys.pairwise_distance import PairwiseDistance
from evidently.metrics.recsys.personalisation import PersonalisationMetric
from evidently.metrics.recsys.popularity_bias import PopularityBias
from evidently.metrics.recsys.precision_recall_k import PrecisionRecallCalculation
from evidently.metrics.recsys.precision_top_k import PrecisionTopKMetric
from evidently.metrics.recsys.recall_top_k import RecallTopKMetric
from evidently.metrics.recsys.serendipity import SerendipityMetric
from evidently.metrics.recsys.train_stats import TrainStats
from evidently.metrics.recsys.user_bias import UserBiasMetric
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def f_beta_top_k():
    return TestMetric(
        "f_beta_top_k",
        FBetaTopKMetric(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def precision_recall_calc():
    return TestMetric(
        "precision_recall_calc",
        PrecisionRecallCalculation(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def precision_top_k():
    return TestMetric(
        "precision_top_k",
        PrecisionTopKMetric(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def recall_top_k():
    return TestMetric(
        "recall_top_k",
        RecallTopKMetric(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def map_k():
    return TestMetric(
        "map_k",
        MAPKMetric(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def mar_k():
    return TestMetric(
        "mar_k",
        MARKMetric(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def ndcg():
    return TestMetric(
        "ndcg",
        NDCGKMetric(3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def novelty():
    return TestMetric(
        "novelty",
        NoveltyMetric(k=3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def pairwise_distance():
    return TestMetric(
        "pairwise_distance",
        PairwiseDistance(k=3, item_features=["feature_1", "feature_2"]),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def serendipity():
    return TestMetric(
        "serendipity",
        SerendipityMetric(k=3, item_features=["feature_1", "feature_2"]),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def personalisation():
    return TestMetric(
        "personalisation",
        PersonalisationMetric(k=3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def popularity_bias():
    return TestMetric(
        "popularity_bias",
        PopularityBias(k=3),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def train_stats():
    return TestMetric(
        "train_stats",
        TrainStats(),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def user_bias():
    return TestMetric(
        "user_bias",
        UserBiasMetric(column_name="feature_1"),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def item_bias():
    return TestMetric(
        "item_bias",
        ItemBiasMetric(k=3, column_name="feature_1"),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )


@metric
def diversity_bias():
    return TestMetric(
        "diversity",
        DiversityMetric(k=3, item_features=["feature_1", "feature_2"]),
        NoopOutcome(),
        [DatasetTags.RECSYS],
    )
