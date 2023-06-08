import json
import uuid
from typing import Annotated
from typing import List

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Path
from starlette.responses import Response

from evidently.utils import NumpyEncoder

from .models import DashboardInfoModel
from .models import ProjectModel
from .models import ReportModel
from .workspace import Workspace

app = FastAPI()
workspace = Workspace(".")

api_router = APIRouter(prefix="/api")

PROJECT_ID = Path(title="id of the project")
REPORT_ID = Path(title="id of the report")


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.get("/projects")
async def list_projects() -> List[ProjectModel]:
    return [ProjectModel.from_project(p) for p in workspace.list_projects()]


@api_router.get("/projects/{project_id}/reports")
async def list_reports(project_id: Annotated[uuid.UUID, PROJECT_ID]) -> List[ReportModel]:
    return [ReportModel.from_report(r) for r in workspace.list_project_reports(project_id)]


@api_router.get("/projects/{project_id}/reports/{report_id}/data")
async def get_report_data(
    project_id: Annotated[uuid.UUID, PROJECT_ID], report_id: Annotated[uuid.UUID, REPORT_ID]
) -> Response:  # DashboardInfoModel:
    info = DashboardInfoModel.from_dashboard_info(workspace.get_report_dashboard_info(project_id, report_id))
    # todo: add numpy encoder to fastapi
    # return info
    json_str = json.dumps(info.dict(), cls=NumpyEncoder).encode("utf-8")
    return Response(media_type="application/json", content=json_str)


app.include_router(api_router)


def run(workspace_path: str):
    global workspace
    workspace = Workspace(workspace_path)
    uvicorn.run(app)


def main():
    run(".")


if __name__ == "__main__":
    main()
