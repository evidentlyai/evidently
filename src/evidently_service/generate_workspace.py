import datetime
import os
import uuid

import numpy as np
from sklearn import datasets

from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetCorrelationsMetric
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns
from evidently.tests import TestShareOfDriftedColumns
from evidently_service.dashboards import CounterAgg
from evidently_service.dashboards import DashboardConfig
from evidently_service.dashboards import DashboardPanelCounter
from evidently_service.dashboards import DashboardPanelPlot
from evidently_service.dashboards import PanelValue
from evidently_service.dashboards import PlotType
from evidently_service.dashboards import ReportFilter
from evidently_service.workspace import Project

adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
adult = adult_data.frame

adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]

adult_cur.iloc[:2000, 3:5] = np.nan


def create_report(metric, date: datetime.datetime, tag: str):
    data_drift_report = Report(
        metrics=[metric], metadata={"type": metric.__class__.__name__}, tags=[tag], timestamp=date
    )

    data_drift_report.run(reference_data=adult_ref, current_data=adult_cur)
    data_drift_report._save(f"workspace/project1/reports/{uuid.uuid4()}")
    # report_dashboard_id, report_dashboard_info, report_graphs = data_drift_report._build_dashboard_info()


def create_test_suite():
    data_drift_dataset_tests = TestSuite(
        tests=[
            TestNumberOfDriftedColumns(),
            TestShareOfDriftedColumns(),
        ]
    )

    data_drift_dataset_tests.run(reference_data=adult_ref, current_data=adult_cur)
    data_drift_dataset_tests._save(f"workspace/project1/test_suites/ts_{uuid.uuid4()}.json")


def create_project_config():
    conf = DashboardConfig(
        name="sample_dashboard",
        panels=[
            DashboardPanelCounter(
                filter=ReportFilter(metadata_values={}, tag_values=["drift"]), agg=CounterAgg.NONE, title="My beatifule panels"
            ),
            DashboardPanelCounter(
                filter=ReportFilter(metadata_values={"type": "DataDriftPreset"}, tag_values=["drift"]),
                agg=CounterAgg.SUM,
                value=PanelValue(metric_id="DatasetDriftMetric", field_path="number_of_columns"),
                title="sum of number_of_columns",
            ),
            DashboardPanelPlot(
                title="sample_panel",
                filter=ReportFilter(metadata_values={"type": "DataDriftPreset"}, tag_values=["drift"]),
                values=[
                    PanelValue(metric_id="DatasetDriftMetric", field_path="share_of_drifted_columns", legend="Share"),
                    PanelValue(metric_id="DatasetDriftMetric", field_path="number_of_drifted_columns", legend="Count"),
                ],
                plot_type=PlotType.LINE,
            ),
        ],
    )
    project = Project(name="project1", path="workspace/project1", dashboard=conf)
    project.save()


def main():
    if not os.path.exists("workspace"):
        os.mkdir("workspace")
        os.mkdir("workspace/project1")
        os.mkdir("workspace/project1/reports")
        os.mkdir("workspace/project1/test_suites")

    create_project_config()

    for d in range(1, 10):
        ts = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=d), datetime.time())
        create_report(
            DataDriftPreset(
                num_stattest="ks", cat_stattest="psi", num_stattest_threshold=0.2, cat_stattest_threshold=0.2
            ),
            ts,
            "drift",
        )
        create_report(DatasetCorrelationsMetric(), ts, "correlation")

    create_test_suite()


if __name__ == "__main__":
    main()
