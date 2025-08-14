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
from litestar import patch
from litestar import post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.params import Dependency
from litestar.params import Parameter
from typing_extensions import Annotated

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.report import Snapshot
from evidently.core.serialization import SnapshotModel
from evidently.legacy.model.dashboard import DashboardInfo
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.report.report import METRIC_GENERATORS
from evidently.legacy.report.report import METRIC_PRESETS
from evidently.legacy.test_suite.test_suite import TEST_GENERATORS
from evidently.legacy.test_suite.test_suite import TEST_PRESETS
from evidently.legacy.ui.api.models import DashboardInfoModel
from evidently.legacy.utils import NumpyEncoder
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.api.models import ReportModel
from evidently.ui.service.base import BatchMetricData
from evidently.ui.service.base import Project
from evidently.ui.service.base import SeriesResponse
from evidently.ui.service.managers.projects import ProjectManager
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID
from evidently.ui.service.type_aliases import TeamID
from evidently.ui.service.type_aliases import UserID


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
    user_id: UserID,
    project: Annotated[Project, Dependency()],
    project_manager: Annotated[ProjectManager, Dependency()],
    log_event: Callable,
) -> List[ReportModel]:
    snapshots = await project_manager.list_snapshots(user_id, project.id)
    reports = [ReportModel.from_snapshot(s) for s in snapshots]
    log_event("list_reports", reports_count=len(reports))
    return reports


