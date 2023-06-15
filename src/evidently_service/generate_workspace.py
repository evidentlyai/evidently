import json
import os
import uuid

import numpy as np
from sklearn import datasets

from evidently.metric_preset import DataDriftPreset
from evidently.tests import *
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.utils.dashboard import dashboard_info_to_json

adult_data = datasets.fetch_openml(name='adult', version=2, as_frame='auto')
adult = adult_data.frame

adult_ref = adult[~adult.education.isin(['Some-college', 'HS-grad', 'Bachelors'])]
adult_cur = adult[adult.education.isin(['Some-college', 'HS-grad', 'Bachelors'])]

adult_cur.iloc[:2000, 3:5] = np.nan

data_drift_report = Report(metrics=[
    DataDriftPreset(num_stattest='ks', cat_stattest='psi', num_stattest_threshold=0.2, cat_stattest_threshold=0.2),
])

data_drift_report.run(reference_data=adult_ref, current_data=adult_cur)
report_dashboard_id, report_dashboard_info, report_graphs = data_drift_report._build_dashboard_info()

data_drift_dataset_tests = TestSuite(tests=[
    TestNumberOfDriftedColumns(),
    TestShareOfDriftedColumns(),
])

data_drift_dataset_tests.run(reference_data=adult_ref, current_data=adult_cur)

if not os.path.exists("workspace"):
    os.mkdir("workspace")
    os.mkdir("workspace/project1")
    os.mkdir("workspace/project1/reports")
    os.mkdir("workspace/project1/test_suites")

data_drift_report._save(f"workspace/project1/reports/{data_drift_report.id}")
data_drift_dataset_tests._save(f"workspace/project1/test_suites/{data_drift_dataset_tests.id}")


project_dashboard_data = {
  "name": "Report",
  "widgets": [
    {
      "type": "counter",
      "title": "",
      "size": 2,
      "id": "69e09b1f-9576-4eb3-8ba9-ff1d9ed09a90",
      "details": "",
      "params": {
        "counters": [
          {
            "value": "Project Dashboard",
            "label": "This is sample project dashboard"
          }
        ]
      },
      "insights": [],
      "alerts": [],
      "tabs": [],
      "widgets": [],
      "pageSize": 5
    },
    {
      "type": "counter",
      "title": "",
      "size": 2,
      "id": "3bf77e34-b4e8-491d-99b5-7e7ecd8c44ed",
      "details": "",
      "params": {
        "counters": [
          {
            "value": "15",
            "label": "Metrics count"
          },
          {
            "value": "6",
            "label": "Reports count"
          }
        ]
      },
      "insights": [],
      "alerts": [],
      "tabs": [],
      "widgets": [],
      "pageSize": 5
    }
  ]
}

with open("workspace/project1/dashboard.json", "w") as f:
    json.dump(project_dashboard_data, f)
