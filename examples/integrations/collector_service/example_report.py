import datetime
import json
import os.path
import random
import time

import numpy as np
import pandas as pd
import requests
from sklearn import datasets
from requests.exceptions import RequestException
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import ColumnValueRangeMetric
from evidently.report import Report
from config import CONFIG_PATH, CollectorConfig, create_config_report
from evidently.utils import NumpyEncoder
from evidently_service.dashboards import DashboardPanelPlot, PanelValue, PlotType, ReportFilter
from evidently_service.workspace import Workspace

REPORT_CONFIG_PATH = "report.json"
WORKSACE_PATH = "workspace"

def get_data():
    cur = ref = pd.DataFrame([{"values1": 5., "values2": 0.} for _ in range(10)])
    return cur, ref


def setup_report(path):
    report = Report(metrics=[ColumnValueRangeMetric("values1", left=5)], tags=["quality"])

    cur, ref = get_data()
    report.run(reference_data=ref, current_data=cur)
    create_config_report(report, path)

def setup_workspace():
    ws = Workspace.create("workspace")
    project = ws.create_project("My Cool Project")
    project.add_panel(
        DashboardPanelPlot(
            title="sample_panel",
            filter=ReportFilter(metadata_values={}, tag_values=["quality"]),
            values=[
                PanelValue(metric_id="ColumnValueRangeMetric", field_path="current.share_in_range", legend="current"),
                PanelValue(metric_id="ColumnValueRangeMetric", field_path="reference.share_in_range", legend="reference"),
            ],
            plot_type=PlotType.LINE,
        )
    )
    project.save()
    conf = CollectorConfig(snapshot_interval=5, report_config_path="report.json", project_id=str(project.id))
    conf.save(CONFIG_PATH)

def send_data():
    size = 1
    data = pd.DataFrame([{"values1": 3. + datetime.datetime.now().minute % 5, "values2": 0.} for _ in range(size)])
    r = requests.post("http://localhost:8001/data", data=json.dumps(data.to_dict(), cls=NumpyEncoder), headers={"ContentType": "application/json"})
    r.raise_for_status()
    print("data sent")


def start_sending_data():
    while True:
        try:
            send_data()
        except RequestException:
            pass
        time.sleep(1)


def main():
    if not os.path.exists(REPORT_CONFIG_PATH):
        setup_report(REPORT_CONFIG_PATH)

    if not os.path.exists(WORKSACE_PATH):
        setup_workspace()

    start_sending_data()


if __name__ == '__main__':
    main()
