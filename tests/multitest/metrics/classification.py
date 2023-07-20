import pandas as pd

from evidently import ColumnMapping
from evidently.metric_results import ConfusionMatrix
from evidently.metric_results import DatasetClassificationQuality
from evidently.metric_results import Histogram
from evidently.metric_results import HistogramData
from evidently.metrics.classification_performance.class_balance_metric import ClassificationClassBalance
from evidently.metrics.classification_performance.class_balance_metric import ClassificationClassBalanceResult
from evidently.metrics.classification_performance.class_separation_metric import ClassificationClassSeparationPlot
from evidently.metrics.classification_performance.classification_dummy_metric import ClassificationDummyMetric
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQualityMetric
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQualityMetricResult
from evidently.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrix
from evidently.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrixResult
from evidently.metrics.classification_performance.pr_curve_metric import ClassificationPRCurve
from evidently.metrics.classification_performance.pr_table_metric import ClassificationPRTable
from evidently.metrics.classification_performance.probability_distribution_metric import ClassificationProbDistribution
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_feature_table import ClassificationQualityByFeatureTable
from evidently.metrics.classification_performance.roc_curve_metric import ClassificationRocCurve
from evidently.tests.utils import approx_result
from tests.multitest.conftest import AssertExpectedResult
from tests.multitest.conftest import NoopOutcome
from tests.multitest.conftest import make_approx_type
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
def classification_p_r_curve_values():
    m = ClassificationPRCurve()
    return TestMetric(
        "classification_p_r_curve_values",
        m,
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                        a=[0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
                        b=[0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
                        c=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
                    ),
                ),
                column_mapping=ColumnMapping(prediction=["a", "b", "c"]),
            ): NoopOutcome()  # todo: check results
        },
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
            ): AssertExpectedResult(
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
            ): AssertExpectedResult(
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
def classification_confusion_matrix_values():
    metric = ClassificationConfusionMatrix()

    return TestMetric(
        "classification_confusion_matrix_values",
        metric,
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                        prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
                    )
                ),
            ): AssertExpectedResult(
                metric,
                ClassificationConfusionMatrixResult(
                    current_matrix=ConfusionMatrix(
                        labels=["a", "b", "c"],
                        values=[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                    )
                ),
            ),
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["a", "a", "a", "a", "a", "b", "b", "b", "b"],
                        prediction=["a", "b", "b", "a", "b", "a", "a", "b", "b"],
                    )
                ),
            ): AssertExpectedResult(
                metric,
                ClassificationConfusionMatrixResult(
                    current_matrix=ConfusionMatrix(
                        labels=["a", "b"],
                        values=[[2, 3], [2, 2]],
                    )
                ),
            ),
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["c", "c", "c", "b", "b", "b", "a", "a", "a"],
                        prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
                    )
                ),
            ): AssertExpectedResult(
                metric,
                ClassificationConfusionMatrixResult(
                    current_matrix=ConfusionMatrix(
                        labels=["a", "b", "c"],
                        values=[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                    )
                ),
            ),
        },
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
def classification_quality_values():
    current = pd.DataFrame(
        data=dict(
            target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
        ),
    )

    current_binary = pd.DataFrame(
        data=dict(
            target=[1, 1, 1, 1, 0, 0, 0, 0, 1],
            prediction=[0.7, 0.8, 0.9, 0.4, 0.1, 0.2, 0.1, 0.3, 0.8],
        ),
    )

    metric = ClassificationQualityMetric()
    return TestMetric(
        "classification_quality_values",
        metric,
        outcomes={
            TestDataset(current=current, column_mapping=ColumnMapping()): AssertExpectedResult(
                metric,
                ClassificationQualityMetricResult(
                    current=make_approx_type(DatasetClassificationQuality)(
                        accuracy=approx_result(0.3333333),
                        precision=approx_result(0.3333333),
                        f1=approx_result(0.3333333),
                        recall=approx_result(0.3333333),
                    ),
                    target_name="target",
                ),
            ),
            TestDataset("binary", current=current_binary, column_mapping=ColumnMapping()): AssertExpectedResult(
                metric,
                ClassificationQualityMetricResult(
                    current=make_approx_type(DatasetClassificationQuality, ignore_not_set=True)(
                        accuracy=approx_result(8 / 9),
                        f1=approx_result(0.888888888888889),
                        precision=approx_result(4 / 4),
                        recall=approx_result(4 / 5),
                        roc_auc=approx_result(1.0),
                        log_loss=approx_result(0.29057253),
                        tpr=0.8,
                        tnr=1.0,
                        fpr=0.0,
                        fnr=0.2,
                    ),
                    target_name="target",
                ),
            ),
        },
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
