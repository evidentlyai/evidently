import numpy as np
import pandas as pd

from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.metric_results import Histogram
from evidently.metric_results import HistogramData
from evidently.metrics.classification_performance.class_balance_metric import ClassificationClassBalance
from evidently.metrics.classification_performance.class_balance_metric import ClassificationClassBalanceResult
from evidently.metrics.classification_performance.class_separation_metric import ClassificationClassSeparationPlot
from evidently.metrics.classification_performance.classification_dummy_metric import ClassificationDummyMetric
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQualityMetric
from evidently.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrix
from evidently.metrics.classification_performance.pr_curve_metric import ClassificationPRCurve
from evidently.metrics.classification_performance.pr_table_metric import ClassificationPRTable
from evidently.metrics.classification_performance.probability_distribution_metric import ClassificationProbDistribution
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_feature_table import ClassificationQualityByFeatureTable
from evidently.metrics.classification_performance.roc_curve_metric import ClassificationRocCurve
from evidently.report import Report
from tests.multitest.conftest import NoopOutcome
from tests.multitest.conftest import TestOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def classification_class_separation_plot():
    return TestMetric(
        "classification_class_separation_plot",
        ClassificationClassSeparationPlot(),
        NoopOutcome(),
        [DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_table():
    return TestMetric(
        "classification_p_r_table",
        ClassificationPRTable(),
        NoopOutcome(),
        [DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_curve():
    return TestMetric(
        "classification_p_r_curve",
        ClassificationPRCurve(),
        NoopOutcome(),
        [DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_quality_by_class():
    return TestMetric(
        "classification_quality_by_class", ClassificationQualityByClass(), NoopOutcome(), [DatasetTags.CLASSIFICATION]
    )


@metric
def classification_class_balance():
    return TestMetric(
        "classification_class_balance", ClassificationClassBalance(), NoopOutcome(), [DatasetTags.CLASSIFICATION]
    )


class ExpectedValue(TestOutcome):
    def __init__(self, metric: Metric, result: MetricResult):
        self.metric = metric
        self.result = result

    def check(self, report: Report):
        result = report._inner_suite.context.metric_results[self.metric]
        np.testing.assert_equal(result, self.result)


@metric
def classification_class_balance_values():
    metric = ClassificationClassBalance()

    return TestMetric(
        "classification_class_balance_values",
        metric,
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    {
                        "target": ["a", "a", "a", "a", "a", "b", "c", "c", "c"],
                        "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    }
                )
            ): ExpectedValue(
                metric=metric,
                result=ClassificationClassBalanceResult(
                    plot_data=Histogram(
                        current=HistogramData.from_df(pd.DataFrame({"x": ["a", "c", "b"], "count": [5, 3, 1]}))
                    )
                ),
            ),
            TestDataset(
                reference=pd.DataFrame(
                    {
                        "target": ["a", "a", "b", "b", "b", "c", "c", "c", "c"],
                        "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    }
                ),
                current=pd.DataFrame(
                    {
                        "target": ["a", "a", "a", "a", "a", "b", "c", "c", "c"],
                        "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    }
                ),
            ): ExpectedValue(
                metric=metric,
                result=ClassificationClassBalanceResult(
                    plot_data=Histogram(
                        current=HistogramData.from_df(pd.DataFrame({"x": ["a", "c", "b"], "count": [5, 3, 1]})),
                        reference=HistogramData.from_df(pd.DataFrame({"x": ["c", "b", "a"], "count": [4, 3, 2]})),
                    )
                ),
            ),
        },
    )


@metric
def classification_confusion_matrix():
    return TestMetric(
        "classification_confusion_matrix", ClassificationConfusionMatrix(), NoopOutcome(), [DatasetTags.CLASSIFICATION]
    )


@metric
def classification_roc_curve():
    return TestMetric(
        "classification_roc_curve",
        ClassificationRocCurve(),
        NoopOutcome(),
        [DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_quality_metric():
    return TestMetric(
        "classification_quality_metric", ClassificationQualityMetric(), NoopOutcome(), [DatasetTags.CLASSIFICATION]
    )


@metric
def classification_quality_by_feature_table():
    return TestMetric(
        "classification_quality_by_feature_table",
        ClassificationQualityByFeatureTable(),
        NoopOutcome(),
        [DatasetTags.CLASSIFICATION],
    )


@metric
def classification_prob_distribution():
    return TestMetric(
        "classification_prob_distribution",
        ClassificationProbDistribution(),
        NoopOutcome(),
        [DatasetTags.CLASSIFICATION],
    )


@metric
def classification_dummy_metric():
    return TestMetric(
        "classification_dummy_metric", ClassificationDummyMetric(), NoopOutcome(), [DatasetTags.CLASSIFICATION]
    )
