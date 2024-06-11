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
        fingerprint="be707cc5a983bc2f90ac5da1e4cd1b73",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_correlations_metric():
    return TestMetric(
        name="dataset_correlations_metric",
        metric=DatasetCorrelationsMetric(),
        fingerprint="47976dadccb007d988b98b6e4e9f8f52",
        outcomes=NoopOutcome(),
        exclude_tags=[DatasetTags.RECSYS],
        marks=[slow],
    )


@metric
def conflict_target_metric():
    return TestMetric(
        name="conflict_target_metric",
        metric=ConflictTargetMetric(),
        fingerprint="c3427ca3cbd6b855e2fee72742f33281",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_correlation_metric():
    return TestMetric(
        name="text_descriptors_correlation_metric",
        metric=TextDescriptorsCorrelationMetric(column_name="Review_Text"),
        fingerprint="48f875cb83344e7529ac1873607a3ed6",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def text_descriptors_distribution():
    return TestMetric(
        name="text_descriptors_distribution",
        metric=TextDescriptorsDistribution(column_name="Review_Text"),
        fingerprint="c4f3e4beb3a76b1d8b1ebc9cd83f4af0",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_distribution_metric():
    return TestMetric(
        name="column_distribution_metric",
        metric=ColumnDistributionMetric(column_name="education"),
        fingerprint="f24b1e5586ef8d26390f841ce67b4ad3",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_list_metric():
    return TestMetric(
        name="column_value_list_metric",
        metric=ColumnValueListMetric(column_name="relationship", values=["Husband", "Unmarried"]),
        fingerprint="ada76140de8ea3aee841c836ee5f8a94",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_range_metric():
    return TestMetric(
        name="column_value_range_metric",
        metric=ColumnValueRangeMetric(column_name="age", left=10, right=20),
        fingerprint="981f380460c6f658952fdf189508c3a2",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def conflict_prediction_metric():
    return TestMetric(
        name="conflict_prediction_metric",
        metric=ConflictPredictionMetric(),
        fingerprint="6d76540b624e1e83323465445761f80c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_PREDICTION],
    )


@metric
def data_quality_stability_metric():
    return TestMetric(
        name="data_quality_stability_metric",
        metric=DataQualityStabilityMetric(),
        fingerprint="c5e84e833c2b12c40dd29dc043b04f80",
        outcomes=NoopOutcome(),
    )


@metric
def column_quantile_metric():
    return TestMetric(
        name="column_quantile_metric",
        metric=ColumnQuantileMetric(column_name="education-num", quantile=0.75),
        fingerprint="280ef7570985ed4edbd5e92eef6d60e4",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_category_metric():
    return TestMetric(
        name="column_category_metric",
        metric=ColumnCategoryMetric(column_name="education", category="Some-college"),
        fingerprint="00b101532a5cd9d715f892062b74f16d",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )
