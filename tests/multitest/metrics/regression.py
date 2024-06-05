from evidently.metrics.regression_performance.abs_perc_error_in_time import RegressionAbsPercentageErrorPlot
from evidently.metrics.regression_performance.error_bias_table import RegressionErrorBiasTable
from evidently.metrics.regression_performance.error_distribution import RegressionErrorDistribution
from evidently.metrics.regression_performance.error_in_time import RegressionErrorPlot
from evidently.metrics.regression_performance.error_normality import RegressionErrorNormality
from evidently.metrics.regression_performance.predicted_and_actual_in_time import RegressionPredictedVsActualPlot
from evidently.metrics.regression_performance.predicted_vs_actual import RegressionPredictedVsActualScatter
from evidently.metrics.regression_performance.regression_dummy_metric import RegressionDummyMetric
from evidently.metrics.regression_performance.regression_performance_metrics import RegressionPerformanceMetrics
from evidently.metrics.regression_performance.regression_quality import RegressionQualityMetric
from evidently.metrics.regression_performance.top_error import RegressionTopErrorMetric
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def regression_error_plot():
    return TestMetric(
        name="regression_error_plot",
        metric=RegressionErrorPlot(),
        fingerprint="6549d5cb78f391d7203b87649c323cdf",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_abs_percentage_error_plot():
    return TestMetric(
        name="regression_abs_percentage_error_plot",
        metric=RegressionAbsPercentageErrorPlot(),
        fingerprint="db17f2fd24edc2bc845e407d6cef08bb",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_performance_metrics():
    return TestMetric(
        name="regression_performance_metrics",
        metric=RegressionPerformanceMetrics(),
        fingerprint="9bcf21bae6f8ef6a522bcc78f80b7269",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_quality_metric():
    return TestMetric(
        name="regression_quality_metric",
        metric=RegressionQualityMetric(),
        fingerprint="2dc1c1b078857192dc760ebdae7abfc1",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_top_error_metric():
    return TestMetric(
        name="regression_top_error_metric",
        metric=RegressionTopErrorMetric(),
        fingerprint="1d21dffb38739baf31ac077ecb654a2c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_dummy_metric():
    return TestMetric(
        name="regression_dummy_metric",
        metric=RegressionDummyMetric(),
        fingerprint="bd479bcf3e3f0a63ed4b2711aa7bab01",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_plot():
    return TestMetric(
        name="regression_predicted_vs_actual_plot",
        metric=RegressionPredictedVsActualPlot(),
        fingerprint="dde8cde7f89398a07d44751e01cd230c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_bias_table():
    return TestMetric(
        name="regression_error_bias_table",
        metric=RegressionErrorBiasTable(),
        fingerprint="1b803c6c1a5738ab8bb504a027669379",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_normality():
    return TestMetric(
        name="regression_error_normality",
        metric=RegressionErrorNormality(),
        fingerprint="e311b3e6c4603973f121f727554dd304",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_distribution():
    return TestMetric(
        name="regression_error_distribution",
        metric=RegressionErrorDistribution(),
        fingerprint="cb8d574b86b12f391c1f50d7aaae8055",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_scatter():
    return TestMetric(
        name="regression_predicted_vs_actual_scatter",
        metric=RegressionPredictedVsActualScatter(),
        fingerprint="9e5781de710c8b26e2c776e087d7acd8",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION, DatasetTags.HAS_PREDICTION, DatasetTags.HAS_TARGET],
    )
