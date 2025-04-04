from evidently.legacy.metrics.regression_performance.abs_perc_error_in_time import RegressionAbsPercentageErrorPlot
from evidently.legacy.metrics.regression_performance.error_bias_table import RegressionErrorBiasTable
from evidently.legacy.metrics.regression_performance.error_distribution import RegressionErrorDistribution
from evidently.legacy.metrics.regression_performance.error_in_time import RegressionErrorPlot
from evidently.legacy.metrics.regression_performance.error_normality import RegressionErrorNormality
from evidently.legacy.metrics.regression_performance.predicted_and_actual_in_time import RegressionPredictedVsActualPlot
from evidently.legacy.metrics.regression_performance.predicted_vs_actual import RegressionPredictedVsActualScatter
from evidently.legacy.metrics.regression_performance.regression_dummy_metric import RegressionDummyMetric
from evidently.legacy.metrics.regression_performance.regression_performance_metrics import RegressionPerformanceMetrics
from evidently.legacy.metrics.regression_performance.regression_quality import RegressionQualityMetric
from evidently.legacy.metrics.regression_performance.top_error import RegressionTopErrorMetric
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def regression_error_plot():
    return TestMetric(
        name="regression_error_plot",
        metric=RegressionErrorPlot(),
        fingerprint="29be3a731577fecd1c0dd976906735b7",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_abs_percentage_error_plot():
    return TestMetric(
        name="regression_abs_percentage_error_plot",
        metric=RegressionAbsPercentageErrorPlot(),
        fingerprint="cf08325cf9a37966d8eff5a253b58dd0",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_performance_metrics():
    return TestMetric(
        name="regression_performance_metrics",
        metric=RegressionPerformanceMetrics(),
        fingerprint="65373a5ec0a79c3ed055731dbd59b849",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_quality_metric():
    return TestMetric(
        name="regression_quality_metric",
        metric=RegressionQualityMetric(),
        fingerprint="83de83d3607f15a79fff37b214301959",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_top_error_metric():
    return TestMetric(
        name="regression_top_error_metric",
        metric=RegressionTopErrorMetric(),
        fingerprint="4bba47983f251bd7fd183147d39ac9f9",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_dummy_metric():
    return TestMetric(
        name="regression_dummy_metric",
        metric=RegressionDummyMetric(),
        fingerprint="8868cdc279f77879f2f8d0d4fa7a7f72",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_plot():
    return TestMetric(
        name="regression_predicted_vs_actual_plot",
        metric=RegressionPredictedVsActualPlot(),
        fingerprint="84919c416a2d031586406f6cb259409d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_bias_table():
    return TestMetric(
        name="regression_error_bias_table",
        metric=RegressionErrorBiasTable(),
        fingerprint="050a13de08cb888ac1bc7f22ca5ac2d9",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_normality():
    return TestMetric(
        name="regression_error_normality",
        metric=RegressionErrorNormality(),
        fingerprint="7324d39037d0f7ba1f977c090e27f076",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_distribution():
    return TestMetric(
        name="regression_error_distribution",
        metric=RegressionErrorDistribution(),
        fingerprint="9b7e89835990fcbabb266eac2bc2928f",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_scatter():
    return TestMetric(
        name="regression_predicted_vs_actual_scatter",
        metric=RegressionPredictedVsActualScatter(),
        fingerprint="b1a0065df4d04b2984e0ae388b304ace",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION, DatasetTags.HAS_PREDICTION, DatasetTags.HAS_TARGET],
    )
