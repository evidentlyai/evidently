from typing import List, Optional, Text

from evidently.metrics import ColumnDriftMetric
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently.metrics import RegressionQualityMetric
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.workspace import Project
from evidently.ui.dashboards import ReportFilter
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase

from config.evidently_config import EVIDENTLY_WS


def get_evidently_project(
    workspace: WorkspaceBase,
    project_name: Text,
    project_description: Optional[Text] = None
) -> Project:
    """Get Evidently project object (load existing or create new).

    Args:
        workspace (WorkspaceBase): Evidently workspace object.
        project_name (Text): name of a project
        project_description (Optional[Text], optional): Project description. Defaults to None.

    Returns:
        Project: Evidently project object.
    """

    # Search project by name in the workspace
    search_proj_list: List[Project] = workspace.search_project(project_name)

    # Check if project with specified name already exists
    if search_proj_list:
        project: Project = search_proj_list[0]
    # If it does not exit create it
    else:
        project = workspace.create_project(project_name)
        project.description = project_description

    return project


def add_regression_dashboard(project: Project) -> Project:
    """Add (build) model performance (regression) dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Regression performance
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Regression Performance",
        )
    )

    # RegressionQualityMetric ME value panel
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="ME",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="RegressionQualityMetric",
                field_path=RegressionQualityMetric.fields.current.mean_error,
                legend="value",
            ),
            text="value",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # RegressionQualityMetric MAE value panel
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="MAE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="RegressionQualityMetric",
                field_path=RegressionQualityMetric.fields.current.mean_abs_error,
                legend="value",
            ),
            text="value",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # RegressionQualityMetric aggregated metric (ME, MAE, MAPE) plots
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Aggregated metrics in time: ME and MAE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="RegressionQualityMetric",
                    field_path=RegressionQualityMetric.fields.current.mean_error,
                    legend="ME"
                ),
                PanelValue(
                    metric_id="RegressionQualityMetric",
                    field_path=RegressionQualityMetric.fields.current.mean_abs_error,
                    legend="MAE",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )

    # RegressionQualityMetric MAPE value panel
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="MAPE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="RegressionQualityMetric",
                field_path=RegressionQualityMetric.fields.current.mean_abs_perc_error,
                legend="value",
            ),
            text="value",
            agg=CounterAgg.LAST,
            size=2
        )
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Aggregated metrics in time: MAPE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="RegressionQualityMetric",
                    field_path=RegressionQualityMetric.fields.current.mean_abs_perc_error,
                    legend="MAPE",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )

    return project


def add_target_drift_dashboard(project: Project) -> Project:
    """Add (build) target drift dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Title: Target drift
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Target Drift",
        )
    )

    # Stattest threshold
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Stattest Threshold",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="ColumnDriftMetric",
                field_path=ColumnDriftMetric.fields.stattest_threshold,
                metric_args={"column_name.name": "duration_min"},
                legend="stattest threshold"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # Row counts
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Row counts",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetSummaryMetric",
                field_path=DatasetSummaryMetric.fields.current.number_of_rows,
                legend="row counts"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # Target drift bar and histogram plots
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Target: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "duration_min"},
                    field_path=ColumnDriftMetric.fields.drift_detected,
                    legend="drift detected",
                ),
            ],
            plot_type=PlotType.BAR,
            size=2
        )
    )

    # Target drift score plot
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Drift Score",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "duration_min"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="drift score",
                ),
            ],
            plot_type=PlotType.LINE,
            size=2
        )
    )

    return project


def add_data_quality_dashboard(project: Project) -> Project:
    """Add (build) data quality dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Title: Data Quality
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Data Quality",
        )
    )

    # Counter: Share of Drifted Features
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
            size=1,
        )
    )

    # Counter: Number of Columns
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Number of Columns",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetDriftMetric",
                field_path="number_of_columns",
                legend="share",
            ),
            text="share",
            agg=CounterAgg.LAST,
            size=1,
        )
    )

    # Plot: Dataset Quality
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Dataset Quality",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(metric_id="DatasetDriftMetric", field_path="share_of_drifted_columns", legend="Drift Share"),
                PanelValue(
                    metric_id="DatasetMissingValuesMetric",
                    field_path=DatasetMissingValuesMetric.fields.current.share_of_missing_values,
                    legend="Missing Values Share",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )

    return project


def add_predictions_drift_dashboard(project: Project) -> Project:
    """Add (build) predictions drift dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Title: Predictions drift
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Predictions Drift",
        )
    )

    # Counter: Stattest threshold
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Stattest Threshold",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="ColumnDriftMetric",
                field_path=ColumnDriftMetric.fields.stattest_threshold,
                metric_args={"column_name.name": "predictions"},
                legend="stattest threshold"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )
    
    # Counter: Drift Detected
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Predictions Drift Detected",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="ColumnDriftMetric",
                field_path=ColumnDriftMetric.fields.drift_detected,
                metric_args={"column_name.name": "predictions"},
                legend="stattest threshold"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # Plot: Predictions drift score plot - LINE
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Drift Score: Wasserstein distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "predictions"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="drift score",
                ),
            ],
            plot_type=PlotType.LINE,
            size=2
        )
    )

    # Plot: Predictions drift score - BAR
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Drift Score: Wasserstein distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "predictions"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=2,
        )
    )

    return project


def build_dashboards():
    """
    Build dashboards for projects:
    - Data Quality
    - Predictions Drift
    - Model Performance
    - Target Drift
    """

    # [Get workspace]
    
    ws: Workspace = Workspace.create(EVIDENTLY_WS)

    # [Build dashboards]

    # Data Quality
    project_dq = get_evidently_project(ws, "Data Quality")
    project_dq.dashboard.panels = []
    project_dq = add_data_quality_dashboard(project_dq)
    project_dq.save()

    # Predictions Drift
    project_pd = get_evidently_project(ws, "Predictions Drift")
    project_pd.dashboard.panels = []
    project_pd = add_predictions_drift_dashboard(project_pd)
    project_pd.save()

    # Model Performance
    project_mp = get_evidently_project(ws, "Model Performance")
    project_mp.dashboard.panels = []
    project_mp = add_regression_dashboard(project_mp)
    project_mp.save()

    # Target Drift
    project_td = get_evidently_project(ws, "Target Drift")
    project_td.dashboard.panels = []
    project_td = add_target_drift_dashboard(project_td)
    project_td.save()
