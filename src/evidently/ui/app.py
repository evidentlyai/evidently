import datetime
import json
import os
import pathlib
import uuid
from contextlib import asynccontextmanager
from typing import List
from typing import Optional
from typing import Sequence

import uvicorn
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import Request
from starlette.responses import FileResponse
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from typing_extensions import Annotated
from watchdog.observers import Observer

import evidently
from evidently.report.report import METRIC_GENERATORS
from evidently.report.report import METRIC_PRESETS
from evidently.suite.base_suite import Snapshot
from evidently.telemetry import DO_NOT_TRACK_ENV
from evidently.telemetry import event_logger
from evidently.test_suite.test_suite import TEST_GENERATORS
from evidently.test_suite.test_suite import TEST_PRESETS
from evidently.ui.dashboards import DashboardPanel
from evidently.ui.models import DashboardInfoModel
from evidently.ui.models import ReportModel
from evidently.ui.models import TestSuiteModel
from evidently.ui.utils import authenticated
from evidently.ui.utils import set_secret
from evidently.ui.watcher import WorkspaceDirHandler
from evidently.ui.workspace import Project
from evidently.ui.workspace import ProjectBase
from evidently.ui.workspace import Workspace
from evidently.utils import NumpyEncoder

SERVICE_INTERFACE = "service_backend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup
    Initialise the Client and add it to app.state
    """
    workspace = Workspace(app.state.workspace_path)
    app.state.workspace = workspace
    observer = Observer()
    observer.schedule(WorkspaceDirHandler(workspace), workspace.path, recursive=True)
    observer.start()

    if event_logger.is_enabled():
        print(f"Anonimous usage reporting is enabled. To disable it, set env variable {DO_NOT_TRACK_ENV} to any value")
    else:
        print("Anonimous usage reporting is disabled")
    event_logger.send_event(SERVICE_INTERFACE, "startup")
    yield
    """ Run on shutdown
        Close the connection
        Clear variables and release the resources
    """


app = FastAPI(lifespan=lifespan)

ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
static_path = os.path.join(ui_path, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/", include_in_schema=False)
@app.get("/projects", include_in_schema=False)
@app.get("/projects/{path:path}", include_in_schema=False)
async def index(path=None):
    event_logger.send_event(SERVICE_INTERFACE, "index")
    return FileResponse(os.path.join(ui_path, "index.html"))


@app.get("/manifest.json", include_in_schema=False)
@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon-16x16.png", include_in_schema=False)
@app.get("/favicon-32x32.png", include_in_schema=False)
async def manifest(request: Request):
    path = request.url.path[1:]
    if path in ("manifest.json", "favicon.ico", "favicon-16x16.png", "favicon-32x32.png"):
        return FileResponse(os.path.join(ui_path, path))


api_router = APIRouter(prefix="/api")

api_read_router = APIRouter()


api_write_router = APIRouter(dependencies=[Depends(authenticated)])


PROJECT_ID = Path(title="id of the project")
SNAPSHOT_ID = Path(title="id of the snapshot")
GRAPH_ID = Path(title="id of snapshot graph")


@api_read_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_read_router.get("/version")
async def version():
    return {"version": evidently.__version__}


@api_read_router.get("/projects")
async def list_projects() -> Sequence[ProjectBase]:
    workspace: Workspace = app.state.workspace
    projects = workspace.list_projects()
    event_logger.send_event(SERVICE_INTERFACE, "list_projects", project_count=len(projects))
    return projects


@api_read_router.get("/projects/{project_id}/reports")
async def list_reports(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[ReportModel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    reports = [ReportModel.from_report(r) for r in project.reports.values()]
    event_logger.send_event(SERVICE_INTERFACE, "list_reports", reports_count=len(reports))
    return reports


@api_read_router.get("/projects/{project_id}/info")
async def get_project_info(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> ProjectBase:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    event_logger.send_event(SERVICE_INTERFACE, "get_project_info")
    return project


@api_read_router.get("/projects/search/{project_name}")
async def search_projects(project_name: Annotated[str, "Name of the project to search"]) -> List[Project]:
    workspace: Workspace = app.state.workspace
    event_logger.send_event(SERVICE_INTERFACE, "search_projects")
    return workspace.search_project(project_name=project_name)


@api_write_router.post("/projects/{project_id}/info")
async def update_project_info(project_id: Annotated[uuid.UUID, PROJECT_ID], data: ProjectBase) -> ProjectBase:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    project.description = data.description
    project.name = data.name
    project.date_from = data.date_from
    project.date_to = data.date_to
    project.save()
    event_logger.send_event(SERVICE_INTERFACE, "update_project_info")
    return project


@api_read_router.get("/projects/{project_id}/test_suites")
async def list_test_suites(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[TestSuiteModel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    event_logger.send_event(SERVICE_INTERFACE, "list_test_suites")
    return [TestSuiteModel.from_report(r) for r in project.test_suites.values()]


@api_read_router.get("/projects/{project_id}/{snapshot_id}/graphs_data/{graph_id}")
async def get_snapshot_graph_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
    graph_id: Annotated[str, GRAPH_ID],
) -> Response:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    snapshot = project.get_snapshot(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    graph = snapshot.additional_graphs.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    event_logger.send_event(SERVICE_INTERFACE, "get_snapshot_graph_data")
    return Response(media_type="application/json", content=json.dumps(graph, cls=NumpyEncoder))


@api_read_router.get("/projects/{project_id}/{snapshot_id}/download")
async def get_snapshot_download(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
    report_format: str = "html",
) -> Response:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    snapshot = project.get_snapshot(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    if report_format == "html":
        return Response(
            snapshot.report.get_html(), headers={"content-disposition": f"attachment;filename={snapshot_id}.html"}
        )
    if report_format == "json":
        return Response(
            snapshot.report.json(), headers={"content-disposition": f"attachment;filename={snapshot_id}.json"}
        )
    event_logger.send_event(SERVICE_INTERFACE, "get_snapshot_download")
    return Response(f"Unknown format {report_format}", status_code=400)


@api_read_router.get("/projects/{project_id}/{snapshot_id}/data")
async def get_snapshot_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID],
) -> Response:  # DashboardInfoModel:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    snapshot = project.get_snapshot(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    info = DashboardInfoModel.from_dashboard_info(snapshot.dashboard_info)
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    event_logger.send_event(
        SERVICE_INTERFACE,
        "get_snapshot_data",
        snapshot_type="report" if snapshot.value.is_report else "test_suite",
        metrics=[m.get_id() for m in snapshot.value.first_level_metrics()],
        metric_presets=snapshot.value.metadata.get(METRIC_PRESETS, []),
        metric_generators=snapshot.value.metadata.get(METRIC_GENERATORS, []),
        tests=[t.get_id() for t in snapshot.value.first_level_tests()],
        test_presets=snapshot.value.metadata.get(TEST_PRESETS, []),
        test_generators=snapshot.value.metadata.get(TEST_GENERATORS, []),
    )
    return Response(media_type="application/json", content=json_str)


@api_read_router.get("/projects/{project_id}/dashboard/panels")
async def list_project_dashboard_panels(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
) -> List[DashboardPanel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    event_logger.send_event(SERVICE_INTERFACE, "list_project_dashboard_panels")
    return list(project.dashboard.panels)


@api_read_router.get("/projects/{project_id}/dashboard")
async def project_dashboard(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    timestamp_start: Optional[datetime.datetime] = None,
    timestamp_end: Optional[datetime.datetime] = None,
) -> Response:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    info = DashboardInfoModel.from_dashboard_info(
        project.build_dashboard_info(timestamp_start=timestamp_start, timestamp_end=timestamp_end)
    )
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    event_logger.send_event(SERVICE_INTERFACE, "project_dashboard")
    return Response(media_type="application/json", content=json_str)


@api_write_router.post("/projects")
async def add_project(project: Project) -> ProjectBase:
    workspace: Workspace = app.state.workspace
    p = workspace.add_project(project)
    event_logger.send_event(SERVICE_INTERFACE, "add_project")
    return p


@api_write_router.delete("/projects/{project_id}")
def delete_project(project_id: Annotated[uuid.UUID, PROJECT_ID]):
    workspace: Workspace = app.state.workspace
    workspace.delete_project(project_id)
    event_logger.send_event(SERVICE_INTERFACE, "delete_project")


@api_read_router.post("/projects/{project_id}/snapshots")
async def add_snapshot(project_id: Annotated[uuid.UUID, PROJECT_ID], snapshot: Snapshot):
    workspace: Workspace = app.state.workspace
    if workspace.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    workspace.add_snapshot(project_id, snapshot)
    event_logger.send_event(SERVICE_INTERFACE, "add_snapshot")


@api_write_router.delete("/projects/{project_id}/{snapshot_id}")
def delete_snapshot(project_id: Annotated[uuid.UUID, PROJECT_ID], snapshot_id: Annotated[uuid.UUID, SNAPSHOT_ID]):
    workspace: Workspace = app.state.workspace
    workspace.delete_snapshot(project_id, snapshot_id)
    event_logger.send_event(SERVICE_INTERFACE, "delete_snapshot")


api_router.include_router(api_read_router)
api_router.include_router(api_write_router)
app.include_router(api_router)


def run(host: str = "0.0.0.0", port: int = 8000, workspace: str = "workspace", secret: str = None):
    if secret is not None:
        set_secret(secret)
    app.state.workspace_path = workspace
    uvicorn.run(app, host=host, port=port)


def main():
    run()


if __name__ == "__main__":
    main()
