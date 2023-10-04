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
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def column_correlations_metric():
    return TestMetric(
        "column_correlations_metric",
        ColumnCorrelationsMetric(column_name="education"),
        NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_correlations_metric():
    return TestMetric(
        "dataset_correlations_metric", DatasetCorrelationsMetric(), NoopOutcome()
    )


@metric
def conflict_target_metric():
    return TestMetric(
        "conflict_target_metric",
        ConflictTargetMetric(),
        NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_correlation_metric():
    return TestMetric(
        "text_descriptors_correlation_metric",
        TextDescriptorsCorrelationMetric(column_name="Review_Text"),
        NoopOutcome(),
        dataset_names=["reviews"],
    )


@metric
def text_descriptors_distribution():
    return TestMetric(
        "text_descriptors_distribution",
        TextDescriptorsDistribution(column_name="Review_Text"),
        NoopOutcome(),
        dataset_names=["reviews"],
    )


@metric
def column_distribution_metric():
    return TestMetric(
        "column_distribution_metric",
        ColumnDistributionMetric(column_name="education"),
        NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_list_metric():
    return TestMetric(
        "column_value_list_metric",
        ColumnValueListMetric(
            column_name="relationship", values=["Husband", "Unmarried"]
        ),
        NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_range_metric():
    return TestMetric(
        "column_value_range_metric",
        ColumnValueRangeMetric(column_name="age", left=10, right=20),
        NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def conflict_prediction_metric():
    return TestMetric(
        "conflict_prediction_metric",
        ConflictPredictionMetric(),
        NoopOutcome(),
        include_tags=[DatasetTags.HAS_PREDICTION],
    )


@metric
def data_quality_stability_metric():
    return TestMetric(
        "data_quality_stability_metric", DataQualityStabilityMetric(), NoopOutcome()
    )


@metric
def column_quantile_metric():
    return TestMetric(
        "column_quantile_metric",
        ColumnQuantileMetric(column_name="education-num", quantile=0.75),
        NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_category_metric():
    return TestMetric(
        "column_category_metric",
        ColumnCategoryMetric(column_name="education", category="Some-college"),
        NoopOutcome(),
        dataset_names=["adult"],
    )
