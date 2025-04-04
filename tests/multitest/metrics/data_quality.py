from evidently.legacy.metrics.data_quality.column_category_metric import ColumnCategoryMetric
from evidently.legacy.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetric
from evidently.legacy.metrics.data_quality.column_distribution_metric import ColumnDistributionMetric
from evidently.legacy.metrics.data_quality.column_quantile_metric import ColumnQuantileMetric
from evidently.legacy.metrics.data_quality.column_value_list_metric import ColumnValueListMetric
from evidently.legacy.metrics.data_quality.column_value_range_metric import ColumnValueRangeMetric
from evidently.legacy.metrics.data_quality.conflict_prediction_metric import ConflictPredictionMetric
from evidently.legacy.metrics.data_quality.conflict_target_metric import ConflictTargetMetric
from evidently.legacy.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetric
from evidently.legacy.metrics.data_quality.stability_metric import DataQualityStabilityMetric
from evidently.legacy.metrics.data_quality.text_descriptors_correlation_metric import TextDescriptorsCorrelationMetric
from evidently.legacy.metrics.data_quality.text_descriptors_distribution import TextDescriptorsDistribution
from tests.conftest import slow
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def column_correlations_metric():
    return TestMetric(
        name="column_correlations_metric",
        metric=ColumnCorrelationsMetric(column_name="education"),
        fingerprint="ec0b93b8effa40c37518e9e124140ebf",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_correlations_metric():
    return TestMetric(
        name="dataset_correlations_metric",
        metric=DatasetCorrelationsMetric(),
        fingerprint="b3732644bdf187795591ccb321679a2b",
        outcomes=NoopOutcome(),
        exclude_tags=[DatasetTags.RECSYS],
        marks=[slow],
    )


@metric
def conflict_target_metric():
    return TestMetric(
        name="conflict_target_metric",
        metric=ConflictTargetMetric(),
        fingerprint="3ad555e8b95b86e136e15a6741891130",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_correlation_metric():
    return TestMetric(
        name="text_descriptors_correlation_metric",
        metric=TextDescriptorsCorrelationMetric(column_name="Review_Text"),
        fingerprint="b1877ae3b6279cc83ced40c5984b2a40",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def text_descriptors_distribution():
    return TestMetric(
        name="text_descriptors_distribution",
        metric=TextDescriptorsDistribution(column_name="Review_Text"),
        fingerprint="4104b02cb3897e06ecb5997ea95d5d8c",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_distribution_metric():
    return TestMetric(
        name="column_distribution_metric",
        metric=ColumnDistributionMetric(column_name="education"),
        fingerprint="95e91b3d899d1caf8316895d3cce766e",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_list_metric():
    return TestMetric(
        name="column_value_list_metric",
        metric=ColumnValueListMetric(column_name="relationship", values=["Husband", "Unmarried"]),
        fingerprint="fd0798bfe9b249931786374ea5d242e5",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_range_metric():
    return TestMetric(
        name="column_value_range_metric",
        metric=ColumnValueRangeMetric(column_name="age", left=10, right=20),
        fingerprint="b90b52004cee0cb9f75f3703759d567f",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def conflict_prediction_metric():
    return TestMetric(
        name="conflict_prediction_metric",
        metric=ConflictPredictionMetric(),
        fingerprint="2b720483dba14c97f04628ac4182bf06",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_PREDICTION],
    )


@metric
def data_quality_stability_metric():
    return TestMetric(
        name="data_quality_stability_metric",
        metric=DataQualityStabilityMetric(),
        fingerprint="e8d02039c1a2819dfa336986bb2dfa2c",
        outcomes=NoopOutcome(),
    )


@metric
def column_quantile_metric():
    return TestMetric(
        name="column_quantile_metric",
        metric=ColumnQuantileMetric(column_name="education-num", quantile=0.75),
        fingerprint="29645f8bfb647d9fcd8e65ff83a4a305",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_category_metric():
    return TestMetric(
        name="column_category_metric",
        metric=ColumnCategoryMetric(column_name="education", category="Some-college"),
        fingerprint="7f5b220826f7b1b653a99ebf49afdd6e",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )
