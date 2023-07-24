import pandas as pd
from pytest import approx
from sklearn import datasets
from sklearn.datasets import fetch_20newsgroups

from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import DriftStatsField
from evidently.calculations.stattests import StatTest
from evidently.calculations.stattests import psi_stat_test
from evidently.metric_results import Distribution
from evidently.metric_results import DistributionIncluded
from evidently.metrics import ColumnInteractionPlot
from evidently.metrics.data_drift.column_drift_metric import ColumnDriftMetric
from evidently.metrics.data_drift.column_value_plot import ColumnValuePlot
from evidently.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.metrics.data_drift.dataset_drift_metric import DatasetDriftMetric
from evidently.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetric
from evidently.metrics.data_drift.target_by_features_table import TargetByFeaturesTable
from evidently.metrics.data_drift.text_descriptors_drift_metric import TextDescriptorsDriftMetric
from evidently.metrics.data_drift.text_domain_classifier_drift_metric import TextDomainClassifierDriftMetric
from evidently.metrics.data_drift.text_metric import Comment
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.tests.utils import approx_result
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
        "comment",
        Comment(""),
        NoopOutcome(),
    )


@metric
def data_drift_table():
    return TestMetric("data_drift_table", DataDriftTable(), NoopOutcome())


@metric
def column_value_plot():
    return TestMetric("column_value_plot", ColumnValuePlot("age"), NoopOutcome(), dataset_names=["adult"])


@metric
def dataset_drift_metric():
    return TestMetric("dataset_drift_metric", DatasetDriftMetric(), NoopOutcome())


@metric
def target_by_features_table():
    return TestMetric(
        "target_by_features_table", TargetByFeaturesTable(), NoopOutcome(), include_tags=[DatasetTags.HAS_TARGET]
    )


@metric
def text_descriptors_drift_metric():
    return TestMetric(
        "text_descriptors_drift_metric",
        TextDescriptorsDriftMetric(column_name="Review_Text"),
        NoopOutcome(),
        dataset_names=["reviews"],
    )


@metric
def column_drift_metric():
    return TestMetric("column_drift_metric", ColumnDriftMetric("age"), NoopOutcome(), dataset_names=["adult"])


@metric
def column_drift_metric_values():
    test_stattest = StatTest(
        name="test_stattest",
        display_name="test stattest",
        func=psi_stat_test.func,
        allowed_feature_types=["num"],
        default_threshold=0.05,
    )

    return [
        TestMetric(
            "column_drift_metric_values",
            ColumnDriftMetric(column_name="col"),
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
            "column_drift_metric_values",
            ColumnDriftMetric(column_name="col"),
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
            "column_drift_metric_values",
            ColumnDriftMetric(column_name="col", stattest="psi", stattest_threshold=0.1),
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
        # TestMetric(
        #     "column_drift_metric_values",
        #     ColumnDriftMetric(column_name="col", stattest=test_stattest, stattest_threshold=0.1),
        #     outcomes={
        #         TestDataset(
        #             current=pd.DataFrame({"col": [1, 2, 3]}),
        #             reference=pd.DataFrame({"col": [3, 2, 2]}),
        #         ): AssertExpectedResult(
        #             make_approx_type(ColumnDataDriftMetrics, ignore_not_set=True)(
        #                 column_name="col",
        #                 column_type="cat",
        #                 drift_detected=True,
        #                 drift_score=approx_result(2.93, absolute=0.01),
        #                 stattest_name="test stattest",
        #                 stattest_threshold=0.1,
        #                 current=DriftStatsField(
        #                     distribution=Distribution(x=[1, 2, 3], y=[1, 1, 1]),
        #                     small_distribution=DistributionIncluded(x=[1, 2, 3], y=[1, 1, 1]),
        #                 ),
        #                 reference=DriftStatsField(
        #                     distribution=Distribution(x=[2, 3], y=[2, 1]),
        #                     small_distribution=DistributionIncluded(x=[1, 2, 3], y=[0, 2, 1]),
        #                 ),
        #             )
        #         )
        #     },
        # ),
    ]


@metric
def column_interaction_plot():
    return TestMetric(
        "column_interaction_plot",
        ColumnInteractionPlot("age", "education"),
        NoopOutcome(),
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
        "embeddings_drift_metric", EmbeddingsDriftMetric("small_subset"), NoopOutcome(), datasets=[embeddings_dataset()]
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
        "text_domain_classifier_drift_metric",
        TextDomainClassifierDriftMetric(text_column_name="text"),
        AssertResultFields(
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
