from datetime import datetime
from datetime import timedelta

import numpy as np
from sklearn import datasets

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import MulticlassClassification
from evidently.core.report import Report
from evidently.descriptors import NonLetterCharacterPercentage
from evidently.descriptors import OOVWordsPercentage
from evidently.descriptors import RegExp
from evidently.descriptors import Sentiment
from evidently.descriptors import TextLength
from evidently.descriptors import TriggerWordsPresent
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.ui.dashboards import CounterAgg
from evidently.legacy.ui.dashboards import DashboardPanelCounter
from evidently.legacy.ui.dashboards import DashboardPanelPlot
from evidently.legacy.ui.dashboards import PanelValue
from evidently.legacy.ui.dashboards import PlotType
from evidently.legacy.ui.dashboards import ReportFilter
from evidently.legacy.ui.demo_projects.base import DemoProject
from evidently.legacy.ui.workspace.base import WorkspaceBase
from evidently.metrics import ValueDrift
from evidently.metrics.classification import Precision
from evidently.metrics.column_statistics import CategoryCount
from evidently.metrics.column_statistics import InRangeValueCount
from evidently.metrics.column_statistics import MeanValue
from evidently.metrics.dataset_statistics import ColumnCount
from evidently.metrics.dataset_statistics import RowCount
from evidently.presets import ClassificationQuality
from evidently.presets import DatasetStats
from evidently.ui.backport import snapshot_v2_to_v1


def create_snapshot(i: int, data):
    current, reference = data

    text_report = Report(
        [
            DatasetStats(),
            ClassificationQuality(),
            ValueDrift(column="prediction"),
            ValueDrift(column="Rating"),
            ValueDrift(column="Age"),
            ValueDrift(column="Positive_Feedback_Count"),
            ValueDrift(column="Division_Name"),
            ValueDrift(column="Class_Name"),
            ValueDrift(column="Review_Text"),
            ValueDrift(column="Title"),
            MeanValue(column="OOV"),
            MeanValue(column="Non Letter Character Percentage"),
            MeanValue(column="Sentiment"),
            MeanValue(column="urls"),
            InRangeValueCount(column="TextLength in the Range", left=1, right=1000),
            CategoryCount(column="Rating", category=1),
            CategoryCount(column="Rating", category=5),
            CategoryCount(column="competitors", category=1),
        ],
        # timestamp=datetime(2023, 1, 29) + timedelta(days=i + 1),
    )
    # text_report.set_batch_size("daily")

    if i < 17:
        current_df = current.as_dataframe()
        current_df_batch = current_df.iloc[1000 * i : 1000 * (i + 1), :]

        data_definition = DataDefinition(
            text_columns=["Review_Text", "Title"],
            numerical_columns=[
                "Age",
                "Positive_Feedback_Count",
                "Rating",
                "prediction",
                "Non Letter Character Percentage",
                "Sentiment",
                "urls",
                "TextLength in the Range",
            ],
            categorical_columns=["Division_Name", "Department_Name", "Class_Name", "OOV"],
            classification=[MulticlassClassification(target="Rating", prediction_labels="prediction")],
        )

        current_batch_dataset = Dataset.from_pandas(current_df_batch, data_definition=data_definition)

        snapshot = text_report.run(
            reference_data=reference,
            current_data=current_batch_dataset,
        )

    else:
        current_df = current.as_dataframe()
        current_df_batch = current_df[(current_df.Rating < 5)]

        data_definition = DataDefinition(
            text_columns=["Review_Text", "Title"],
            numerical_columns=[
                "Age",
                "Positive_Feedback_Count",
                "Rating",
                "prediction",
                "Non Letter Character Percentage",
                "Sentiment",
                "urls",
                "TextLength in the Range",
            ],
            categorical_columns=["Division_Name", "Department_Name", "Class_Name", "OOV"],
            classification=[MulticlassClassification(target="Rating", prediction_labels="prediction")],
        )

        current_batch_dataset = Dataset.from_pandas(current_df_batch, data_definition=data_definition)

        snapshot = text_report.run(
            reference_data=reference,
            current_data=current_batch_dataset,
        )

    v1_snapshot = snapshot_v2_to_v1(snapshot)
    v1_snapshot.timestamp = datetime(2024, 1, 29) + timedelta(days=i + 1)

    return v1_snapshot


