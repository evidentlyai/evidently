import datetime

from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetCorrelationsMetric
from evidently_service.client import EvidentlyClient
from evidently_service.generate_workspace import create_project
from evidently_service.generate_workspace import create_report
from evidently_service.generate_workspace import create_test_suite

WORKSPACE = "http://localhost:8000"


def main():
    project = create_project()
    client = EvidentlyClient(WORKSPACE)
    client.add_project(project)

    for d in range(1, 10):
        ts = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=d), datetime.time())
        create_report(
            DataDriftPreset(
                num_stattest="ks", cat_stattest="psi", num_stattest_threshold=0.2, cat_stattest_threshold=0.2
            ),
            ts,
            "drift",
        ).upload(WORKSPACE, project.id)
        create_report(DatasetCorrelationsMetric(), ts, "correlation").upload(WORKSPACE, project.id)

    create_test_suite().upload(WORKSPACE, project.id)


if __name__ == "__main__":
    main()
