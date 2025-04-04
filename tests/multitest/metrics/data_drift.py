import pandas as pd
from pytest import approx
from sklearn import datasets
from sklearn.datasets import fetch_20newsgroups

from evidently.legacy.calculation_engine.python_engine import PythonEngine
from evidently.legacy.calculations.data_drift import ColumnDataDriftMetrics
from evidently.legacy.calculations.data_drift import DriftStatsField
from evidently.legacy.calculations.stattests import StatTest
from evidently.legacy.calculations.stattests import psi_stat_test
from evidently.legacy.calculations.stattests.registry import _impls
from evidently.legacy.calculations.stattests.registry import add_stattest_impl
from evidently.legacy.core import ColumnType
from evidently.legacy.metric_results import Distribution
from evidently.legacy.metric_results import DistributionIncluded
from evidently.legacy.metrics import ColumnInteractionPlot
from evidently.legacy.metrics.data_drift.column_drift_metric import ColumnDriftMetric
from evidently.legacy.metrics.data_drift.column_value_plot import ColumnValuePlot
from evidently.legacy.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.legacy.metrics.data_drift.dataset_drift_metric import DatasetDriftMetric
from evidently.legacy.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetric
from evidently.legacy.metrics.data_drift.feature_importance import FeatureImportanceMetric
from evidently.legacy.metrics.data_drift.target_by_features_table import TargetByFeaturesTable
from evidently.legacy.metrics.data_drift.text_descriptors_drift_metric import TextDescriptorsDriftMetric
from evidently.legacy.metrics.data_drift.text_domain_classifier_drift_metric import TextDomainClassifierDriftMetric
from evidently.legacy.metrics.data_drift.text_metric import Comment
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.tests.utils import approx_result
from tests.conftest import slow
from tests.multitest.conftest import AssertExpectedResult
from tests.multitest.conftest import AssertResultFields
from tests.multitest.conftest import NoopOutcome
from tests.multitest.conftest import make_approx_type
from tests.multitest.datasets import DatasetTags
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def comment():
    return TestMetric(
        name="comment",
        metric=Comment(""),
        fingerprint="9357c4a1ebf5fb78e4f005cdf6ad8d7c",
        outcomes=NoopOutcome(),
    )


@metric
def feature_importance():
    return TestMetric(
        name="feature_importance",
        metric=FeatureImportanceMetric(),
        fingerprint="d0c2670a5a1c56ac4573c5db5650cba2",
        outcomes=NoopOutcome(),
        dataset_names=["bcancer"],
    )


