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
        fingerprint="c775c38ca8fd040b3b21f58a1b9f3cd3",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_correlations_metric():
    return TestMetric(
        name="dataset_correlations_metric",
        metric=DatasetCorrelationsMetric(),
        fingerprint="45e9a7a5b2d8f63a3330648e3c548c3c",
        outcomes=NoopOutcome(),
        exclude_tags=[DatasetTags.RECSYS],
        marks=[slow],
    )


@metric
def conflict_target_metric():
    return TestMetric(
        name="conflict_target_metric",
        metric=ConflictTargetMetric(),
        fingerprint="1259855b872f6b12f835cafc7f3b7239",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_correlation_metric():
    return TestMetric(
        name="text_descriptors_correlation_metric",
        metric=TextDescriptorsCorrelationMetric(column_name="Review_Text"),
        fingerprint="7f4e0c38aa910a24b8490c8c5a889d55",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def text_descriptors_distribution():
    return TestMetric(
        name="text_descriptors_distribution",
        metric=TextDescriptorsDistribution(column_name="Review_Text"),
        fingerprint="54465c8723324815de7a671e5d7e4468",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_distribution_metric():
    return TestMetric(
        name="column_distribution_metric",
        metric=ColumnDistributionMetric(column_name="education"),
        fingerprint="72839e5afbe6fc4c9d975e8f072510e2",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_list_metric():
    return TestMetric(
        name="column_value_list_metric",
        metric=ColumnValueListMetric(column_name="relationship", values=["Husband", "Unmarried"]),
        fingerprint="9001233bb9fac6941786e5b56dcce15c",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_range_metric():
    return TestMetric(
        name="column_value_range_metric",
        metric=ColumnValueRangeMetric(column_name="age", left=10, right=20),
        fingerprint="1eecd0e2ea6701a872526c629bf039e5",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def conflict_prediction_metric():
    return TestMetric(
        name="conflict_prediction_metric",
        metric=ConflictPredictionMetric(),
        fingerprint="3858a9345275641faf507095d577a4f0",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_PREDICTION],
    )


@metric
def data_quality_stability_metric():
    return TestMetric(
        name="data_quality_stability_metric",
        metric=DataQualityStabilityMetric(),
        fingerprint="b74e85ea6cbce85b8d968b95aa428bb8",
        outcomes=NoopOutcome(),
    )


@metric
def column_quantile_metric():
    return TestMetric(
        name="column_quantile_metric",
        metric=ColumnQuantileMetric(column_name="education-num", quantile=0.75),
        fingerprint="13165afd6df8073f353b7ed6d4983a1a",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_category_metric():
    return TestMetric(
        name="column_category_metric",
        metric=ColumnCategoryMetric(column_name="education", category="Some-college"),
        fingerprint="f37ca8273d73f2e31af2790c8a5123b8",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )
