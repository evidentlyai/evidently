import os
import pathlib
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn import datasets

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import MulticlassClassification
from evidently.core.report import Report
from evidently.descriptors import NonLetterCharacterPercentage
from evidently.descriptors import OOVWordsPercentage
from evidently.descriptors import Sentiment
from evidently.descriptors import TextLength
from evidently.metrics import CategoryCount
from evidently.metrics import InRangeValueCount
from evidently.presets import ClassificationPreset
from evidently.presets import DataDriftPreset
from evidently.presets import DataSummaryPreset
from evidently.presets import TextEvals
from evidently.sdk.models import PanelMetric
from evidently.sdk.panels import counter_panel
from evidently.sdk.panels import line_plot_panel
from evidently.sdk.panels import text_panel
from evidently.ui.service.demo_projects import DemoProject
from evidently.ui.workspace import WorkspaceBase


def create_data():
    if os.environ.get("EVIDENTLY_TEST_ENVIRONMENT", "0") != "1":
        reviews_data = datasets.fetch_openml(name="Womens-E-Commerce-Clothing-Reviews", version=2, as_frame="auto")
        reviews = reviews_data.frame
    else:
        reviews = pd.read_parquet(pathlib.Path(__file__).parent.joinpath("../../../../../test_data/reviews.parquet"))

    for name, rs in (
        ("TheOtherStore", 0),
        ("AMajorCompetitor", 42),
        ("AwesomeShop", 100),
    ):
        np.random.seed(rs)
        random_index = np.random.choice(reviews.index, 300, replace=False)
        reviews.loc[random_index, "Review_Text"] = (
            reviews.loc[random_index, "Review_Text"] + f" mention competitor {name}"
        )

    np.random.seed(13)
    random_index = np.random.choice(reviews.index, 1000, replace=False)
    reviews.loc[random_index, "Review_Text"] = (
        reviews.loc[random_index, "Review_Text"] + " mention www.someurl.someurl "
    )
    reviews["prediction"] = reviews["Rating"]
    np.random.seed(0)
    random_index = np.random.choice(reviews.index, 2000, replace=False)
    reviews.loc[random_index, "prediction"] = 1
    reference = reviews.sample(n=5000, replace=True, ignore_index=True, random_state=42)
    current = reviews

    data_definition = DataDefinition(
        numerical_columns=["Age", "Positive_Feedback_Count"],
        categorical_columns=["Division_Name", "Department_Name", "Class_Name", "Rating", "prediction"],
        text_columns=["Review_Text", "Title"],
        classification=[
            MulticlassClassification(
                name="default",
                target="Rating",
                prediction_labels="prediction",
            )
        ],
    )

    current_dataset = Dataset.from_pandas(
        current,
        data_definition=data_definition,
        descriptors=[
            TextLength("Review_Text", alias="TextLength"),
            NonLetterCharacterPercentage("Review_Text", alias="NonLetterCharacterPercentage"),
            OOVWordsPercentage("Review_Text", alias="OOVWordsPercentage"),
            Sentiment("Review_Text", alias="Sentiment"),
        ],
    )
    reference_dataset = Dataset.from_pandas(
        reference,
        data_definition=data_definition,
        descriptors=[
            TextLength("Review_Text", alias="TextLength"),
            NonLetterCharacterPercentage("Review_Text", alias="NonLetterCharacterPercentage"),
            OOVWordsPercentage("Review_Text", alias="OOVWordsPercentage"),
            Sentiment("Review_Text", alias="Sentiment"),
        ],
    )

    return current_dataset, reference_dataset


def create_datasets() -> List[Tuple[Dataset, str, str]]:
    return [(create_data()[0], "Reviews Data", "E-commerce Reviews dataset")]


def create_snapshot(i: int, data: Tuple[Dataset, Dataset]):
    current, reference = data
    report = Report(
        [
            DataSummaryPreset(),
            ClassificationPreset(),
            DataDriftPreset(
                columns=[
                    "prediction",
                    "Rating",
                    "Age",
                    "Positive_Feedback_Count",
                    "Division_Name",
                    "Department_Name",
                    "Class_Name",
                    "Title",
                    "Review_Text",
                ]
            ),
            TextEvals(),
            InRangeValueCount(column="TextLength", left=1, right=1000),
            CategoryCount(column="Rating", category=1),
            CategoryCount(column="Rating", category=5),
        ]
    )

    report.set_batch_size("daily")

    current_df = current.as_dataframe()
    descriptor_columns = set(
        current.data_definition.numerical_descriptors + current.data_definition.categorical_descriptors
    )
    original_columns = [col for col in current_df.columns if col not in descriptor_columns]

    if i < 17:
        new_current_df = current_df[original_columns].iloc[1000 * i : 1000 * (i + 1)]
    else:
        new_current_df = current_df[original_columns][current_df[original_columns]["Rating"] < 5]

    new_current = Dataset.from_pandas(
        data=new_current_df,
        data_definition=current.data_definition,
        descriptors=[
            TextLength("Review_Text", alias="TextLength"),
            NonLetterCharacterPercentage("Review_Text", alias="NonLetterCharacterPercentage"),
            OOVWordsPercentage("Review_Text", alias="OOVWordsPercentage"),
            Sentiment("Review_Text", alias="Sentiment"),
        ],
    )

    snapshot = report.run(
        new_current,
        reference,
        timestamp=datetime(2023, 1, 29) + timedelta(days=i + 1),
    )

    return snapshot


def create_project(workspace: WorkspaceBase, name: str):
    projects = workspace.list_projects()
    existing_project = [p for p in projects if p.name == name]
    if len(existing_project) > 0:
        project = existing_project[0]
        return project

    project = workspace.create_project(name)
    project.description = "A toy demo project using E-commerce Reviews dataset. Text and tabular data, classification."

    is_create_dashboard = True

    if is_create_dashboard:
        project.dashboard.add_panel(text_panel(title="Classification of E-commerce User Reviews"))

        project.dashboard.add_panel(
            counter_panel(
                title="Model Calls",
                size="half",
                values=[
                    PanelMetric(legend="count", metric="evidently:metric_v2:RowCount", metric_labels={}),
                ],
                aggregation="sum",
            )
        )
        project.dashboard.add_panel(
            counter_panel(
                title="Share of Drifted Features",
                size="half",
                values=[
                    PanelMetric(
                        legend="share",
                        metric="evidently:metric_v2:DriftedColumnsCount",
                        metric_labels={"value_type": "share"},
                    ),
                ],
                aggregation="last",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Model Precision",
                values=[
                    PanelMetric(
                        metric="evidently:metric_v2:Precision",
                        legend="precision\nvalue type: {{value_type}}",
                    ),
                ],
                size="full",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Target and Prediction Drift (Jensen-Shannon distance)",
                values=[
                    PanelMetric(
                        legend="prediction drift score",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "prediction"},
                    ),
                    PanelMetric(
                        legend="target drift score",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Rating"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Data Drift: review texts (domain classifier ROC AUC)",
                values=[
                    PanelMetric(
                        legend="Title",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Title"},
                    ),
                    PanelMetric(
                        legend="Review_Text",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Review_Text"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Data Drift: numerical features (Wasserstein distance)",
                values=[
                    PanelMetric(
                        legend="Age",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Age"},
                    ),
                    PanelMetric(
                        legend="Positive_Feedback_Count",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Positive_Feedback_Count"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Data Drift: categorical features (Jensen-Shannon distance)",
                values=[
                    PanelMetric(
                        legend="Division_Name",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Division_Name"},
                    ),
                    PanelMetric(
                        legend="Department_Name",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Department_Name"},
                    ),
                    PanelMetric(
                        legend="Class_Name",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "Class_Name"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Review Text Quality: % of out-of-vocabulary words",
                values=[
                    PanelMetric(
                        legend="OOV % (mean)",
                        metric="evidently:metric_v2:MeanValue",
                        metric_labels={"column": "OOVWordsPercentage"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Review Text Quality: % of non-letter characters",
                values=[
                    PanelMetric(
                        legend="NonLetterCharacter % (mean)",
                        metric="evidently:metric_v2:MeanValue",
                        metric_labels={"column": "NonLetterCharacterPercentage"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Review Text Quality: share of non-empty reviews",
                values=[
                    PanelMetric(
                        legend="Reviews with 1-1000 symbols",
                        metric="evidently:metric_v2:InRangeValueCount",
                        metric_labels={"column": "TextLength", "left": "1", "right": "1000", "value_type": "share"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title="Review sentiment",
                values=[
                    PanelMetric(
                        legend="sentiment (mean)",
                        metric="evidently:metric_v2:MeanValue",
                        metric_labels={"column": "Sentiment"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title='Share of reviews ranked "1"',
                values=[
                    PanelMetric(
                        legend='share of "1"',
                        metric="evidently:metric_v2:CategoryCount",
                        metric_labels={"column": "Rating", "categories": "[1]", "value_type": "share"},
                    ),
                ],
                size="half",
            )
        )

        project.dashboard.add_panel(
            line_plot_panel(
                title='Share of reviews ranked "5"',
                values=[
                    PanelMetric(
                        legend='share of "5"',
                        metric="evidently:metric_v2:CategoryCount",
                        metric_labels={"column": "Rating", "categories": "[5]", "value_type": "share"},
                    ),
                ],
                size="half",
            )
        )

        project.save()
    return project


reviews_demo_project = DemoProject(
    name="Demo project - Reviews",
    create_data=create_data,
    create_snapshot=create_snapshot,
    create_project=create_project,
    create_datasets=create_datasets,
    count=19,
)
