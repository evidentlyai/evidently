import json
import uuid
from contextlib import asynccontextmanager
from typing import Annotated
from typing import List

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Path
from starlette.responses import FileResponse
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from evidently.utils import NumpyEncoder
from evidently_service.dashboards import DashboardConfig
from evidently_service.models import DashboardInfoModel
from evidently_service.models import ProjectModel
from evidently_service.models import ReportModel
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
    app.state.n_client.close()


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
    workspace = app.state.workspace
    return [ProjectModel.from_project(p) for p in workspace.list_projects()]


@api_router.get("/projects/{project_id}/reports")
async def list_reports(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[ReportModel]:
    workspace = app.state.workspace
    return [ReportModel.from_report(r) for r in workspace.list_project_reports(project_id)]


@api_router.get("/projects/{project_id}/reports/{report_id}/data")
async def get_report_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID], report_id: Annotated[uuid.UUID, REPORT_ID]
) -> Response:  # DashboardInfoModel:
    workspace = app.state.workspace
    info = DashboardInfoModel.from_dashboard_info(workspace.get_report_dashboard_info(project_id, report_id))
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    return Response(media_type="application/json", content=json_str)


@api_router.get("/projects/{project_id}/dashboards")
async def list_project_dashboards(
    project_id: Annotated[uuid.UUID, PROJECT_ID],
) -> List[DashboardConfig]:
    workspace: Workspace = app.state.workspace
    return workspace.list_project_dashboards(project_id)


@api_router.get("/projects/{project_id}/dashboards/{dashboard_id}/data")
async def get_dashboard_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID], dashboard_id: Annotated[uuid.UUID, Path(title="dashboard id")]
) -> Response:  # DashboardInfoModel
    workspace: Workspace = app.state.workspace
    info = DashboardInfoModel.from_dashboard_info(workspace.get_dashboard_dashboard_info(project_id, dashboard_id))
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    return Response(media_type="application/json", content=json_str)


@api_router.get("/sample_dashboard")
async def sample_dashboard():
    workspace: Workspace = app.state.workspace
    project_id = workspace.list_projects()[0].id
    dashboard_id = workspace.list_project_dashboards(project_id)[0].id
    info = DashboardInfoModel.from_dashboard_info(workspace.get_dashboard_dashboard_info(project_id, dashboard_id))
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    return Response(media_type="application/json", content=json_str)


app.include_router(api_router)


def run(workspace_path: str):
    app.state.workspace_path = workspace_path
    uvicorn.run(app)


def main():
    run("workspace")


if __name__ == "__main__":
    main()
