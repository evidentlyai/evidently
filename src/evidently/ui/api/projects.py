import datetime
import json
import uuid
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from starlette.responses import Response
from typing_extensions import Annotated

from evidently.report.report import METRIC_GENERATORS
from evidently.report.report import METRIC_PRESETS
from evidently.suite.base_suite import Snapshot
from evidently.test_suite.test_suite import TEST_GENERATORS
from evidently.test_suite.test_suite import TEST_PRESETS
from evidently.ui.api.models import DashboardInfoModel
from evidently.ui.api.models import ReportModel
from evidently.ui.api.models import TestSuiteModel
from evidently.ui.api.security import get_org_id
from evidently.ui.api.security import get_user_id
from evidently.ui.api.utils import authorized
from evidently.ui.api.utils import event_logger
from evidently.ui.api.utils import get_project_manager
from evidently.ui.base import Project
from evidently.ui.base import ProjectManager
from evidently.ui.dashboards.base import DashboardPanel
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import TeamID
from evidently.ui.type_aliases import UserID
from evidently.ui.utils import NumpyJsonResponse
from evidently.ui.utils import skip_jsonable_encoder
from evidently.utils import NumpyEncoder

project_api = APIRouter()

project_read_router = APIRouter(prefix="/projects")
project_write_router = APIRouter(prefix="/projects", dependencies=[Depends(authorized)])

PROJECT_ID = Path(title="id of the project")
SNAPSHOT_ID = Path(title="id of the snapshot")
GRAPH_ID = Path(title="id of snapshot graph")


@project_read_router.get("")
async def list_projects(
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> Sequence[Project]:
    projects = project_manager.list_projects(user_id)
    log_event("list_projects", project_count=len(projects))
    return projects


@project_read_router.get("/{project_id}/reports")
async def list_reports(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> List[ReportModel]:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    reports = [ReportModel.from_snapshot(s) for s in project.list_snapshots(include_test_suites=False) if s.is_report]
    log_event("list_reports", reports_count=len(reports))
    return reports


@project_read_router.get("/{project_id}/info")
async def get_project_info(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> Project:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    log_event("get_project_info")
    return project


@project_read_router.get("/search/{project_name}")
async def search_projects(
    project_name: Annotated[str, "Name of the project to search"],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> List[Project]:
    log_event("search_projects")
    return project_manager.search_project(user_id, project_name=project_name)


@project_write_router.post("/{project_id}/info")
async def update_project_info(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    data: Project,
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> Project:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    project.description = data.description
    project.name = data.name
    project.date_from = data.date_from
    project.date_to = data.date_to
    project.dashboard = data.dashboard
    project.save()
    log_event("update_project_info")
    return project


@project_read_router.get("/{project_id}/reload")
async def reload_project_snapshots(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
):
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    project.reload(reload_snapshots=True)
    log_event("reload_project_snapshots")
    return


@project_read_router.get("/{project_id}/test_suites")
async def list_test_suites(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> List[TestSuiteModel]:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    log_event("list_test_suites")
    return [TestSuiteModel.from_snapshot(s) for s in project.list_snapshots(include_reports=False) if not s.is_report]


@project_read_router.get("/{project_id}/{snapshot_id}/graphs_data/{graph_id}")
async def get_snapshot_graph_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
    graph_id: Annotated[str, GRAPH_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> Response:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    snapshot = project.get_snapshot_metadata(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    graph = snapshot.additional_graphs.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    log_event("get_snapshot_graph_data")
    return Response(media_type="application/json", content=json.dumps(graph, cls=NumpyEncoder))


@project_read_router.get("/{project_id}/{snapshot_id}/download")
async def get_snapshot_download(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
    report_format: str = "html",
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> Response:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    snapshot = project.get_snapshot_metadata(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    report = snapshot.as_report_base()
    if report_format == "html":
        return Response(report.get_html(), headers={"content-disposition": f"attachment;filename={snapshot_id}.html"})
    if report_format == "json":
        return Response(report.json(), headers={"content-disposition": f"attachment;filename={snapshot_id}.json"})
    log_event("get_snapshot_download")
    return Response(f"Unknown format {report_format}", status_code=400)


@project_read_router.get("/{project_id}/{snapshot_id}/data", response_class=NumpyJsonResponse)
@skip_jsonable_encoder
async def get_snapshot_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> DashboardInfoModel:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    snapshot_meta = project.get_snapshot_metadata(snapshot_id)
    if snapshot_meta is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    info = DashboardInfoModel.from_dashboard_info(snapshot_meta.dashboard_info)
    snapshot = snapshot_meta.load()
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
    return info


@project_read_router.get("/{project_id}/dashboard/panels")
async def list_project_dashboard_panels(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> List[DashboardPanel]:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    log_event("list_project_dashboard_panels")
    return list(project.dashboard.panels)


@project_read_router.get("/{project_id}/dashboard", response_class=NumpyJsonResponse)
@skip_jsonable_encoder
async def project_dashboard(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    timestamp_start: Optional[datetime.datetime] = None,
    timestamp_end: Optional[datetime.datetime] = None,
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
) -> DashboardInfoModel:
    project = project_manager.get_project(user_id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    info = DashboardInfoModel.from_project_with_time_range(
        project, timestamp_start=timestamp_start, timestamp_end=timestamp_end
    )
    log_event("project_dashboard")
    return info


@project_write_router.post("")
async def add_project(
    project: Project,
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
    team_id: Annotated[TeamID, "Id of team"] = None,
    org_id: OrgID = Depends(get_org_id),
) -> Project:
    p = project_manager.add_project(project, user_id, team_id, org_id)
    log_event("add_project")
    return p


@project_write_router.delete("/{project_id}")
def delete_project(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
):
    project_manager.delete_project(user_id, project_id)
    log_event("delete_project")


@project_write_router.post("/{project_id}/snapshots")
async def add_snapshot(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot: Snapshot,
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
):
    if project_manager.get_project(user_id, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    project_manager.add_snapshot(user_id, project_id, snapshot)
    log_event("add_snapshot")


@project_write_router.delete("/{project_id}/{snapshot_id}")
def delete_snapshot(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
    project_manager: ProjectManager = Depends(get_project_manager),
    log_event: Callable = Depends(event_logger),
    user_id: UserID = Depends(get_user_id),
):
    project_manager.delete_snapshot(user_id, project_id, snapshot_id)
    log_event("delete_snapshot")


project_api.include_router(project_read_router)
project_api.include_router(project_write_router)
