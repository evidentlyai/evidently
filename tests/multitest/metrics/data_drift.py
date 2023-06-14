import pandas as pd
from sklearn import datasets
from sklearn.datasets import fetch_20newsgroups

from evidently import ColumnMapping
from evidently.metrics.data_drift.column_drift_metric import ColumnDriftMetric
from evidently.metrics.data_drift.column_value_plot import ColumnValuePlot
from evidently.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.metrics.data_drift.dataset_drift_metric import DatasetDriftMetric
from evidently.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetric
from evidently.metrics.data_drift.target_by_features_table import TargetByFeaturesTable
from evidently.metrics.data_drift.text_descriptors_drift_metric import TextDescriptorsDriftMetric
from evidently.metrics.data_drift.text_domain_classifier_drift_metric import TextDomainClassifierDriftMetric
from evidently.metrics.data_drift.text_metric import Comment
from tests.multitest.datasets import DatasetTags
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def comment():
    return TestMetric("comment", Comment(""))


@metric
def data_drift_table():
    return TestMetric("data_drift_table", DataDriftTable())


@metric
def column_value_plot():
    return TestMetric("column_value_plot", ColumnValuePlot("age"), dataset_names=["adult"])


@metric
def dataset_drift_metric():
    return TestMetric("dataset_drift_metric", DatasetDriftMetric())


@metric
def target_by_features_table():
    return TestMetric("target_by_features_table", TargetByFeaturesTable(), include_tags=[DatasetTags.HAS_TARGET])


@metric
def text_descriptors_drift_metric():
    return TestMetric(
        "text_descriptors_drift_metric",
        TextDescriptorsDriftMetric(column_name="Review_Text"),
        dataset_names=["reviews"],
    )


@metric
def column_drift_metric():
    return TestMetric("column_drift_metric", ColumnDriftMetric("age"), dataset_names=["adult"])


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
    return TestMetric("embeddings_drift_metric", EmbeddingsDriftMetric("small_subset"), datasets=[embeddings_dataset()])


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
        datasets=[
            TestDataset(
                "text_domain_classifier_drift_metric_data", current=current_data, reference=reference_data, tags=[]
            )
        ],
    )
