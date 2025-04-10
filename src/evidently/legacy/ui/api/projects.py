import asyncio
import datetime
import json
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

from litestar import Response
from litestar import Router
from litestar import delete
from litestar import get
from litestar import post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.params import Dependency
from litestar.params import Parameter
from typing_extensions import Annotated

from evidently.legacy.report.report import METRIC_GENERATORS
from evidently.legacy.report.report import METRIC_PRESETS
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.test_suite.test_suite import TEST_GENERATORS
from evidently.legacy.test_suite.test_suite import TEST_PRESETS
from evidently.legacy.ui.api.models import DashboardInfoModel
from evidently.legacy.ui.api.models import ReportModel
from evidently.legacy.ui.api.models import TestSuiteModel
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.base import SnapshotMetadata
from evidently.legacy.ui.dashboards.base import DashboardPanel
from evidently.legacy.ui.dashboards.reports import DashboardPanelCounter
from evidently.legacy.ui.dashboards.reports import DashboardPanelDistribution
from evidently.legacy.ui.dashboards.reports import DashboardPanelHistogram
from evidently.legacy.ui.dashboards.reports import DashboardPanelPlot
from evidently.legacy.ui.dashboards.test_suites import DashboardPanelTestSuite
from evidently.legacy.ui.dashboards.test_suites import DashboardPanelTestSuiteCounter
from evidently.legacy.ui.managers.projects import ProjectManager
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TeamID
from evidently.legacy.ui.type_aliases import UserID
from evidently.legacy.utils import NumpyEncoder


async def path_project_dependency(
    project_id: ProjectID,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    user_id: UserID,
):
    project = await project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    return project


@get("/{project_id:uuid}/reports")
async def list_reports(
    project: Annotated[Project, Dependency()],
    log_event: Callable,
) -> List[ReportModel]:
    reports = [
        ReportModel.from_snapshot(s)
        for s in await project.list_snapshots_async(include_test_suites=False)
        if s.is_report
    ]
    log_event("list_reports", reports_count=len(reports))
    return reports


@get("/{project_id:uuid}/test_suites")
async def list_test_suites(
    project: Annotated[Project, Dependency()],
    log_event: Callable,
) -> List[TestSuiteModel]:
    log_event("list_test_suites")
    return [
        TestSuiteModel.from_snapshot(s)
        for s in await project.list_snapshots_async(include_reports=False)
        if not s.is_report
    ]