def create_project(workspace: WorkspaceBase, name: str):
    project = workspace.create_project(name)
    project.description = "A toy demo project using Bike Demand forecasting dataset"

    project.dashboard.panels = []

    # title
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Classification of E-commerce User Reviews",
        )
    )
    # counters
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Model Calls",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                # metric_id="DatasetSummaryMetric",
                metric_args={"metric.metric_id": RowCount().metric_id},
                field_path="value",
                legend="count",
            ),
            text="count",
            agg=CounterAgg.SUM,
            size=WidgetSize.HALF,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="[to be]Share of Drifted Features",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_args={"metric.metric_id": ColumnCount().metric_id},
                field_path="value",
                legend="count",
            ),
            text="count",
            agg=CounterAgg.LAST,
            size=WidgetSize.HALF,
        )
    )

    # Precision
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Model Precision",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": Precision().metric_id},
                    field_path="value",
                    legend="precision",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.FULL,
        )
    )

    # target and prediction drift
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Target and Prediction Drift (Jensen-Shannon distance) ",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": ValueDrift(column="prediction").metric_id},
                    field_path="value",
                    legend="prediction drift score",
                ),
                PanelValue(
                    metric_args={"metric.metric_id": ValueDrift(column="Rating").metric_id},
                    field_path="value",
                    legend="target drift score",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )

    # features drift
    # text
    values = []
    for col in ["Title", "Review_Text"]:
        values.append(
            PanelValue(
                metric_args={"metric.metric_id": ValueDrift(column=col).metric_id},
                field_path="value",
                legend=col,
            ),
        )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Data Drift: review texts (domain classifier ROC AUC) ",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=values,
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    # numerical
    values = []
    for col in ["Age", "Positive_Feedback_Count"]:
        values.append(
            PanelValue(
                metric_args={"metric.metric_id": ValueDrift(column=col).metric_id},
                field_path="value",
                legend=f"{col}",
            ),
        )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Data Drift: numerical features (Wasserstein distance)",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=values,
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    # categorical
    values = []
    for col in ["Division_Name", "Department_Name", "Class_Name"]:
        values.append(
            PanelValue(
                metric_args={"metric.metric_id": ValueDrift(column=col).metric_id},
                field_path="value",
                legend=col,
            ),
        )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Data Drift: categorical features (Jensen-Shannon distance)",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=values,
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )

    # Text quality
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Review Text Quality: % of out-of-vocabulary words",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": MeanValue(column="OOV").metric_id},
                    field_path="value",
                    legend="OOV % (mean)",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Review Text Quality: % of non-letter characters",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": MeanValue(column="Non Letter Character Percentage").metric_id},
                    field_path="value",
                    legend="NonLetterCharacter % (mean)",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Review Text Quality: share of non-empty reviews",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={
                        "metric.metric_id": InRangeValueCount(
                            column="TextLength in the Range", left=1, right=1000
                        ).metric_id
                    },
                    field_path="share",
                    legend="Reviews with 1-1000 symbols",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )

    # Average review sentiment
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title=" Review sentiment",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": MeanValue(column="Sentiment").metric_id},
                    field_path="value",
                    legend="sentiment (mean)",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    # Reviews that mention competitors
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Share of reviews mentioning 'TheOtherStore', 'AMajorCompetitor', 'AwesomeShop'",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": CategoryCount(column="competitors", category=1).metric_id},
                    field_path="share",
                    legend="reviews with competitors",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    # Reviews that mention url
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="[to be] Reviews with URLs distribution",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": MeanValue(column="urls").metric_id},
                    field_path="value",
                    legend="reviews with URLs",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    # Rating ratio
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title='Share of reviews ranked "1"',
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": CategoryCount(column="Rating", category=1).metric_id},
                    field_path="share",
                    legend='share of "1"',
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title='Share of reviews ranked "5"',
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_args={"metric.metric_id": CategoryCount(column="Rating", category=5).metric_id},
                    field_path="share",
                    legend='share of "5"',
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        )
    )

    project.save()
    return project


def create_data():
    reviews_data = datasets.fetch_openml(name="Womens-E-Commerce-Clothing-Reviews", version=2, as_frame="auto")
    reviews = reviews_data.frame
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
    current = reviews.sample(n=5000, replace=True, ignore_index=True, random_state=142)

    data_definition = DataDefinition(
        text_columns=["Review_Text", "Title"],
        numerical_columns=["Age", "Positive_Feedback_Count", "Rating", "prediction"],
        categorical_columns=["Division_Name", "Department_Name", "Class_Name"],
        classification=[MulticlassClassification(target="Rating", prediction_labels="prediction")],
    )

    ref_dataset = Dataset.from_pandas(
        reference,
        data_definition=data_definition,
        descriptors=[
            TextLength("Review_Text", alias="TextLength in the Range"),
            NonLetterCharacterPercentage("Review_Text", alias="Non Letter Character Percentage"),
            OOVWordsPercentage("Review_Text", alias="OOV"),
            RegExp("Review_Text", reg_exp=r".*(http|www)\S+.*", alias="urls"),
            Sentiment("Review_Text", alias="Sentiment"),
            TriggerWordsPresent(
                "Review_Text",
                alias="competitors",
                words_list=["theotherstore", "amajorcompetitor", "awesomeshop"],
                lemmatize=False,
            ),
        ],
    )

    data_definition = DataDefinition(
        text_columns=["Review_Text", "Title"],
        numerical_columns=["Age", "Positive_Feedback_Count", "Rating", "prediction"],
        categorical_columns=["Division_Name", "Department_Name", "Class_Name"],
        classification=[MulticlassClassification(target="Rating", prediction_labels="prediction")],
    )

    cur_dataset = Dataset.from_pandas(
        current,
        data_definition=data_definition,
        descriptors=[
            TextLength("Review_Text", alias="TextLength in the Range"),
            NonLetterCharacterPercentage("Review_Text", alias="Non Letter Character Percentage"),
            OOVWordsPercentage("Review_Text", alias="OOV"),
            RegExp("Review_Text", reg_exp=r".*(http|www)\S+.*", alias="urls"),
            Sentiment("Review_Text", alias="Sentiment"),
            TriggerWordsPresent(
                "Review_Text",
                alias="competitors",
                words_list=["theotherstore", "amajorcompetitor", "awesomeshop"],
                lemmatize=False,
            ),
        ],
    )

    return ref_dataset, cur_dataset, ColumnMapping()


reviews_v2_demo_project = DemoProject(
    name="Demo project - Reviews v2",
    create_data=create_data,
    create_snapshot=create_snapshot,
    create_report=None,
    create_test_suite=None,
    create_project=create_project,
    count=5,
)
