import datetime

from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetCorrelationsMetric
from evidently.ui.generate_workspace import create_project
from evidently.ui.generate_workspace import create_report
from evidently.ui.generate_workspace import create_test_suite
from evidently.ui.remote import RemoteWorkspace

WORKSPACE = "http://localhost:8000"


def main():
    project = create_project()
    client = RemoteWorkspace(WORKSPACE)
    client.add_project(project)

    for d in range(1, 10):
        ts = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=d), datetime.time())
        client.add_report(
            project.id,
            create_report(
                DataDriftPreset(
                    num_stattest="ks", cat_stattest="psi", num_stattest_threshold=0.2, cat_stattest_threshold=0.2
                ),
                ts,
                "drift",
            ),
        )
        client.add_report(project.id, create_report(DatasetCorrelationsMetric(), ts, "correlation"))

    client.add_test_suite(project.id, create_test_suite())


if __name__ == "__main__":
    main()
