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
        fingerprint="16ae7224d6097fa78ca0cc080016b1f4",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_abs_percentage_error_plot():
    return TestMetric(
        name="regression_abs_percentage_error_plot",
        metric=RegressionAbsPercentageErrorPlot(),
        fingerprint="40c910d043e21fe996e4dd822b82ecc9",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_performance_metrics():
    return TestMetric(
        name="regression_performance_metrics",
        metric=RegressionPerformanceMetrics(),
        fingerprint="8a0972d3abe25ccf53b074f83d0e6a67",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_quality_metric():
    return TestMetric(
        name="regression_quality_metric",
        metric=RegressionQualityMetric(),
        fingerprint="ccfcebaf7ccaacc7c43c9f62035a128f",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_top_error_metric():
    return TestMetric(
        name="regression_top_error_metric",
        metric=RegressionTopErrorMetric(),
        fingerprint="45436313d7756b0f671ade42e57dc699",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_dummy_metric():
    return TestMetric(
        name="regression_dummy_metric",
        metric=RegressionDummyMetric(),
        fingerprint="2543c5ad5afdfc3f02161a42247078bd",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_plot():
    return TestMetric(
        name="regression_predicted_vs_actual_plot",
        metric=RegressionPredictedVsActualPlot(),
        fingerprint="9a8d976963a9a33b1fd2e60baed08802",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_bias_table():
    return TestMetric(
        name="regression_error_bias_table",
        metric=RegressionErrorBiasTable(),
        fingerprint="47fc390cd82119c769ec6870674c5e85",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_normality():
    return TestMetric(
        name="regression_error_normality",
        metric=RegressionErrorNormality(),
        fingerprint="f9690b3332f89ebfbc0cd2ce25ff60e9",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_error_distribution():
    return TestMetric(
        name="regression_error_distribution",
        metric=RegressionErrorDistribution(),
        fingerprint="cd5a010985bdbbe2942900943b56dad8",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION],
    )


@metric
def regression_predicted_vs_actual_scatter():
    return TestMetric(
        name="regression_predicted_vs_actual_scatter",
        metric=RegressionPredictedVsActualScatter(),
        fingerprint="ad185986b1694e026e0f942637104403",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.REGRESSION, DatasetTags.HAS_PREDICTION, DatasetTags.HAS_TARGET],
    )
