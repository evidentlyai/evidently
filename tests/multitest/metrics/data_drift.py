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
        fingerprint="dbe49b0a28d93d2f881a8221ab0c712c",
        outcomes=NoopOutcome(),
    )


@metric
def feature_importance():
    return TestMetric(
        name="feature_importance",
        metric=FeatureImportanceMetric(),
        fingerprint="7434b61d4f3095f16b2ea6fd0bc1ade7",
        outcomes=NoopOutcome(),
        dataset_names=["bcancer"],
    )


@metric
def data_drift_table():
    return TestMetric(
        name="data_drift_table",
        metric=DataDriftTable(),
        fingerprint="f2770cd7b34f6f7ee8007063dc426b62",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_value_plot():
    return TestMetric(
        name="column_value_plot",
        metric=ColumnValuePlot("age"),
        fingerprint="73782ae02883d6917e1f2e81c5e309c7",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_drift_metric():
    return TestMetric(
        name="dataset_drift_metric",
        metric=DatasetDriftMetric(),
        fingerprint="810d22365ecfe39517d86f5f85f2d56a",
        outcomes=NoopOutcome(),
    )


@metric
def target_by_features_table():
    return TestMetric(
        name="target_by_features_table",
        metric=TargetByFeaturesTable(),
        fingerprint="28d0e88a55084aa6efeca039e37c32a0",
        outcomes=NoopOutcome(),
        include_tags=[DatasetTags.HAS_TARGET],
    )


@metric
def text_descriptors_drift_metric():
    return TestMetric(
        name="text_descriptors_drift_metric",
        metric=TextDescriptorsDriftMetric(column_name="Review_Text"),
        fingerprint="75944946f4ac5122a8393b468b961589",
        outcomes=NoopOutcome(),
        dataset_names=["reviews"],
        marks=[slow],
    )


@metric
def column_drift_metric():
    return TestMetric(
        name="column_drift_metric",
        metric=ColumnDriftMetric("age"),
        fingerprint="1fb00300367542cb96e1742294071124",
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
            fingerprint="442147b4c50a8bda1fca24930b1cbe72",
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
            fingerprint="442147b4c50a8bda1fca24930b1cbe72",
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
            fingerprint="4400d784ce122fa86628535a0a6d191e",
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
            fingerprint="ca8b2e8169a0fd43ff4ed52f5ec2b715",
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
        fingerprint="81f49907fcdd392fe421beefeb2837be",
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
        fingerprint="8aa4942fb793bd0dce286a0517b4b674",
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
        fingerprint="273ef9cd576700ebc024c0e98d9780ea",
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
