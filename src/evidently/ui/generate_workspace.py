import datetime

import numpy as np
from sklearn import datasets

from evidently.metric_preset import DataDriftPreset
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnMissingValuesMetric
from evidently.metrics import DatasetCorrelationsMetric
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns
from evidently.tests import TestShareOfDriftedColumns
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.workspace import Workspace

adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
adult = adult_data.frame

adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]

adult_cur.iloc[:2000, 3:5] = np.nan

WORKSPACE = "workspace"


def create_report(metric, date: datetime.datetime, tag: str):
    data_drift_report = Report(
        metrics=[metric, ColumnDriftMetric(column_name="age"), ColumnMissingValuesMetric(column_name="education")],
        options={"render": {"raw_data": True}},
        metadata={"type": metric.__class__.__name__},
        tags=[tag],
        timestamp=date,
        dataset_id="adult",
    ).set_batch_size("1")

    data_drift_report.run(reference_data=adult_ref, current_data=adult_cur)
    return data_drift_report


def create_test_suite():
    data_drift_dataset_tests = TestSuite(
        tests=[
            TestNumberOfDriftedColumns(),
            TestShareOfDriftedColumns(),
        ]
    )

    data_drift_dataset_tests.run(reference_data=adult_ref, current_data=adult_cur)
    return data_drift_dataset_tests


def create_project(workspace: Workspace):
    project = workspace.create_project("project1")
    project.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=["drift"]),
            agg=CounterAgg.NONE,
            title="My beatifule panels",
        )
    )
    project.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={"type": "DataDriftPreset"}, tag_values=["drift"]),
            agg=CounterAgg.SUM,
            value=PanelValue(metric_id="DatasetDriftMetric", field_path="number_of_columns"),
            title="sum of number_of_columns",
        )
    )
    project.add_panel(
        DashboardPanelPlot(
            title="sample_panel",
            filter=ReportFilter(metadata_values={"type": "DataDriftPreset"}, tag_values=["drift"]),
            values=[
                PanelValue(
                    metric_id="DatasetDriftMetric",
                    metric_args={"num_stattest": "ks"},
                    field_path="share_of_drifted_columns",
                    legend="Share",
                ),
                PanelValue(
                    metric_id="DatasetDriftMetric",
                    metric_args={"num_stattest": "ks"},
                    field_path="number_of_drifted_columns",
                    legend="Count",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )
    return project


def main(workspace: str):
    ws = Workspace.create(workspace)
    project = create_project(ws)
    project.save()

    for d in range(1, 3):
        ts = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=d), datetime.time())
        report = create_report(
            DataDriftPreset(
                num_stattest="ks", cat_stattest="psi", num_stattest_threshold=0.2, cat_stattest_threshold=0.2
            ),
            ts,
            "drift",
        )
        ws.add_report(project.id, report)
        report = create_report(
            DataDriftPreset(
                num_stattest="cramer_von_mises",
                cat_stattest="psi",
                num_stattest_threshold=0.5,
                cat_stattest_threshold=0.2,
            ),
            ts,
            "drift",
        )
        ws.add_report(project.id, report)
        corr_report = create_report(DatasetCorrelationsMetric(), ts, "correlation")
        ws.add_report(project.id, corr_report)

    test_suite = create_test_suite()
    ws.add_test_suite(project.id, test_suite)


if __name__ == "__main__":
    main("workspace")
