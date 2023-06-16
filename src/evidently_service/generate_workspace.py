import datetime
import json
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
from evidently.utils import NumpyEncoder
from evidently_service.dashboards import DashboardConfig
from evidently_service.dashboards import DashboardValue
from evidently_service.dashboards import ReportFilter

adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
adult = adult_data.frame

adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]

adult_cur.iloc[:2000, 3:5] = np.nan


def create_report(metric, date: datetime.datetime):
    data_drift_report = Report(metrics=[metric], metadata={"type": metric.__class__.__name__}, timestamp=date)

    data_drift_report.run(reference_data=adult_ref, current_data=adult_cur)
    data_drift_report._save(f"workspace/project1/{uuid.uuid4()}")
    # report_dashboard_id, report_dashboard_info, report_graphs = data_drift_report._build_dashboard_info()


def create_test_suite():
    data_drift_dataset_tests = TestSuite(
        tests=[
            TestNumberOfDriftedColumns(),
            TestShareOfDriftedColumns(),
        ]
    )

    data_drift_dataset_tests.run(reference_data=adult_ref, current_data=adult_cur)
    data_drift_dataset_tests._save(f"workspace/project1/ts_{uuid.uuid4()}.json")


def create_dashboard_config():
    conf = DashboardConfig(
        id=uuid.uuid4(),
        name="sample_dashboard",
        filter=ReportFilter(metadata_values={"type": "DataDriftPreset"}),
        value=DashboardValue(metric_id="DataDriftTableResults", field_path="share_of_drifted_columns"),
    )
    with open("workspace/project1.dashboards.json", "w") as f:
        json.dump({str(conf.id): conf.dict()}, f, cls=NumpyEncoder)


def main():
    if not os.path.exists("workspace"):
        os.mkdir("workspace")
        os.mkdir("workspace/project1")
        os.mkdir("workspace/project1/reports")
        os.mkdir("workspace/project1/test_suites")

    for d in range(1, 10):
        ts = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=d), datetime.time())
        create_report(
            DataDriftPreset(
                num_stattest="ks", cat_stattest="psi", num_stattest_threshold=0.2, cat_stattest_threshold=0.2
            ),
            ts,
        )
        create_report(DatasetCorrelationsMetric(), ts)

    create_test_suite()
    create_dashboard_config()


if __name__ == "__main__":
    main()

