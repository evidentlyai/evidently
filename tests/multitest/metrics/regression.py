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
        fingerprint="8c8bb19e517359561148725ac8688c1c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_abs_percentage_error_plot():
    return TestMetric(
        name="regression_abs_percentage_error_plot",
        metric=RegressionAbsPercentageErrorPlot(),
        fingerprint="f2115d320f6b9c40c1c0ad23393dda07",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_performance_metrics():
    return TestMetric(
        name="regression_performance_metrics",
        metric=RegressionPerformanceMetrics(),
        fingerprint="72db75a7b25260cab3fca04bf74efdec",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_quality_metric():
    return TestMetric(
        name="regression_quality_metric",
        metric=RegressionQualityMetric(),
        fingerprint="4dcce3fed9d6c5bc925787a08dc945d9",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_top_error_metric():
    return TestMetric(
        name="regression_top_error_metric",
        metric=RegressionTopErrorMetric(),
        fingerprint="da0fbe768227d0a2804709573f8972a9",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_dummy_metric():
    return TestMetric(
        name="regression_dummy_metric",
        metric=RegressionDummyMetric(),
        fingerprint="65f71b0f273da54c3431cef43982299b",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_plot():
    return TestMetric(
        name="regression_predicted_vs_actual_plot",
        metric=RegressionPredictedVsActualPlot(),
        fingerprint="7decda864d2eceb32fbb103e072ebaf6",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_bias_table():
    return TestMetric(
        name="regression_error_bias_table",
        metric=RegressionErrorBiasTable(),
        fingerprint="814faec5614e6d85a963f73d4a696a50",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_normality():
    return TestMetric(
        name="regression_error_normality",
        metric=RegressionErrorNormality(),
        fingerprint="c30863cfaf33d1dcab6b0980a10d7da5",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_distribution():
    return TestMetric(
        name="regression_error_distribution",
        metric=RegressionErrorDistribution(),
        fingerprint="a0267e8c5e642f90c124b9512c4b0645",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_scatter():
    return TestMetric(
        name="regression_predicted_vs_actual_scatter",
        metric=RegressionPredictedVsActualScatter(),
        fingerprint="069ef7b9d91218a620392a167be74316",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION, DatasetTags.HAS_PREDICTION, DatasetTags.HAS_TARGET],
    )
