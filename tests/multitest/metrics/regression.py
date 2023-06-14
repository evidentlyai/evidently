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
from tests.multitest.datasets import DatasetTags
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def regression_error_plot():
    return TestMetric("regression_error_plot", RegressionErrorPlot(), [DatasetTags.REGRESSION])


@metric
def regression_abs_percentage_error_plot():
    return TestMetric(
        "regression_abs_percentage_error_plot", RegressionAbsPercentageErrorPlot(), [DatasetTags.REGRESSION]
    )


@metric
def regression_performance_metrics():
    return TestMetric("regression_performance_metrics", RegressionPerformanceMetrics(), [DatasetTags.REGRESSION])


@metric
def regression_quality_metric():
    return TestMetric("regression_quality_metric", RegressionQualityMetric(), [DatasetTags.REGRESSION])


@metric
def regression_top_error_metric():
    return TestMetric("regression_top_error_metric", RegressionTopErrorMetric(), [DatasetTags.REGRESSION])


@metric
def regression_dummy_metric():
    return TestMetric("regression_dummy_metric", RegressionDummyMetric(), [DatasetTags.REGRESSION])


@metric
def regression_predicted_vs_actual_plot():
    return TestMetric(
        "regression_predicted_vs_actual_plot", RegressionPredictedVsActualPlot(), [DatasetTags.REGRESSION]
    )


@metric
def regression_error_bias_table():
    return TestMetric("regression_error_bias_table", RegressionErrorBiasTable(), [DatasetTags.REGRESSION])


@metric
def regression_error_normality():
    return TestMetric("regression_error_normality", RegressionErrorNormality(), [DatasetTags.REGRESSION])


@metric
def regression_error_distribution():
    return TestMetric("regression_error_distribution", RegressionErrorDistribution(), [DatasetTags.REGRESSION])


@metric
def regression_predicted_vs_actual_scatter():
    return TestMetric(
        "regression_predicted_vs_actual_scatter",
        RegressionPredictedVsActualScatter(),
        [DatasetTags.REGRESSION, DatasetTags.HAS_PREDICTION, DatasetTags.HAS_TARGET],
    )
