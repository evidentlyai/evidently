import numpy as np
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
from evidently.metrics.classification_performance.lift_curve_metric import ClassificationLiftCurve
from evidently.metrics.classification_performance.lift_table_metric import ClassificationLiftTable
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
        name="classification_class_separation_plot",
        metric=ClassificationClassSeparationPlot(),
        fingerprint="28dc663e180f5d31456d48d452b4849b",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_table():
    return TestMetric(
        name="classification_p_r_table",
        metric=ClassificationPRTable(),
        fingerprint="e6b2c4d0e0b5f3789d5d6eee9063e062",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_table_values():
    m = ClassificationPRTable()
    return TestMetric(
        name="classification_p_r_table_values",
        metric=m,
        fingerprint="e6b2c4d0e0b5f3789d5d6eee9063e062",
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
def classification_p_r_curve():
    return TestMetric(
        name="classification_p_r_curve",
        metric=ClassificationPRCurve(),
        fingerprint="ddb196d496ff95c452aa8c7047fd425d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_lift_table():
    return TestMetric(
        name="classification_lift_table",
        metric=ClassificationLiftTable(),
        fingerprint="d75e8f44b88c2c0100dffb44f0ab158c",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_lift_curve():
    return TestMetric(
        name="classification_lift_curve",
        metric=ClassificationLiftCurve(),
        fingerprint="f634924c8e9c8d8da7dc1a46ee3e22fb",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_curve_values():
    m = ClassificationPRCurve()
    return TestMetric(
        name="classification_p_r_curve_values",
        metric=m,
        fingerprint="ddb196d496ff95c452aa8c7047fd425d",
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
        name="classification_quality_by_class",
        metric=ClassificationQualityByClass(),
        fingerprint="99d10ad99d5cd21e9c83fc808093d1a5",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_class_balance():
    return TestMetric(
        name="classification_class_balance",
        metric=ClassificationClassBalance(),
        fingerprint="b08256a576e0a1c7c74430e575878d65",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_class_balance_values():
    metric = ClassificationClassBalance()

    return TestMetric(
        name="classification_class_balance_values",
        metric=metric,
        fingerprint="b08256a576e0a1c7c74430e575878d65",
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    {
                        "target": ["a", "a", "a", "a", "a", "b", "c", "c", "c"],
                        "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    }
                )
            ): AssertExpectedResult(
                result=ClassificationClassBalanceResult(
                    plot_data=Histogram(
                        current=HistogramData.from_df(pd.DataFrame({"x": ["a", "c", "b"], "count": [5, 3, 1]}))
                    )
                ),
                metric=metric,
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
                result=ClassificationClassBalanceResult(
                    plot_data=Histogram(
                        current=HistogramData.from_df(pd.DataFrame({"x": ["a", "c", "b"], "count": [5, 3, 1]})),
                        reference=HistogramData.from_df(pd.DataFrame({"x": ["c", "b", "a"], "count": [4, 3, 2]})),
                    )
                ),
                metric=metric,
            ),
        },
    )


@metric
def classification_confusion_matrix():
    return TestMetric(
        name="classification_confusion_matrix",
        metric=ClassificationConfusionMatrix(),
        fingerprint="d60bb3a9b294941f6b0f4cd8987dd80f",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_confusion_matrix_values():
    metric = ClassificationConfusionMatrix()

    return TestMetric(
        name="classification_confusion_matrix_values",
        metric=metric,
        fingerprint="d60bb3a9b294941f6b0f4cd8987dd80f",
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                        prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
                    )
                ),
            ): AssertExpectedResult(
                ClassificationConfusionMatrixResult(
                    current_matrix=ConfusionMatrix(
                        labels=["a", "b", "c"],
                        values=[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                    )
                ),
                metric,
            ),
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["a", "a", "a", "a", "a", "b", "b", "b", "b"],
                        prediction=["a", "b", "b", "a", "b", "a", "a", "b", "b"],
                    )
                ),
            ): AssertExpectedResult(
                ClassificationConfusionMatrixResult(
                    current_matrix=ConfusionMatrix(
                        labels=["a", "b"],
                        values=[[2, 3], [2, 2]],
                    )
                ),
                metric,
            ),
            TestDataset(
                current=pd.DataFrame(
                    data=dict(
                        target=["c", "c", "c", "b", "b", "b", "a", "a", "a"],
                        prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
                    )
                ),
            ): AssertExpectedResult(
                ClassificationConfusionMatrixResult(
                    current_matrix=ConfusionMatrix(
                        labels=["a", "b", "c"],
                        values=[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                    )
                ),
                metric,
            ),
        },
    )


@metric
def classification_roc_curve():
    return TestMetric(
        name="classification_roc_curve",
        metric=ClassificationRocCurve(),
        fingerprint="3e0fe7518013e22decb9c10112d510e4",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_roc_curve_values():
    return TestMetric(
        name="classification_roc_curve_values",
        metric=ClassificationRocCurve(),
        fingerprint="3e0fe7518013e22decb9c10112d510e4",
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
            ): NoopOutcome()
        },
    )


