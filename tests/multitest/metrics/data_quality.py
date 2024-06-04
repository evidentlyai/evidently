from evidently.metrics.data_quality.column_category_metric import ColumnCategoryMetric
from evidently.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetric
from evidently.metrics.data_quality.column_distribution_metric import ColumnDistributionMetric
from evidently.metrics.data_quality.column_quantile_metric import ColumnQuantileMetric
from evidently.metrics.data_quality.column_value_list_metric import ColumnValueListMetric
from evidently.metrics.data_quality.column_value_range_metric import ColumnValueRangeMetric
from evidently.metrics.data_quality.conflict_prediction_metric import ConflictPredictionMetric
from evidently.metrics.data_quality.conflict_target_metric import ConflictTargetMetric
from evidently.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetric
from evidently.metrics.data_quality.stability_metric import DataQualityStabilityMetric
from evidently.metrics.data_quality.text_descriptors_correlation_metric import TextDescriptorsCorrelationMetric
from evidently.metrics.data_quality.text_descriptors_distribution import TextDescriptorsDistribution
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
        fingerprint="1335ba8694746383a255a9785bf1ea4e",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_correlations_metric():
    return TestMetric(
        name="dataset_correlations_metric",
        metric=DatasetCorrelationsMetric(),
        fingerprint="8c019a41b048119661f0d40b91557f06",
        outcomes=NoopOutcome(),
        exclude_tags=[DatasetTags.RECSYS],
        marks=[slow],
    )


@metric
def conflict_target_metric():
    return TestMetric(
        name="conflict_target_metric",
        metric=ConflictTargetMetric(),
        fingerprint="b422147bfa24f93cfab9aa4a6610e393",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_correlation_metric():
    return TestMetric(
        name="text_descriptors_correlation_metric",
        metric=TextDescriptorsCorrelationMetric(column_name="Review_Text"),
        fingerprint="d58bda68fb5c345fe3b36190d94e23ea",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def text_descriptors_distribution():
    return TestMetric(
        name="text_descriptors_distribution",
        metric=TextDescriptorsDistribution(column_name="Review_Text"),
        fingerprint="c67f116de18a37af48a20e198714d701",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_distribution_metric():
    return TestMetric(
        name="column_distribution_metric",
        metric=ColumnDistributionMetric(column_name="education"),
        fingerprint="d6a4ce56cb698e59919362dc3f6157fb",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_list_metric():
    return TestMetric(
        name="column_value_list_metric",
        metric=ColumnValueListMetric(column_name="relationship", values=["Husband", "Unmarried"]),
        fingerprint="3038db11eb98707753bd53e6a12731c2",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_range_metric():
    return TestMetric(
        name="column_value_range_metric",
        metric=ColumnValueRangeMetric(column_name="age", left=10, right=20),
        fingerprint="38afbe08382fd9a9a066282871fdc139",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def conflict_prediction_metric():
    return TestMetric(
        name="conflict_prediction_metric",
        metric=ConflictPredictionMetric(),
        fingerprint="d056e58a16180405ff1f95a1deea55be",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_PREDICTION],
    )


@metric
def data_quality_stability_metric():
    return TestMetric(
        name="data_quality_stability_metric",
        metric=DataQualityStabilityMetric(),
        fingerprint="c0720c2182a865e8e2ce276445badf19",
        outcomes=NoopOutcome(),
    )


@metric
def column_quantile_metric():
    return TestMetric(
        name="column_quantile_metric",
        metric=ColumnQuantileMetric(column_name="education-num", quantile=0.75),
        fingerprint="3a9991c361d9ad3b9c2ee8c26df5ab05",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_category_metric():
    return TestMetric(
        name="column_category_metric",
        metric=ColumnCategoryMetric(column_name="education", category="Some-college"),
        fingerprint="f418f44eee0ec102aea190031417e0db",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )
