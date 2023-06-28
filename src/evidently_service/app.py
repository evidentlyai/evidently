import datetime
import json
import uuid
from contextlib import asynccontextmanager
from typing import Annotated
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

from evidently.suite.base_suite import Snapshot
from evidently.utils import NumpyEncoder
from evidently_service.dashboards import DashboardPanel
from evidently_service.models import DashboardInfoModel
from evidently_service.models import ProjectModel
from evidently_service.models import ReportModel
from evidently_service.models import TestSuiteModel
from evidently_service.workspace import Project
from evidently_service.workspace import Workspace


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup
    Initialise the Client and add it to app.state
    """
    app.state.workspace = Workspace(app.state.workspace_path)
    yield
    """ Run on shutdown
        Close the connection
        Clear variables and release the resources
    """


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="ui/static"), name="static")


@app.get("/")
@app.get("/projects")
@app.get("/projects/{path:path}")
async def index(path=None):
    return FileResponse("ui/index.html")


@app.get("/manifest.json")
async def manifest():
    return FileResponse("ui/manifest.json")


api_router = APIRouter(prefix="/api")

PROJECT_ID = Path(title="id of the project")
REPORT_ID = Path(title="id of the report")


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.get("/projects")
async def list_projects() -> List[ProjectModel]:
    workspace: Workspace = app.state.workspace
    return [ProjectModel.from_project(p) for p in workspace.list_projects()]


@api_router.get("/projects/{project_id}/reports")
async def list_reports(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[ReportModel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    return [ReportModel.from_report(r) for r in project.reports.values()]


@api_router.get("/projects/{project_id}/test_suites")
async def list_test_suites(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[TestSuiteModel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    return [TestSuiteModel.from_report(r) for r in project.test_suites.values()]


@api_router.get("/projects/{project_id}/{report_id}/graphs_data/{graph_id}")
async def get_report_graph_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    report_id: Annotated[uuid.UUID, REPORT_ID],
    graph_id: Annotated[uuid.UUID, REPORT_ID],
) -> Response:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    report = project.get_snapshot(report_id).value.as_report()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    graphs = report.additional_graphs
    return Response(media_type="application/json", content=json.dumps(graphs.get(str(graph_id)), cls=NumpyEncoder))


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
    report = project.get_item(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report_format == "html":
        return Response(
            report.report.get_html(), headers={"content-disposition": f"attachment;filename={report_id}.html"}
        )
    if report_format == "json":
        return Response(report.report.json(), headers={"content-disposition": f"attachment;filename={report_id}.json"})


@api_router.get("/projects/{project_id}/{report_id}/data")
async def get_report_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
    report_id: Annotated[uuid.UUID, REPORT_ID],
) -> Response:  # DashboardInfoModel:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    report = project.get_item(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    info = DashboardInfoModel.from_dashboard_info(report.dashboard_info)
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    return Response(media_type="application/json", content=json_str)


@api_router.get("/projects/{project_id}/dashboard/panels")
async def list_project_dashboard_panels(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
) -> List[DashboardPanel]:
    workspace: Workspace = app.state.workspace
    project = workspace.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

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
    return Response(media_type="application/json", content=json_str)


@api_router.post("/projects")
async def add_project(project: Project):
    workspace: Workspace = app.state.workspace
    workspace.add_project(project)


@api_router.post("/projects/{project_id}/snapshots")
async def add_snapshot(project_id: Annotated[uuid.UUID, PROJECT_ID], snapshot: Snapshot):
    workspace: Workspace = app.state.workspace
    if workspace.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    workspace.add_snapshot(project_id, snapshot)




app.include_router(api_router)


def run(workspace_path: str):
    app.state.workspace_path = workspace_path
    uvicorn.run(app)


def main():
    run("workspace")


if __name__ == "__main__":
    main()