@get("/{project_id:uuid}/snapshots")
async def list_snapshots(
    project: Annotated[Project, Dependency()],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> List[SnapshotMetadata]:
    snapshots = await project_manager.list_snapshots(user_id, project.id)
    log_event("list_snapshots", reports_count=len(snapshots))
    return snapshots


@get("/")
async def list_projects(
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
    team_id: Annotated[Optional[TeamID], Parameter(title="filter by team")] = None,
    org_id: Annotated[Optional[OrgID], Parameter(title="filter by org")] = None,
) -> Sequence[Project]:
    projects = await project_manager.list_projects(user_id, team_id, org_id)
    log_event("list_projects", project_count=len(projects))
    return projects


@get("/{project_id:uuid}/info")
async def get_project_info(
    project: Annotated[Project, Dependency()],
    log_event: Callable,
) -> Project:
    log_event("get_project_info")
    return project


@get("/search/{project_name:str}")
async def search_projects(
    project_name: Annotated[str, Parameter(title="Name of the project to search")],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
    team_id: Annotated[Optional[TeamID], Parameter(title="filter by team")] = None,
    org_id: Annotated[Optional[OrgID], Parameter(title="filter by org")] = None,
) -> List[Project]:
    log_event("search_projects")
    return await project_manager.search_project(user_id, team_id=team_id, org_id=org_id, project_name=project_name)


@post("/{project_id:uuid}/info")
async def update_project_info(
    project: Annotated[Project, Dependency()],
    data: Project,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> Project:
    data.id = project.id
    await project_manager.update_project(user_id, data)
    log_event("update_project_info")
    return project


@get("/{project_id:uuid}/reload")
async def reload_project_snapshots(
    project: Annotated[Project, Dependency()],
    log_event: Callable,
) -> None:
    await project.reload_async(reload_snapshots=True)
    log_event("reload_project_snapshots")


async def path_snapshot_metadata_dependency(
    project: Annotated[Project, Dependency()],
    snapshot_id: SnapshotID,
):
    snapshot = await project.get_snapshot_metadata_async(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot


@get(
    "/{project_id:uuid}/{snapshot_id:uuid}/graphs_data/{graph_id:str}",
)
async def get_snapshot_graph_data(
    snapshot_metadata: Annotated[SnapshotMetadata, Dependency()],
    graph_id: Annotated[str, Parameter(title="id of graph in snapshot")],
    log_event: Callable,
) -> str:
    graph = (await snapshot_metadata.get_additional_graphs()).get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    log_event("get_snapshot_graph_data")
    return json.dumps(graph.dict() if not isinstance(graph, dict) else graph, cls=NumpyEncoder)


@get("/{project_id:uuid}/{snapshot_id:uuid}/download")
async def get_snapshot_download(
    snapshot_metadata: Annotated[SnapshotMetadata, Dependency()],
    log_event: Callable,
    report_format: str = "html",
) -> Response:
    report = await snapshot_metadata.as_report_base()
    if report_format == "html":
        return Response(
            report.get_html(),
            headers={"content-disposition": f"attachment;filename={snapshot_metadata.id}.html"},
        )
    if report_format == "json":
        return Response(
            report.json(),
            headers={"content-disposition": f"attachment;filename={snapshot_metadata.id}.json"},
        )
    log_event("get_snapshot_download")
    raise HTTPException(status_code=400, detail=f"Unknown format {report_format}")


@get("/{project_id:uuid}/{snapshot_id:uuid}/data")
async def get_snapshot_data(
    snapshot_metadata: Annotated[SnapshotMetadata, Dependency()],
    log_event: Callable,
) -> str:
    dashboard_info, snapshot = await asyncio.gather(snapshot_metadata.get_dashboard_info(), snapshot_metadata.load())
    info = DashboardInfoModel.from_dashboard_info(dashboard_info=dashboard_info)

    log_event(
        "get_snapshot_data",
        snapshot_type="report" if snapshot.is_report else "test_suite",
        metrics=[m.get_id() for m in snapshot.first_level_metrics()],
        metric_presets=snapshot.metadata.get(METRIC_PRESETS, []),
        metric_generators=snapshot.metadata.get(METRIC_GENERATORS, []),
        tests=[t.get_id() for t in snapshot.first_level_tests()],
        test_presets=snapshot.metadata.get(TEST_PRESETS, []),
        test_generators=snapshot.metadata.get(TEST_GENERATORS, []),
    )
    return json.dumps(info.dict() if not isinstance(info, dict) else info, cls=NumpyEncoder)


@get("/{project_id:uuid}/{snapshot_id:uuid}/metadata")
async def get_snapshot_metadata(
    snapshot_metadata: Annotated[SnapshotMetadata, Dependency()],
    log_event: Callable,
) -> SnapshotMetadata:
    log_event(
        "get_snapshot_metadata",
        snapshot_type="report" if snapshot_metadata.is_report else "test_suite",
        metric_presets=snapshot_metadata.metadata.get(METRIC_PRESETS, []),
        metric_generators=snapshot_metadata.metadata.get(METRIC_GENERATORS, []),
        test_presets=snapshot_metadata.metadata.get(TEST_PRESETS, []),
        test_generators=snapshot_metadata.metadata.get(TEST_GENERATORS, []),
    )
    return snapshot_metadata


@get("/{project_id:uuid}/dashboard/panels")
async def list_project_dashboard_panels(
    project: Annotated[Project, Dependency()],
    log_event: Callable,
) -> List[DashboardPanel]:
    log_event("list_project_dashboard_panels")
    return list(project.dashboard.panels)


# We need this endpoint to export
# some additional models to open api schema
@get("/models/additional")
async def additional_models() -> (
    List[
        Union[
            DashboardInfoModel,
            DashboardPanelPlot,
            DashboardPanelCounter,
            DashboardPanelDistribution,
            DashboardPanelHistogram,
            DashboardPanelTestSuite,
            DashboardPanelTestSuiteCounter,
        ]
    ]
):
    return []


@get("/{project_id:uuid}/dashboard")
async def project_dashboard(
    project: Annotated[Project, Dependency()],
    # TODO: no datetime, as it unable to validate '2023-07-09T02:03'
    log_event: Callable,
    timestamp_start: Optional[str] = None,
    timestamp_end: Optional[str] = None,
) -> str:
    timestamp_start_ = datetime.datetime.fromisoformat(timestamp_start) if timestamp_start else None
    timestamp_end_ = datetime.datetime.fromisoformat(timestamp_end) if timestamp_end else None

    info = await DashboardInfoModel.from_project_with_time_range(
        project,
        timestamp_start=timestamp_start_,
        timestamp_end=timestamp_end_,
    )
    log_event("project_dashboard")
    return json.dumps(info.dict() if not isinstance(info, dict) else info, cls=NumpyEncoder)


@post("/")
async def add_project(
    data: Project,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
    team_id: Optional[TeamID] = None,
    org_id: Optional[OrgID] = None,
) -> Project:
    if team_id is None and data.team_id is not None:
        team_id = data.team_id
    elif org_id is None and data.org_id is not None:
        org_id = data.org_id

    p = await project_manager.add_project(data, user_id, team_id, org_id)
    log_event("add_project")
    return p


@delete("/{project_id:uuid}")
async def delete_project(
    project_id: Annotated[ProjectID, Parameter(title="id of project")],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> None:
    await project_manager.delete_project(user_id, project_id)
    log_event("delete_project")


@post("/{project_id:uuid}/snapshots")
async def add_snapshot(
    project: Annotated[Project, Dependency()],
    parsed_json: Snapshot,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> None:
    await project_manager.add_snapshot(user_id, project.id, parsed_json)
    log_event("add_snapshot")


@delete("/{project_id:uuid}/{snapshot_id:uuid}")
async def delete_snapshot(
    project: Annotated[Project, Dependency()],
    snapshot_id: Annotated[SnapshotID, Parameter(title="id of snapshot")],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> None:
    await project_manager.delete_snapshot(user_id, project.id, snapshot_id)
    log_event("delete_snapshot")


def create_projects_api(guard: Callable) -> Router:
    return Router(
        "/projects",
        route_handlers=[
            Router(
                "",
                route_handlers=[
                    additional_models,
                    list_projects,
                    list_reports,
                    get_project_info,
                    search_projects,
                    list_test_suites,
                    get_snapshot_graph_data,
                    get_snapshot_data,
                    get_snapshot_download,
                    list_project_dashboard_panels,
                    project_dashboard,
                    list_snapshots,
                    get_snapshot_metadata,
                ],
            ),
            Router(
                "",
                route_handlers=[
                    update_project_info,
                    reload_project_snapshots,
                    add_project,
                    delete_project,
                    add_snapshot,
                    delete_snapshot,
                ],
                guards=[guard],
            ),
        ],
    )


projects_api_dependencies: Dict[str, Provide] = {
    "project": Provide(path_project_dependency),
    "snapshot_metadata": Provide(path_snapshot_metadata_dependency),
}
