import pandas as pd
from pytest import approx
from sklearn import datasets
from sklearn.datasets import fetch_20newsgroups

from evidently.calculation_engine.python_engine import PythonEngine
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import DriftStatsField
from evidently.calculations.stattests import StatTest
from evidently.calculations.stattests import psi_stat_test
from evidently.calculations.stattests.registry import _impls
from evidently.calculations.stattests.registry import add_stattest_impl
from evidently.core import ColumnType
from evidently.metric_results import Distribution
from evidently.metric_results import DistributionIncluded
from evidently.metrics import ColumnInteractionPlot
from evidently.metrics.data_drift.column_drift_metric import ColumnDriftMetric
from evidently.metrics.data_drift.column_value_plot import ColumnValuePlot
from evidently.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.metrics.data_drift.dataset_drift_metric import DatasetDriftMetric
from evidently.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetric
from evidently.metrics.data_drift.feature_importance import FeatureImportanceMetric
from evidently.metrics.data_drift.target_by_features_table import TargetByFeaturesTable
from evidently.metrics.data_drift.text_descriptors_drift_metric import TextDescriptorsDriftMetric
from evidently.metrics.data_drift.text_domain_classifier_drift_metric import TextDomainClassifierDriftMetric
from evidently.metrics.data_drift.text_metric import Comment
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.tests.utils import approx_result
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
        fingerprint="70c9afc03c9b9462bb698d6f2cb324c2",
        outcomes=NoopOutcome(),
    )


@metric
def feature_importance():
    return TestMetric(
        name="feature_importance",
        metric=FeatureImportanceMetric(),
        fingerprint="374130b75be647e96d0bf12a8ff44d2b",
        outcomes=NoopOutcome(),
        dataset_names=["bcancer"],
    )


@metric
def data_drift_table():
    return TestMetric(
        name="data_drift_table",
        metric=DataDriftTable(),
        fingerprint="1b7c7a7a5d02c75cbc6117b4959126ae",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_plot():
    return TestMetric(
        name="column_value_plot",
        metric=ColumnValuePlot("age"),
        fingerprint="1b07ca1ade67405170ba12ff004eb01a",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_drift_metric():
    return TestMetric(
        name="dataset_drift_metric",
        metric=DatasetDriftMetric(),
        fingerprint="248c833d76b543077d29c121773e597d",
        outcomes=NoopOutcome(),
    )


@metric
def target_by_features_table():
    return TestMetric(
        name="target_by_features_table",
        metric=TargetByFeaturesTable(),
        fingerprint="0c42b508685f82de5d9aca44e4da339d",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_drift_metric():
    return TestMetric(
        name="text_descriptors_drift_metric",
        metric=TextDescriptorsDriftMetric(column_name="Review_Text"),
        fingerprint="0453b9f12e296e6132382818342b7be9",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_drift_metric():
    return TestMetric(
        name="column_drift_metric",
        metric=ColumnDriftMetric("age"),
        fingerprint="aeab198cff7b829ea3708c65c1e27ff4",
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
            fingerprint="d4db5b0ce2c9344fd1fe7324a11d14b4",
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
            fingerprint="d4db5b0ce2c9344fd1fe7324a11d14b4",
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
            fingerprint="a2e27baefdeba9c5cd008b93ab9f1427",
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
            fingerprint="08d3ff3a4d29c37689cb4fc2fe349a36",
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
        fingerprint="d7438613c6fec94732ca923559da6ee4",
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
        fingerprint="f74a5a7a1aa8203bb86b1885899d3388",
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
        fingerprint="1281bc0b31336d868630b5714351ce28",
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
