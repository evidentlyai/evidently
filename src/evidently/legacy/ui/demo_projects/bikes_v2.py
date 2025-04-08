from datetime import datetime
from datetime import timedelta
from typing import Tuple

from pandas import DataFrame

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.report import Report
from evidently.legacy import metrics
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.ui.dashboards import CounterAgg
from evidently.legacy.ui.dashboards import DashboardPanelCounter
from evidently.legacy.ui.dashboards import DashboardPanelPlot
from evidently.legacy.ui.dashboards import PanelValue
from evidently.legacy.ui.dashboards import PlotType
from evidently.legacy.ui.dashboards import ReportFilter
from evidently.legacy.ui.demo_projects import DemoProject
from evidently.legacy.ui.demo_projects.bikes import create_data
from evidently.legacy.ui.workspace.base import WorkspaceBase
from evidently.metrics.column_statistics import MaxValue
from evidently.metrics.column_statistics import MeanValue
from evidently.metrics.column_statistics import MedianValue
from evidently.metrics.column_statistics import MinValue
from evidently.metrics.column_statistics import QuantileValue
from evidently.metrics.column_statistics import StdValue
from evidently.tests import gte
from evidently.tests import lte
from evidently.ui.backport import snapshot_v2_to_v1


def create_snapshot(i: int, data: Tuple[DataFrame, DataFrame, ColumnMapping]):
    current, reference, column_mapping = data
    if column_mapping.numerical_features is None or len(column_mapping.numerical_features) < 1:
        raise ValueError("ColumnMapping must have at least one numerical feature")

    report = Report(
        [
            MinValue(column=column_mapping.numerical_features[0], tests=[lte(0.2), gte(2)]),
            MaxValue(column=column_mapping.numerical_features[0]),
            MedianValue(column=column_mapping.numerical_features[0]),
            MeanValue(column=column_mapping.numerical_features[0]),
            StdValue(column=column_mapping.numerical_features[0]),
            QuantileValue(column=column_mapping.numerical_features[0]),
            QuantileValue(column=column_mapping.numerical_features[0], quantile=0.95),
        ]
    )

    # report.set_batch_size("daily")

    data_chunk = current.loc[datetime(2023, 1, 29) + timedelta(days=i) : datetime(2023, 1, 29) + timedelta(i + 1)]

    dataset = Dataset.from_pandas(
        data=data_chunk,
        data_definition=DataDefinition(
            numerical_columns=column_mapping.numerical_features,
            categorical_columns=column_mapping.categorical_features,
            text_columns=column_mapping.text_features,
        ),
    )

    snapshot = report.run(dataset, None)

    return snapshot_v2_to_v1(snapshot)


def noop():
    pass


def create_project(workspace: WorkspaceBase, name: str):
    project = workspace.create_project(name)
    project.description = "A toy demo project using Bike Demand forecasting dataset"

    # feel free to change
    is_create_dashboard = False

    if is_create_dashboard:
        project.dashboard.add_panel(
            DashboardPanelCounter(
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                agg=CounterAgg.NONE,
                title="Bike Rental Demand Forecast",
            )
        )

        project.dashboard.add_panel(
            DashboardPanelCounter(
                title="Model Calls",
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                value=PanelValue(
                    metric_id="DatasetSummaryMetric",
                    field_path=metrics.DatasetSummaryMetric.fields.current.number_of_rows,
                    legend="count",
                ),
                text="count",
                agg=CounterAgg.SUM,
                size=WidgetSize.HALF,
            )
        )
        project.dashboard.add_panel(
            DashboardPanelCounter(
                title="Share of Drifted Features",
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                value=PanelValue(
                    metric_id="DatasetDriftMetric",
                    field_path="share_of_drifted_columns",
                    legend="share",
                ),
                text="share",
                agg=CounterAgg.LAST,
                size=WidgetSize.HALF,
            )
        )
        project.dashboard.add_panel(
            DashboardPanelPlot(
                title="Target and Prediction",
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                values=[
                    PanelValue(
                        metric_id="ColumnSummaryMetric",
                        field_path="current_characteristics.mean",
                        metric_args={"column_name.name": "cnt"},
                        legend="Target (daily mean)",
                    ),
                    PanelValue(
                        metric_id="ColumnSummaryMetric",
                        field_path="current_characteristics.mean",
                        metric_args={"column_name.name": "prediction"},
                        legend="Prediction (daily mean)",
                    ),
                ],
                plot_type=PlotType.LINE,
                size=WidgetSize.FULL,
            )
        )
        project.dashboard.add_panel(
            DashboardPanelPlot(
                title="MAE",
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                values=[
                    PanelValue(
                        metric_id="RegressionQualityMetric",
                        field_path=metrics.RegressionQualityMetric.fields.current.mean_abs_error,
                        legend="MAE",
                    ),
                ],
                plot_type=PlotType.LINE,
                size=WidgetSize.HALF,
            )
        )
        project.dashboard.add_panel(
            DashboardPanelPlot(
                title="MAPE",
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                values=[
                    PanelValue(
                        metric_id="RegressionQualityMetric",
                        field_path=metrics.RegressionQualityMetric.fields.current.mean_abs_perc_error,
                        legend="MAPE",
                    ),
                ],
                plot_type=PlotType.LINE,
                size=WidgetSize.HALF,
            )
        )
        project.dashboard.add_panel(
            DashboardPanelPlot(
                title="Features Drift (Wasserstein Distance)",
                filter=ReportFilter(metadata_values={}, tag_values=[]),
                values=[
                    PanelValue(
                        metric_id="ColumnDriftMetric",
                        metric_args={"column_name.name": "temp"},
                        field_path=metrics.ColumnDriftMetric.fields.drift_score,
                        legend="temp",
                    ),
                    PanelValue(
                        metric_id="ColumnDriftMetric",
                        metric_args={"column_name.name": "atemp"},
                        field_path=metrics.ColumnDriftMetric.fields.drift_score,
                        legend="atemp",
                    ),
                    PanelValue(
                        metric_id="ColumnDriftMetric",
                        metric_args={"column_name.name": "hum"},
                        field_path=metrics.ColumnDriftMetric.fields.drift_score,
                        legend="hum",
                    ),
                    PanelValue(
                        metric_id="ColumnDriftMetric",
                        metric_args={"column_name.name": "windspeed"},
                        field_path=metrics.ColumnDriftMetric.fields.drift_score,
                        legend="windspeed",
                    ),
                ],
                plot_type=PlotType.LINE,
                size=WidgetSize.FULL,
            )
        )
        project.save()
    return project


bikes_v2_demo_project = DemoProject(
    name="Demo project - Bikes v2",
    create_data=create_data,
    create_snapshot=create_snapshot,
    create_report=None,
    create_test_suite=None,
    create_project=create_project,
    count=28,
)