@metric
def classification_quality_metric():
    return TestMetric(
        name="classification_quality_metric",
        metric=ClassificationQualityMetric(),
        fingerprint="e51bbc9c07a84af5602698e1951b57f2",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
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
        name="classification_quality_values",
        metric=metric,
        fingerprint="e51bbc9c07a84af5602698e1951b57f2",
        outcomes={
            TestDataset(current=current, column_mapping=ColumnMapping()): AssertExpectedResult(
                ClassificationQualityMetricResult(
                    current=make_approx_type(DatasetClassificationQuality)(
                        accuracy=approx_result(0.3333333),
                        precision=approx_result(0.3333333),
                        f1=approx_result(0.3333333),
                        recall=approx_result(0.3333333),
                    ),
                    target_name="target",
                ),
                metric,
            ),
            TestDataset("binary", current=current_binary, column_mapping=ColumnMapping()): AssertExpectedResult(
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
                metric,
            ),
        },
    )


@metric
def classification_quality_by_feature_table():
    return TestMetric(
        name="classification_quality_by_feature_table",
        metric=ClassificationQualityByFeatureTable(),
        fingerprint="f01dde05a091e869024491a147f04125",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_prob_distribution():
    return TestMetric(
        name="classification_prob_distribution",
        metric=ClassificationProbDistribution(),
        fingerprint="0a9e3dd9697d753e27c5ccd90aa5fba0",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_prob_distribution_values():
    return TestMetric(
        name="classification_prob_distribution_values",
        metric=ClassificationProbDistribution(),
        fingerprint="0a9e3dd9697d753e27c5ccd90aa5fba0",
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    data={
                        "target": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                        "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
                        "b": [0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
                        "c": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
                    },
                ),
                reference=None,
                column_mapping=ColumnMapping(prediction=["a", "b", "c"]),
            ): NoopOutcome(),
            TestDataset(
                current=pd.DataFrame(
                    data={
                        "my_target": ["a", np.NaN, "a", "b", "b", "c"],
                        "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2],
                        "b": [0.1, 0.2, 0.7, np.NaN, 0.8, 0.3],
                        "c": [0.1, 0.1, 0.1, 0.1, 0.1, np.NaN],
                    },
                ),
                reference=pd.DataFrame(
                    data={
                        "my_target": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                        "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
                        "b": [0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
                        "c": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
                    },
                ),
                column_mapping=ColumnMapping(target="my_target", prediction=["a", "b", "c"]),
            ): NoopOutcome(),
        },
    )


@metric
def classification_dummy_metric():
    return TestMetric(
        name="classification_dummy_metric",
        metric=ClassificationDummyMetric(),
        fingerprint="24f47aab253d5d8229ed82df4158b5cf",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )
