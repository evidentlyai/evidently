import pandas as pd

from evidently.collector.client import CollectorClient
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset

from evidently.collector.config import CollectorConfig, IntervalTrigger, ReportConfig
from evidently.ui.workspace import RemoteWorkspace


def get_or_create_project_by_name(ui_api_url: str, project_name: str):
    ui_client = RemoteWorkspace(ui_api_url)
    projects = ui_client.search_project(project_name)
    if len(projects) == 0:
        project = ui_client.create_project(project_name)
    else:
        project = projects[0]
    return str(project.id)


# Project ID to upload data.
# Can be obtained via UI after creating project
project_id = get_or_create_project_by_name("http://localhost:8000", "My Test Project")

# Address of UI service for snapshot upload.
# Should be address of UI service accessible from collector service.
# For docker compose: http://ui.:8000
api_url = "http://ui.:8000"

# Generate Report configuration
# create sample report to create configuration from it should contain:
#  - expected metrics
#  - sample dataset (with required columns)

report = Report(metrics=[DataQualityPreset()])

sample_data = pd.DataFrame(data={"a": [1, 2, 3, 4]})

report.run(current_data=sample_data, reference_data=None)

# create collector configuration
config = CollectorConfig(
    id="main",
    trigger=IntervalTrigger(interval=10),
    report_config=ReportConfig.from_report(report),
    reference_path=None,
    project_id=project_id,
    api_url=api_url,
)

client = CollectorClient("http://localhost:8001")
client.create_collector("main", config)
# After this call collector configuration would be saved in ./config folder.
