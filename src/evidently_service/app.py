from typing import Annotated, List

import uvicorn
from fastapi import FastAPI, Path

from .models import ProjectModel, ReportModel
from .workspace import Workspace

app = FastAPI()
workspace = Workspace(".")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/projects")
async def list_projects() -> List[ProjectModel]:
    return [ProjectModel(project_name=p) for p in workspace.list_projects()]


@app.get("/projects/{project_name}")
async def list_reports(project_name: Annotated[str, Path(title="The name of the project to get reports for")]) -> List[ReportModel]:
    return [
        ReportModel.from_report(r) for r in workspace.list_project_reports(project_name)
    ]


def run(workspace_path: str):
    global workspace
    workspace = Workspace(workspace_path)
    uvicorn.run(app)


def main():
    run(".")


if __name__ == '__main__':
    main()
