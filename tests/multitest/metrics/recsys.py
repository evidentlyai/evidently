from evidently.metrics.recsys.f_beta_top_k import FBetaTopKMetric
from evidently.metrics.recsys.map_k import MAPKMetric
from evidently.metrics.recsys.mar_k import MARKMetric
from evidently.metrics.recsys.ndcg_k import NDCGKMetric
from evidently.metrics.recsys.precision_recall_k import PrecisionRecallCalculation
from evidently.metrics.recsys.precision_top_k import PrecisionTopKMetric
from evidently.metrics.recsys.recall_top_k import RecallTopKMetric
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
