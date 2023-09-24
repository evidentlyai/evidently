from prefect import flow

from src.utils.evidently_monitoring import build_dashboards


@flow(flow_run_name="build-dashboards", log_prints=True)
def build_projects_dashboards() -> None:
    """Build Evidently projects dashboards flow."""
    build_dashboards()


if __name__ == "__main__":
    build_projects_dashboards()
