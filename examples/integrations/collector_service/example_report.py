import datetime
import os.path
import time

import pandas as pd
from requests.exceptions import RequestException

from evidently.collector.client import CollectorClient
from evidently.collector.config import CollectorConfig
from evidently.collector.config import IntervalTrigger
from evidently.collector.config import ReportConfig
from evidently.collector.config import RowsCountTrigger
from evidently.metrics import ColumnValueRangeMetric
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfOutRangeValues
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.workspace import Workspace

COLLECTOR_ID = "default"
COLLECTOR_TEST_ID = "default_test"

PROJECT_NAME = "My Cool Project"

WORKSPACE_PATH = "workspace"

client = CollectorClient("http://localhost:8001")


def get_data():
    cur = ref = pd.DataFrame([{"values1": 5.0, "values2": 0.0} for _ in range(10)])
    return cur, ref


def setup_report():
    report = Report(metrics=[ColumnValueRangeMetric("values1", left=5)], tags=["quality"])

    cur, ref = get_data()
    report.run(reference_data=ref, current_data=cur)
    return ReportConfig.from_report(report)


def setup_test_suite():
    report = TestSuite(tests=[TestNumberOfOutRangeValues("values1", left=5)], tags=["quality"])

    cur, ref = get_data()
    report.run(reference_data=ref, current_data=cur)
    return ReportConfig.from_test_suite(report)


def setup_workspace():
    ws = Workspace.create(WORKSPACE_PATH)
    project = ws.create_project(PROJECT_NAME)
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="sample_panel",
            filter=ReportFilter(metadata_values={}, tag_values=["quality"]),
            values=[
                PanelValue(metric_id="ColumnValueRangeMetric", field_path="current.share_in_range", legend="current"),
                PanelValue(
                    metric_id="ColumnValueRangeMetric", field_path="reference.share_in_range", legend="reference"
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )
    project.save()


def setup_config():
    ws = Workspace.create(WORKSPACE_PATH)
    project = ws.search_project(PROJECT_NAME)[0]
    # conf = CollectorConfig(trigger=IntervalTrigger(interval=5), report_config=setup_report(), project_id=str(project.id))
    conf = CollectorConfig(
        trigger=RowsCountTrigger(rows_count=5), report_config=setup_report(), project_id=str(project.id)
    )
    client.create_collector(id=COLLECTOR_ID, collector=conf)

    # test_conf = CollectorConfig(trigger=IntervalTrigger(interval=5), report_config=setup_test_suite(), project_id=str(project.id))
    test_conf = CollectorConfig(
        trigger=RowsCountTrigger(rows_count=5), report_config=setup_test_suite(), project_id=str(project.id)
    )
    client.create_collector(id=COLLECTOR_TEST_ID, collector=test_conf)

    _, ref = get_data()
    client.set_reference(id=COLLECTOR_ID, reference=ref)
    client.set_reference(id=COLLECTOR_TEST_ID, reference=ref)


def send_data():
    size = 1
    data = pd.DataFrame([{"values1": 3.0 + datetime.datetime.now().minute % 5, "values2": 0.0} for _ in range(size)])

    client.send_data(COLLECTOR_ID, data)
    client.send_data(COLLECTOR_TEST_ID, data)
    print("sent")


def start_sending_data():
    print("Start data loop")
    while True:
        try:
            send_data()
        except RequestException as e:
            print(f"collector service not available: {e.__class__.__name__}")
        time.sleep(1)


def main():
    if not os.path.exists(WORKSPACE_PATH) or len(Workspace.create(WORKSPACE_PATH).search_project(PROJECT_NAME)) == 0:
        setup_workspace()

    setup_config()

    start_sending_data()


if __name__ == "__main__":
    main()