@get("/{project_id:uuid}/snapshots")
async def list_snapshots(
    project: Annotated[Project, Dependency()],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> List[SnapshotMetadataModel]:
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


@get("/{project_id:uuid}/{snapshot_id:uuid}/graphs_data/{graph_id:str}")
async def get_snapshot_graph_data(
    user_id: UserID,
    project_id: ProjectID,
    snapshot_id: SnapshotID,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    graph_id: Annotated[str, Parameter(title="id of graph in snapshot")],
    log_event: Callable,
) -> str:
    snapshot = await project_manager.load_snapshot(user_id, project_id, snapshot_id)
    log_event("get_snapshot_graph_data")
    for widget in snapshot.widgets:
        for graph in widget.additionalGraphs:
            if graph_id == graph.id:
                return json.dumps(graph.dict() if not isinstance(graph, dict) else graph, cls=NumpyEncoder)
    raise HTTPException(status_code=404, detail="Graph not found")


@get("/{project_id:uuid}/{snapshot_id:uuid}/download")
async def get_snapshot_download(
    user_id: UserID,
    project_id: ProjectID,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    snapshot_metadata: Annotated[SnapshotMetadataModel, Dependency()],
    log_event: Callable,
    report_format: str = "html",
) -> Response:
    snapshot = await project_manager.load_snapshot(user_id, project_id, snapshot_metadata.id)
    s = Snapshot.load_dict(snapshot.dict())
    if report_format == "html":
        return Response(
            s.get_html_str(as_iframe=False).encode("utf8"),
            headers={"content-disposition": f"attachment;filename={snapshot_metadata.id}.html"},
        )
    if report_format == "json":
        return Response(
            s.json().encode("utf8"),
            headers={"content-disposition": f"attachment;filename={snapshot_metadata.id}.json"},
        )
    log_event("get_snapshot_download")
    raise HTTPException(status_code=400, detail=f"Unknown format {report_format}")


@get("/{project_id:uuid}/{snapshot_id:uuid}/data")
async def get_snapshot_data(
    user_id: UserID,
    project_id: ProjectID,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    snapshot_metadata: Annotated[SnapshotMetadataModel, Dependency()],
    log_event: Callable,
) -> str:
    snapshot = await project_manager.load_snapshot(user_id, project_id, snapshot_metadata.id)
    info = DashboardInfo(name="", widgets=snapshot.widgets + snapshot.tests_widgets)

    log_event(
        "get_snapshot_data",
        snapshot_type="report",
        metrics=[m for m in snapshot.top_level_metrics],
        metric_presets=snapshot.metadata.get(METRIC_PRESETS, []),
        metric_generators=snapshot.metadata.get(METRIC_GENERATORS, []),
        tests=[],
        test_presets=snapshot.metadata.get(TEST_PRESETS, []),
        test_generators=snapshot.metadata.get(TEST_GENERATORS, []),
    )
    return json.dumps(info.dict(), cls=NumpyEncoder)


@get("/{project_id:uuid}/{snapshot_id:uuid}/metadata")
async def get_snapshot_metadata(
    snapshot_metadata: Annotated[SnapshotMetadataModel, Dependency()],
    log_event: Callable,
) -> SnapshotMetadataModel:
    log_event(
        "get_snapshot_metadata",
        snapshot_type="report",
        metric_presets=snapshot_metadata.metadata.get(METRIC_PRESETS, []),
        metric_generators=snapshot_metadata.metadata.get(METRIC_GENERATORS, []),
        test_presets=snapshot_metadata.metadata.get(TEST_PRESETS, []),
        test_generators=snapshot_metadata.metadata.get(TEST_GENERATORS, []),
    )
    return snapshot_metadata


@get("/{project_id:uuid}")
async def get_dashboard(
    user_id: UserID,
    project_id: ProjectID,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
) -> DashboardModel:
    dashboard = await project_manager.get_project_dashboard(user_id, project_id)
    log_event("project_dashboard")
    return dashboard


@post("/{project_id:uuid}")
async def update_dashboard(
    user_id: UserID,
    project_id: ProjectID,
    data: DashboardModel,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
) -> DashboardModel:
    dashboard = await project_manager.save_project_dashboard(user_id, project_id, data)
    log_event("save_project_dashboard")
    return dashboard


@post("/")
async def add_project(
    data: Project,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
    org_id: Optional[OrgID] = None,
) -> ProjectID:
    if org_id is None and data.org_id is not None:
        org_id = data.org_id

    p = await project_manager.add_project(data, user_id, org_id)
    log_event("add_project")
    return p.id


@patch("/{project_id:uuid}")
async def update_project(
    user_id: UserID,
    project_id: ProjectID,
    data: Project,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
) -> ProjectID:
    if data.id != project_id:
        raise ValueError("id in data must be equal to project id")
    await project_manager.update_project(user_id, data)
    return data.id


@delete("/{project_id:uuid}")
async def delete_project(
    project_id: Annotated[ProjectID, Parameter(title="id of project")],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Callable,
    user_id: UserID,
) -> None:
    await project_manager.delete_project(user_id, project_id)
    log_event("delete_project")


class AddSnapshotResponse(BaseModel):
    snapshot_id: SnapshotID


@post("/{project_id:uuid}")
async def add_snapshot(
    project: Annotated[Project, Dependency()],
    body: bytes,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    log_event: Annotated[Callable, Dependency()],
    user_id: UserID,
) -> AddSnapshotResponse:
    model = parse_obj_as(SnapshotModel, json.loads(body))
    snapshot_id = await project_manager.add_snapshot(user_id, project.id, model)
    log_event("add_snapshot")
    return AddSnapshotResponse(snapshot_id=snapshot_id)


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


class MetricsList(BaseModel):
    metrics: List[str]


class LabelsList(BaseModel):
    labels: List[str]


class LabelValuesList(BaseModel):
    label_values: List[str]


@get("/{project_id:uuid}/metrics")
async def get_snapshots_metrics(
    project_id: ProjectID,
    user_id: UserID,
    tags: Optional[str],
    metadata: Optional[str],
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
) -> MetricsList:
    _tags: List[str] = [] if tags is None else json.loads(tags)
    _metadata: Dict[str, str] = {} if metadata is None else json.loads(metadata)
    metrics = await project_manager.get_metrics(user_id, project_id, _tags, _metadata)
    return MetricsList(metrics=metrics)


@get("/{project_id:uuid}/labels")
async def get_snapshots_metric_labels(
    project_id: ProjectID,
    user_id: UserID,
    tags: Optional[str],
    metadata: Optional[str],
    metric_type: str,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
) -> LabelsList:
    _tags: List[str] = [] if tags is None else json.loads(tags)
    _metadata: Dict[str, str] = {} if metadata is None else json.loads(metadata)
    labels = await project_manager.get_metric_labels(user_id, project_id, _tags, _metadata, metric_type)
    return LabelsList(labels=labels)


@get("/{project_id:uuid}/label_values")
async def get_snapshots_metric_label_values(
    project_id: ProjectID,
    user_id: UserID,
    tags: Optional[str],
    metadata: Optional[str],
    metric_type: str,
    label: str,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
) -> LabelValuesList:
    _tags: List[str] = [] if tags is None else json.loads(tags)
    _metadata: Dict[str, str] = {} if metadata is None else json.loads(metadata)
    values = await project_manager.get_metric_label_values(user_id, project_id, _tags, _metadata, metric_type, label)
    return LabelValuesList(label_values=values)


@post("/{project_id:uuid}/data_series_batch")
async def get_snapshots_metrics_data_batch(
    project_id: ProjectID,
    user_id: UserID,
    data: BatchMetricData,
    project_manager: Annotated[ProjectManager, Dependency(skip_validation=True)],
    timestamp_start: Optional[str] = None,
    timestamp_end: Optional[str] = None,
) -> SeriesResponse:
    timestamp_start_ = datetime.datetime.fromisoformat(timestamp_start) if timestamp_start else None
    timestamp_end_ = datetime.datetime.fromisoformat(timestamp_end) if timestamp_end else None
    series = await project_manager.get_data_series(
        user_id,
        project_id,
        data.series_filter or [],
        timestamp_start_,
        timestamp_end_,
    )
    return series


# We need this endpoint to export
# some additional models to open api schema
@get("/models/additional")
async def additional_models() -> (
    List[
        Union[
            BaseWidgetInfo,
            DashboardInfoModel,
        ]
    ]
):
    return []


def create_projects_api(guard: Callable) -> Router:
    projects_router_v1 = Router(
        "/projects",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    list_projects,
                    list_reports,
                    get_project_info,
                    search_projects,
                    get_snapshot_graph_data,
                    get_snapshot_data,
                    get_snapshot_download,
                    list_snapshots,
                    get_snapshot_metadata,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[
                    add_project,
                    delete_project,
                    update_project_info,
                    reload_project_snapshots,
                    delete_snapshot,
                ],
                guards=[guard],
            ),
        ],
    )
    projects_router_v2 = Router(
        "/projects",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    list_projects,
                    additional_models,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[
                    add_project,
                    update_project,
                    delete_project,
                ],
                guards=[guard],
            ),
        ],
    )

    dashboard_router_v2 = Router(
        "/dashboards",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    get_dashboard,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[
                    update_dashboard,
                ],
                guards=[guard],
            ),
        ],
    )
    snapshots_router_v2 = Router(
        "/snapshots",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    get_snapshots_metrics_data_batch,
                    get_snapshots_metrics,
                    get_snapshots_metric_labels,
                    get_snapshots_metric_label_values,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[add_snapshot],
                guards=[guard],
            ),
        ],
    )
    return Router(
        "",
        route_handlers=[
            Router("", route_handlers=[projects_router_v1]),
            Router("v2", route_handlers=[projects_router_v2, snapshots_router_v2, dashboard_router_v2]),
        ],
    )


projects_api_dependencies: Dict[str, Provide] = {
    "project": Provide(path_project_dependency),
    "snapshot_metadata": Provide(path_snapshot_metadata_dependency),
}
