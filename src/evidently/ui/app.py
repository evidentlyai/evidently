import datetime
import json
import os
import pathlib
import uuid
from contextlib import asynccontextmanager
from typing import List
from typing import Optional

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from starlette.responses import FileResponse
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from typing_extensions import Annotated

from evidently.suite.base_suite import Snapshot
from evidently.telemetry import event_logger
from evidently.ui.dashboards import DashboardPanel
from evidently.ui.generate_workspace import main as generate_workspace_main
from evidently.ui.models import DashboardInfoModel
from evidently.ui.models import ProjectModel
from evidently.ui.models import ReportModel
from evidently.ui.models import TestSuiteModel
from evidently.ui.workspace import Project
from evidently.ui.workspace import Workspace
from evidently.utils import NumpyEncoder

SERVICE_INTERFACE = "service_backend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup
    Initialise the Client and add it to app.state
    """
    app.state.workspace = Workspace(app.state.workspace_path)

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


@app.get("/")
@app.get("/projects")
@app.get("/projects/{path:path}")
async def index(path=None):
    event_logger.send_event(SERVICE_INTERFACE, "index")
    return FileResponse(os.path.join(ui_path, "index.html"))


@app.get("/manifest.json")
async def manifest():
    return FileResponse(os.path.join(ui_path, "manifest.json"))


api_router = APIRouter(prefix="/api")

PROJECT_ID = Path(title="id of the project")
REPORT_ID = Path(title="id of the report")


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.get("/projects")
async def list_projects() -> List[ProjectModel]:
    workspace: Workspace = app.state.workspace
    projects = [ProjectModel.from_project(p) for p in workspace.list_projects()]
    event_logger.send_event(SERVICE_INTERFACE, "list_projects", project_count=len(projects))
    return projects


@api_router.get("/projects/{project_id}/reports")
async def list_reports(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[ReportModel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    reports = [ReportModel.from_report(r) for r in project.reports.values()]
    event_logger.send_event(SERVICE_INTERFACE, "list_reports", project_count=len(reports))
    return reports


@api_router.get("/projects/{project_id}/info")
async def get_project_info(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> ProjectModel:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    event_logger.send_event(SERVICE_INTERFACE, "get_project_info")
    return ProjectModel.from_project(project)


@api_router.post("/projects/{project_id}/info")
async def update_project_info(project_id: Annotated[uuid.UUID, PROJECT_ID], data: ProjectModel) -> ProjectModel:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    project.description = data.description
    project.name = data.project_name
    project.date_from = data.date_from
    project.date_to = data.date_to
    project.save()
    event_logger.send_event(SERVICE_INTERFACE, "get_project_info")
    return ProjectModel.from_project(project)


@api_router.get("/projects/{project_id}/test_suites")
async def list_test_suites(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[TestSuiteModel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    event_logger.send_event(SERVICE_INTERFACE, "get_project_info")
    return [TestSuiteModel.from_report(r) for r in project.test_suites.values()]


@api_router.get("/projects/{project_id}/{report_id}/graphs_data/{graph_id}")
async def get_report_graph_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    report_id: Annotated[uuid.UUID, REPORT_ID],
    graph_id: Annotated[str, REPORT_ID],
) -> Response:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    report = project.get_snapshot(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    graph = report.additional_graphs.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")
    event_logger.send_event(SERVICE_INTERFACE, "get_project_info")
    return Response(media_type="application/json", content=json.dumps(graph, cls=NumpyEncoder))


@api_router.get("/projects/{project_id}/{report_id}/download")
async def get_report_download(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    report_id: Annotated[uuid.UUID, REPORT_ID],
    report_format: str = "html",
) -> Response:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    report = project.get_snapshot(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report_format == "html":
        return Response(
            report.report.get_html(), headers={"content-disposition": f"attachment;filename={report_id}.html"}
        )
    if report_format == "json":
        return Response(report.report.json(), headers={"content-disposition": f"attachment;filename={report_id}.json"})
    event_logger.send_event(SERVICE_INTERFACE, "get_report_download")
    return Response(f"Unknown format {report_format}", status_code=400)


@api_router.get("/projects/{project_id}/{report_id}/data")
async def get_report_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    report_id: Annotated[uuid.UUID, REPORT_ID],
) -> Response:  # DashboardInfoModel:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    report = project.get_snapshot(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    info = DashboardInfoModel.from_dashboard_info(report.dashboard_info)
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    event_logger.send_event(SERVICE_INTERFACE, "get_report_data")
    return Response(media_type="application/json", content=json_str)


@api_router.get("/projects/{project_id}/dashboard/panels")
async def list_project_dashboard_panels(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
) -> List[DashboardPanel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    event_logger.send_event(SERVICE_INTERFACE, "list_project_dashboard_panels")
    return list(project.dashboard.panels)


@api_router.get("/projects/{project_id}/dashboard")
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


@api_router.post("/projects")
async def add_project(project: Project):
    workspace: Workspace = app.state.workspace
    workspace.add_project(project)
    event_logger.send_event(SERVICE_INTERFACE, "add_project")


@api_router.post("/projects/{project_id}/snapshots")
async def add_snapshot(project_id: Annotated[uuid.UUID, PROJECT_ID], snapshot: Snapshot):
    workspace: Workspace = app.state.workspace
    if workspace.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    workspace.add_snapshot(project_id, snapshot)
    event_logger.send_event(SERVICE_INTERFACE, "add_snapshot")


app.include_router(api_router)


def run(args):
    app.state.workspace_path = args.workspace
    uvicorn.run(app, host=args.host, port=args.port)


def generate_workspace(args):
    generate_workspace_main(args.workspace)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="evidently service")
    parser.add_argument("--workspace", help="path to workspace", default="workspace", required=False)
    subparsers = parser.add_subparsers()
    ui_parser = subparsers.add_parser("ui")
    ui_parser.add_argument("--port", help="port to start on", type=int, default=8000, required=False)
    ui_parser.add_argument("--host", help="host to start on", default="127.0.0.1", required=False)
    ui_parser.add_argument("--workspace", help="path to workspace", default="workspace", required=False)
    ui_parser.set_defaults(func=run)
    generator_parser = subparsers.add_parser("generate_workspace")
    generator_parser.set_defaults(func=generate_workspace)
    generator_parser.add_argument("--workspace", help="path to workspace", default="workspace", required=False)

    parsed = parser.parse_args(sys.argv[1:])
    parsed.func(parsed)


if __name__ == "__main__":
    main()
