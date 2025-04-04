import numpy as np
import pandas as pd

from evidently.legacy.metric_results import ConfusionMatrix
from evidently.legacy.metric_results import DatasetClassificationQuality
from evidently.legacy.metric_results import Histogram
from evidently.legacy.metric_results import HistogramData
from evidently.legacy.metrics.classification_performance.class_balance_metric import ClassificationClassBalance
from evidently.legacy.metrics.classification_performance.class_balance_metric import ClassificationClassBalanceResult
from evidently.legacy.metrics.classification_performance.class_separation_metric import (
    ClassificationClassSeparationPlot,
)
from evidently.legacy.metrics.classification_performance.classification_dummy_metric import ClassificationDummyMetric
from evidently.legacy.metrics.classification_performance.classification_quality_metric import (
    ClassificationQualityMetric,
)
from evidently.legacy.metrics.classification_performance.classification_quality_metric import (
    ClassificationQualityMetricResult,
)
from evidently.legacy.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrix
from evidently.legacy.metrics.classification_performance.confusion_matrix_metric import (
    ClassificationConfusionMatrixResult,
)
from evidently.legacy.metrics.classification_performance.lift_curve_metric import ClassificationLiftCurve
from evidently.legacy.metrics.classification_performance.lift_table_metric import ClassificationLiftTable
from evidently.legacy.metrics.classification_performance.pr_curve_metric import ClassificationPRCurve
from evidently.legacy.metrics.classification_performance.pr_table_metric import ClassificationPRTable
from evidently.legacy.metrics.classification_performance.probability_distribution_metric import (
    ClassificationProbDistribution,
)
from evidently.legacy.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClass
from evidently.legacy.metrics.classification_performance.quality_by_feature_table import (
    ClassificationQualityByFeatureTable,
)
from evidently.legacy.metrics.classification_performance.roc_curve_metric import ClassificationRocCurve
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.tests.utils import approx_result
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
        fingerprint="a238692f61349ce9193b72c393bd0669",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_table():
    return TestMetric(
        name="classification_p_r_table",
        metric=ClassificationPRTable(),
        fingerprint="9262b3e3a9764b1c45a3a8e6de4c82f0",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_table_values():
    m = ClassificationPRTable()
    return TestMetric(
        name="classification_p_r_table_values",
        metric=m,
        fingerprint="9262b3e3a9764b1c45a3a8e6de4c82f0",
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
        fingerprint="f768817940edb126f1bc6ec7e5c77a8a",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_lift_table():
    return TestMetric(
        name="classification_lift_table",
        metric=ClassificationLiftTable(),
        fingerprint="7998350645d85ef9a28039f6f4edb2d1",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_lift_curve():
    return TestMetric(
        name="classification_lift_curve",
        metric=ClassificationLiftCurve(),
        fingerprint="57fc202600628307b5c1d4ee01163982",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_p_r_curve_values():
    m = ClassificationPRCurve()
    return TestMetric(
        name="classification_p_r_curve_values",
        metric=m,
        fingerprint="f768817940edb126f1bc6ec7e5c77a8a",
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
        fingerprint="1a93c8f01b4e0ea01d78ef5b09ba7522",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_class_balance():
    return TestMetric(
        name="classification_class_balance",
        metric=ClassificationClassBalance(),
        fingerprint="cab9c98aee4aa4a678ab28d8c5907331",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_class_balance_values():
    metric = ClassificationClassBalance()

    return TestMetric(
        name="classification_class_balance_values",
        metric=metric,
        fingerprint="cab9c98aee4aa4a678ab28d8c5907331",
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
        fingerprint="7b2be6b2f70536034d41bbf6753b80f5",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_confusion_matrix_values():
    metric = ClassificationConfusionMatrix()

    return TestMetric(
        name="classification_confusion_matrix_values",
        metric=metric,
        fingerprint="7b2be6b2f70536034d41bbf6753b80f5",
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
        fingerprint="be3125d0b6a253770b6d612306166c4d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION, DatasetTags.BINARY_CLASSIFICATION, DatasetTags.PROB_PREDICTIONS],
    )


@metric
def classification_roc_curve_values():
    return TestMetric(
        name="classification_roc_curve_values",
        metric=ClassificationRocCurve(),
        fingerprint="be3125d0b6a253770b6d612306166c4d",
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
        fingerprint="aa8f28863b76b4886a0c28cdac4d7ba6",
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
        fingerprint="aa8f28863b76b4886a0c28cdac4d7ba6",
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
        fingerprint="ffc2075e84a940eaab0f9ce643a76686",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_prob_distribution():
    return TestMetric(
        name="classification_prob_distribution",
        metric=ClassificationProbDistribution(),
        fingerprint="9eb345021d523c50009760785863235e",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )


@metric
def classification_prob_distribution_values():
    return TestMetric(
        name="classification_prob_distribution_values",
        metric=ClassificationProbDistribution(),
        fingerprint="9eb345021d523c50009760785863235e",
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
                        "my_target": ["a", np.nan, "a", "b", "b", "c"],
                        "a": [0.8, 0.7, 0.3, 0.1, 0.2, 0.2],
                        "b": [0.1, 0.2, 0.7, np.nan, 0.8, 0.3],
                        "c": [0.1, 0.1, 0.1, 0.1, 0.1, np.nan],
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
        fingerprint="31a1ebd2ca7e5047d8ea65b3f451ece7",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.CLASSIFICATION],
    )
