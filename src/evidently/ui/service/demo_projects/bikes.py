import io
import os
import zipfile
from datetime import datetime
from datetime import time
from datetime import timedelta
from itertools import cycle
from typing import Tuple

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from sklearn import ensemble

from evidently import Regression
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.report import Report
from evidently.presets import DataDriftPreset
from evidently.presets import DataSummaryPreset
from evidently.presets import RegressionPreset
from evidently.sdk.models import PanelMetric
from evidently.sdk.panels import counter_panel
from evidently.sdk.panels import line_plot_panel
from evidently.sdk.panels import text_panel
from evidently.ui.service.demo_projects import DemoProject
from evidently.ui.workspace import WorkspaceBase


def create_data():
    if os.path.exists("Bike-Sharing-Dataset.zip"):
        with open("Bike-Sharing-Dataset.zip", "rb") as f:
            content = f.read()
    else:
        content = requests.get(
            "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip",
            verify=False,
        ).content
    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        raw_data = pd.read_csv(
            arc.open("hour.csv"),
            header=0,
            sep=",",
            parse_dates=["dteday"],
            index_col="dteday",
        )

        raw_data.index = raw_data.apply(
            lambda row: datetime.combine(row.name, time(hour=int(row["hr"]))) + relativedelta(years=11),
            axis=1,
        )
        raw_data.sort_index(inplace=True)

    reference = raw_data.loc["2023-01-01 00:00:00":"2023-01-28 23:00:00"]
    current = raw_data.loc["2023-01-29 00:00:00":"2023-02-28 23:00:00"]

    target = "cnt"
    prediction = "prediction"
    numerical_columns = ["temp", "atemp", "hum", "windspeed", "hr", "weekday"]
    categorical_columns = ["season", "holiday", "workingday"]

    regressor = ensemble.RandomForestRegressor(random_state=0, n_estimators=50)
    regressor.fit(reference[numerical_columns + categorical_columns], reference[target])

    reference["prediction"] = regressor.predict(reference[numerical_columns + categorical_columns])
    current["prediction"] = regressor.predict(current[numerical_columns + categorical_columns])

    data_definition = DataDefinition(
        numerical_columns=numerical_columns + [target, prediction],
        categorical_columns=categorical_columns,
        regression=[Regression(target=target, prediction=prediction)],
    )

    return Dataset.from_pandas(current, data_definition), Dataset.from_pandas(reference, data_definition)


def snapshot_tags_generator():
    tags = [
        "production_critical",
        "city_bikes_hourly",
        "tabular_data",
        "regression_batch_model",
        "high_seasonality",
        "numerical_features",
        "categorical_features",
        "no_missing_values",
    ]

    yield from cycle(
        [
            [tags[0], tags[1], tags[2]],
            [tags[1]],
            [],
            [tags[2]],
            [tags[3], tags[4]],
            [],
            [tags[4], tags[5], tags[6], tags[7]],
            [],
            [],
        ]
    )


SNAPSHOT_TAGS = snapshot_tags_generator()


def next_snapshot_tags():
    return next(SNAPSHOT_TAGS)


def create_snapshot(i: int, data: Tuple[Dataset, Dataset]):
    current, reference = data
    report = Report(
        [
            DataSummaryPreset(),
            RegressionPreset(),
            DataDriftPreset(),
        ]
    )

    report.set_batch_size("daily")

    new_current = Dataset.from_pandas(
        data=current.as_dataframe()[
            datetime(2023, 1, 29) + timedelta(days=i) : datetime(2023, 1, 29) + timedelta(i + 1)
        ],
        data_definition=current.data_definition,
    )

    snapshot = report.run(
        new_current,
        reference,
        timestamp=datetime(2023, 1, 29) + timedelta(days=i + 1),
        tags=next_snapshot_tags(),
    )

    return snapshot


def create_project(workspace: WorkspaceBase, name: str):
    projects = workspace.list_projects()
    existing_project = [p for p in projects if p.name == name]
    if len(existing_project) > 0:
        project = existing_project[0]
        return project

    project = workspace.create_project(name)
    project.description = "A toy demo project using Bike Demand forecasting dataset"

    # feel free to change
    is_create_dashboard = True

    if is_create_dashboard:
        project.dashboard.add_panel(text_panel(title="Bike Rental Demand Forecast"))

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
                title="Target and Prediction",
                values=[
                    PanelMetric(
                        legend="Target (daily mean)\ncolumn: {{column}}",
                        metric="evidently:metric_v2:MeanValue",
                        metric_labels={"column": "cnt"},
                    ),
                    PanelMetric(
                        legend="Prediction (daily mean)\ncolumn: {{column}}",
                        metric="evidently:metric_v2:MeanValue",
                        metric_labels={"column": "prediction"},
                    ),
                ],
                size="full",
            )
        )
        project.dashboard.add_panel(
            line_plot_panel(
                title="MAE",
                size="half",
                values=[
                    PanelMetric(
                        metric="evidently:metric_v2:MAE",
                        legend="MAE\nvalue type: {{value_type}}",
                    ),
                ],
            )
        )
        project.dashboard.add_panel(
            line_plot_panel(
                title="MAPE",
                size="half",
                values=[
                    PanelMetric(
                        metric="evidently:metric_v2:MAPE",
                        legend="MAPE\nvalue type: {{value_type}}",
                    ),
                ],
            )
        )
        project.dashboard.add_panel(
            line_plot_panel(
                title="Features Drift (Wasserstein Distance)",
                values=[
                    PanelMetric(
                        legend="temp",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "temp"},
                    ),
                    PanelMetric(
                        legend="atemp",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "atemp"},
                    ),
                    PanelMetric(
                        legend="hum",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "hum"},
                    ),
                    PanelMetric(
                        legend="windspeed",
                        metric="evidently:metric_v2:ValueDrift",
                        metric_labels={"column": "windspeed"},
                    ),
                ],
            )
        )
        project.save()
    return project


bikes_demo_project = DemoProject(
    name="Demo project - Bikes",
    create_data=create_data,
    create_snapshot=create_snapshot,
    create_project=create_project,
    count=28,
)