@metric
def data_drift_table():
    return TestMetric(
        name="data_drift_table",
        metric=DataDriftTable(),
        fingerprint="8c49b4dcadf84ddd94342d386ee3f214",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_plot():
    return TestMetric(
        name="column_value_plot",
        metric=ColumnValuePlot("age"),
        fingerprint="d20c6d228a8204a329dcd4b368cc4b1c",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_drift_metric():
    return TestMetric(
        name="dataset_drift_metric",
        metric=DatasetDriftMetric(),
        fingerprint="eb75be4bf9fbac23ed47059053232258",
        outcomes=NoopOutcome(),
    )


@metric
def target_by_features_table():
    return TestMetric(
        name="target_by_features_table",
        metric=TargetByFeaturesTable(),
        fingerprint="1f004c7a2ac94f5e4f03548f759b549b",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_drift_metric():
    return TestMetric(
        name="text_descriptors_drift_metric",
        metric=TextDescriptorsDriftMetric(column_name="Review_Text"),
        fingerprint="1cbb29d0cd0609b21b2a218fed3a6e04",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_drift_metric():
    return TestMetric(
        name="column_drift_metric",
        metric=ColumnDriftMetric("age"),
        fingerprint="539cca77a886f183975a676fc4a7424d",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_drift_metric_values():
    test_stattest = StatTest(
        name="test_stattest",
        display_name="test stattest",
        allowed_feature_types=[ColumnType.Numerical],
        default_threshold=0.05,
    )
    add_stattest_impl(test_stattest, PythonEngine, _impls[psi_stat_test][PythonEngine])

    return [
        TestMetric(
            name="column_drift_metric_values",
            metric=ColumnDriftMetric(column_name="col"),
            fingerprint="87fac12514cb22bb4417157f9afac1d5",
            outcomes={
                TestDataset(
                    current=pd.DataFrame({"col": [1, 2, 3]}),
                    reference=pd.DataFrame({"col": [1, 2, 3]}),
                ): AssertExpectedResult(
                    ColumnDataDriftMetrics(
                        column_name="col",
                        column_type="cat",
                        drift_detected=False,
                        drift_score=1.0,
                        stattest_name="chi-square p_value",
                        stattest_threshold=0.05,
                        current=DriftStatsField(
                            distribution=Distribution(x=[1, 2, 3], y=[1, 1, 1]),
                            small_distribution=DistributionIncluded(x=[1, 2, 3], y=[1, 1, 1]),
                        ),
                        reference=DriftStatsField(
                            distribution=Distribution(x=[1, 2, 3], y=[1, 1, 1]),
                            small_distribution=DistributionIncluded(x=[1, 2, 3], y=[1, 1, 1]),
                        ),
                    )
                )
            },
        ),
        TestMetric(
            name="column_drift_metric_values",
            metric=ColumnDriftMetric(column_name="col"),
            fingerprint="87fac12514cb22bb4417157f9afac1d5",
            outcomes={
                TestDataset(
                    current=pd.DataFrame({"col": [5, 8, 3]}),
                    reference=pd.DataFrame({"col": [1, 2, 3]}),
                ): AssertExpectedResult(
                    ColumnDataDriftMetrics(
                        column_name="col",
                        column_type="cat",
                        drift_detected=True,
                        drift_score=0.0,
                        stattest_name="chi-square p_value",
                        stattest_threshold=0.05,
                        current=DriftStatsField(
                            small_distribution=DistributionIncluded(x=[1, 2, 3, 5, 8], y=[0, 0, 1, 1, 1]),
                            distribution=Distribution(x=[5, 8, 3], y=[1, 1, 1]),
                        ),
                        reference=DriftStatsField(
                            small_distribution=DistributionIncluded(x=[1, 2, 3, 5, 8], y=[1, 1, 1, 0, 0]),
                            distribution=Distribution(
                                x=[1, 2, 3],
                                y=[
                                    1,
                                    1,
                                    1,
                                ],
                            ),
                        ),
                    )
                )
            },
        ),
        TestMetric(
            name="column_drift_metric_values",
            metric=ColumnDriftMetric(column_name="col", stattest="psi", stattest_threshold=0.1),
            fingerprint="2a8347b6245c9ec8de2fba8d36c45716",
            outcomes={
                TestDataset(
                    current=pd.DataFrame({"col": [1, 2, 3]}),
                    reference=pd.DataFrame({"col": [3, 2, 2]}),
                ): AssertExpectedResult(
                    make_approx_type(ColumnDataDriftMetrics, ignore_not_set=True)(
                        column_name="col",
                        column_type="cat",
                        drift_detected=True,
                        drift_score=approx_result(2.93, absolute=0.01),
                        stattest_name="PSI",
                        stattest_threshold=0.1,
                        current=DriftStatsField(
                            distribution=Distribution(x=[1, 2, 3], y=[1, 1, 1]),
                            small_distribution=DistributionIncluded(x=[1, 2, 3], y=[1, 1, 1]),
                        ),
                        reference=DriftStatsField(
                            distribution=Distribution(x=[2, 3], y=[2, 1]),
                            small_distribution=DistributionIncluded(x=[1, 2, 3], y=[0, 2, 1]),
                        ),
                    )
                )
            },
        ),
        TestMetric(
            name="column_drift_metric_values",
            metric=ColumnDriftMetric(column_name="col", stattest=test_stattest, stattest_threshold=0.1),
            fingerprint="fc57cfacae72e747b972ffbf123c5b5c",
            outcomes={
                TestDataset(
                    current=pd.DataFrame({"col": [1, 2, 3]}),
                    reference=pd.DataFrame({"col": [3, 2, 2]}),
                ): AssertExpectedResult(
                    make_approx_type(ColumnDataDriftMetrics, ignore_not_set=True)(
                        column_name="col",
                        column_type="cat",
                        drift_detected=True,
                        drift_score=approx_result(2.93, absolute=0.01),
                        stattest_name="test stattest",
                        stattest_threshold=0.1,
                        current=DriftStatsField(
                            distribution=Distribution(x=[1, 2, 3], y=[1, 1, 1]),
                            small_distribution=DistributionIncluded(x=[1, 2, 3], y=[1, 1, 1]),
                        ),
                        reference=DriftStatsField(
                            distribution=Distribution(x=[2, 3], y=[2, 1]),
                            small_distribution=DistributionIncluded(x=[1, 2, 3], y=[0, 2, 1]),
                        ),
                    )
                )
            },
        ),
    ]


@metric
def column_interaction_plot():
    return TestMetric(
        name="column_interaction_plot",
        metric=ColumnInteractionPlot("age", "education"),
        fingerprint="37807d9f3c3b85b17ddaefc7079ae7ec",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


def embeddings_dataset():
    embeddings_data = datasets.fetch_lfw_people()
    embeddings_data = pd.DataFrame(embeddings_data["data"])
    embeddings_data.columns = ["col_" + str(x) for x in embeddings_data.columns]

    embeddings_data = embeddings_data.iloc[:5100, :31]

    embeddings_data_shifted = embeddings_data.copy()
    embeddings_data_shifted.iloc[2500:5000, :5] = 0

    column_mapping = ColumnMapping(
        embeddings={"small_subset": embeddings_data.columns[:10], "big_subset": embeddings_data.columns[10:29]},
        target=embeddings_data.columns[30],
    )

    return TestDataset(
        "embeddings_data",
        current=embeddings_data[2500:5000],
        reference=embeddings_data[:2500],
        column_mapping=column_mapping,
    )


@metric
def embeddings_drift_metric():
    return TestMetric(
        name="embeddings_drift_metric",
        metric=EmbeddingsDriftMetric("small_subset"),
        fingerprint="c43052a6a99ece41e40153fc4f46b1b2",
        outcomes=NoopOutcome(),
        datasets=[embeddings_dataset()],
        marks=[slow],
    )


@metric
def text_domain_classifier_drift_metric():
    categories_ref = ["alt.atheism", "talk.religion.misc"]
    categories_cur = ["comp.graphics", "sci.space"]
    reference = fetch_20newsgroups(subset="train", remove=("headers", "footers", "quotes"), categories=categories_ref)
    current = fetch_20newsgroups(subset="test", remove=("headers", "footers", "quotes"), categories=categories_cur)
    reference_data = pd.DataFrame({"text": reference.data})
    current_data = pd.DataFrame({"text": current.data})

    return TestMetric(
        name="text_domain_classifier_drift_metric",
        metric=TextDomainClassifierDriftMetric(text_column_name="text"),
        fingerprint="a283d9e03e192687ab7a59194503236e",
        outcomes=AssertResultFields(
            {
                "text_column_name": "text",
                "domain_classifier_roc_auc": approx(0.91, abs=0.02),
                "random_classifier_95_percentile": approx(0.53, abs=0.01),
                "content_drift": True,
            }
        ),
        datasets=[
            TestDataset(
                "text_domain_classifier_drift_metric_data", current=current_data, reference=reference_data, tags=[]
            ),
        ],
    )
