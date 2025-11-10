import datetime
import json
from io import BytesIO
from json import JSONDecodeError
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from litestar import Router
from litestar import delete
from litestar import get
from litestar import patch
from litestar import post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.exceptions import ValidationException
from litestar.params import Body
from litestar.params import Dependency
from litestar.params import Parameter
from litestar.response.base import ASGIResponse
from typing_extensions import Annotated
from typing_extensions import TypeAlias

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Extra
from evidently._pydantic_compat import ValidationError
from evidently._pydantic_compat import create_model
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.ui.api.models import EvidentlyAPIModel
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import UserID
from evidently.ui.service.datasets.data_source import DataSourceDTO
from evidently.ui.service.datasets.data_source import SortBy
from evidently.ui.service.datasets.filters import FilterBy
from evidently.ui.service.datasets.filters import FilterByNumber
from evidently.ui.service.datasets.filters import FilterByString
from evidently.ui.service.datasets.metadata import DatasetMetadata
from evidently.ui.service.datasets.metadata import DatasetMetadataFull
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.datasets.models import DatasetPagination
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager
from evidently.ui.service.managers.datasets import DatasetManager
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import SnapshotID


class UploadDatasetRequest(BaseModel):
    """Request for uploading a dataset."""

    class Config:
        extra = Extra.forbid
        arbitrary_types_allowed = True

    name: str
    file: UploadFile
    description: Optional[str] = None
    data_definition_str: Optional[str] = None
    metadata_str: str = ""
    tags_str: str = ""

    @property
    def metadata(self) -> Dict[str, MetadataValueType]:
        """Parse metadata from string."""
        if not self.metadata_str:
            return {}
        return parse_obj_as(Dict[str, MetadataValueType], json.loads(self.metadata_str))

    @property
    def tags(self) -> List[str]:
        """Parse tags from string."""
        if not self.tags_str:
            return []
        return parse_obj_as(List[str], json.loads(self.tags_str))

    @property
    def data_definition(self) -> Optional[DataDefinition]:
        """Parse data definition from string."""
        if self.data_definition_str:
            return parse_obj_as(DataDefinition, json.loads(self.data_definition_str))
        return None


class UploadDatasetResponse(EvidentlyAPIModel):
    """Response for dataset upload."""

    dataset: DatasetMetadata


class PatchDatasetRequest(EvidentlyAPIModel):
    """Request for updating a dataset."""

    name: Optional[str] = None
    description: Optional[str] = None
    data_definition: Optional[DataDefinition] = None
    metadata: Optional[Dict[str, MetadataValueType]] = None
    tags: Optional[List[str]] = None


@post("/upload")
async def upload_dataset(
    data: Annotated[UploadDatasetRequest, Body(media_type=RequestEncodingType.MULTI_PART)],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    snapshot_dataset_links: Annotated["SnapshotDatasetLinksManager", Dependency(skip_validation=True)],
    user_id: UserID,
    project_id: ProjectID,
    snapshot_id: Annotated[Optional[SnapshotID], Parameter(title="snapshot id")] = None,
    dataset_type: Annotated[Optional[str], Parameter(title="dataset type (input/output)")] = None,
    dataset_subtype: Annotated[Optional[str], Parameter(title="dataset subtype (current/reference)")] = None,
) -> UploadDatasetResponse:
    """Upload a dataset."""
    if snapshot_id is not None:
        if dataset_type is None or dataset_subtype is None:
            raise HTTPException(
                status_code=400, detail="snapshot_id, dataset_type and dataset_subtype must be specified together"
            )

    default_dd = (
        Dataset.from_pandas(pd.DataFrame()).data_definition if data.data_definition is None else data.data_definition
    )
    dataset = await dataset_manager.upload_dataset(
        user_id,
        project_id,
        data.name,
        data.description,
        data.file,
        default_dd,
        origin=DatasetOrigin.file,
        metadata=data.metadata,
        tags=data.tags,
    )

    if (
        snapshot_id is not None
        and dataset_type is not None
        and dataset_subtype is not None
        and snapshot_dataset_links is not None
    ):
        await snapshot_dataset_links.link_dataset_snapshot(
            project_id=project_id,
            snapshot_id=snapshot_id,
            dataset_id=dataset.id,
            dataset_type=dataset_type,
            dataset_subtype=dataset_subtype,
        )

    return UploadDatasetResponse(dataset=dataset)


@patch("/{dataset_id:uuid}")
async def update_dataset(
    dataset_id: Annotated[DatasetID, Parameter(title="dataset id")],
    data: Annotated[PatchDatasetRequest, Body()],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
) -> None:
    """Update a dataset."""
    await dataset_manager.update_dataset(
        user_id, dataset_id, data.name, data.description, data.data_definition, data.metadata, data.tags
    )


@delete("/{dataset_id:uuid}")
async def delete_dataset(
    dataset_id: Annotated[DatasetID, Parameter(title="dataset id")],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
) -> None:
    """Delete a dataset."""
    await dataset_manager.delete_dataset(user_id, dataset_id)


@get("/{dataset_id:uuid}")
async def get_dataset(
    dataset_id: Annotated[DatasetID, Parameter(title="dataset id")],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    page_size: Annotated[int, Parameter(gt=0)] = 10,
    current_page: Annotated[int, Parameter(gt=0)] = 1,
    sort_by_column: Optional[str] = None,
    sort_ascending: Optional[bool] = True,
    filters: Optional[List[str]] = None,
) -> DatasetPagination:
    """Get a dataset with pagination."""

    try:
        filter_queries = [parse_obj_as(FilterBy, json.loads(_filter)) for _filter in filters] if filters else None
    except (ValidationError, JSONDecodeError) as e:
        raise ValidationException(str(e)) from e

    sort_by = SortBy(column=sort_by_column, ascending=sort_ascending) if sort_by_column else None
    result = await dataset_manager.get_dataset_pagination(
        user_id, dataset_id, page_size, current_page, sort_by, filter_queries
    )
    return result


@get("/{dataset_id:uuid}/download")
async def download_dataset(
    dataset_id: Annotated[DatasetID, Parameter(title="dataset id")],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    format: str = "parquet+sdk",
) -> ASGIResponse:
    """Download a dataset."""
    dataset = await dataset_manager.get_dataset_metadata(user_id, dataset_id)
    df, _ = await dataset_manager.get_dataset(user_id, dataset_id)

    buf = BytesIO()
    file_format: str
    if "parquet" in format.split("+"):
        df.to_parquet(buf)
        file_format = "parquet"
    elif "csv" in format.split("+"):
        df.to_csv(buf, index=False)
        file_format = "csv"
    else:
        raise HTTPException(status_code=400, detail="unsupported file format")

    metadata: str = dataset.json(exclude_none=True, exclude_defaults=True)

    boundary = "----LitestarBoundary123"

    def generate():
        yield f"--{boundary}\r\n".encode()
        yield b"Content-Type: application/json\r\n\r\n"
        yield metadata.encode() + b"\r\n"

        yield f"--{boundary}\r\n".encode()
        yield b"Content-Type: application/octet-stream\r\n\r\n"
        yield buf.getvalue() + b"\r\n"

        yield f"--{boundary}--\r\n".encode()

    if "sdk" in format.split("+"):
        return ASGIResponse(
            body=b"".join(generate()),
            media_type=f"multipart/mixed; boundary={boundary}",
        )
    return ASGIResponse(
        body=buf.getvalue(),
        media_type="application/octet-stream",
        headers=[("Content-Disposition", f"attachment; filename={dataset_id}.{file_format}")],
    )


class DatasetMetadataResponse(EvidentlyAPIModel):
    """Response for dataset metadata."""

    id: DatasetID
    project_id: ProjectID
    name: str
    description: str
    size_bytes: int
    created_at: datetime.datetime
    author_name: str
    row_count: int
    column_count: int
    origin: DatasetOrigin
    metadata: Dict[str, MetadataValueType]
    tags: List[str]

    @classmethod
    def from_dataset_metadata(cls, dataset: DatasetMetadataFull):
        """Create from DatasetMetadataFull."""
        return cls(**{k: v for k, v in dataset.__dict__.items() if k in cls.__fields__})


class ListDatasetResponse(EvidentlyAPIModel):
    """Response for listing datasets."""

    datasets: List[DatasetMetadataResponse]


@get("/")
async def list_datasets(
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    project_id: Optional[ProjectID] = None,
    limit: Annotated[Optional[int], Parameter(title="Page size")] = None,
    origin: Annotated[Optional[List[DatasetOrigin]], Parameter(schema_extra={"type": "array"})] = None,
    draft: Annotated[Optional[bool], Parameter(title="Return draft datasets")] = False,
) -> ListDatasetResponse:
    """List datasets."""
    if project_id is None:
        raise HTTPException(status_code=400, detail="project_id is required")
    datasets = await dataset_manager.list_datasets(user_id, project_id, limit, origin, draft)
    return ListDatasetResponse(datasets=[DatasetMetadataResponse.from_dataset_metadata(d) for d in datasets])


@get("/{dataset_id:uuid}/metadata")
async def get_dataset_metadata(
    dataset_id: Annotated[DatasetID, Parameter(title="dataset id")],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
) -> DatasetMetadata:
    """Get dataset metadata."""
    dataset = await dataset_manager.get_dataset_metadata(user_id, dataset_id)
    return dataset


class DatasetDataDefinitionResponse(EvidentlyAPIModel):
    """Response for data definition."""

    data_definition: DataDefinition
    all_columns: List[str]


@get("/{dataset_id:uuid}/data_definition")
async def get_data_definition(
    dataset_id: Annotated[DatasetID, Parameter()],
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
) -> DatasetDataDefinitionResponse:
    """Get data definition for a dataset."""
    dataset = await dataset_manager.get_dataset_metadata(user_id, dataset_id)
    return DatasetDataDefinitionResponse(data_definition=dataset.data_definition, all_columns=dataset.all_columns)


class MaterializeDatasetRequest(BaseModel):
    """Request for materializing a dataset from a source."""

    name: str
    description: Optional[str] = None
    source: DataSourceDTO
    metadata: Dict[str, MetadataValueType] = {}
    tags: List[str] = []


class MaterializeDatasetResponse(EvidentlyAPIModel):
    """Response for materializing a dataset."""

    dataset_id: DatasetID


@post("/materialize")
async def materialize_from_source(
    data: MaterializeDatasetRequest,
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    project_id: ProjectID,
) -> MaterializeDatasetResponse:
    """Materialize a dataset from a data source."""
    df = await data.source.to_data_source(user_id=user_id, project_id=project_id).materialize(dataset_manager)
    dataset = await dataset_manager.upload_dataset(
        user_id=user_id,
        project_id=project_id,
        name=data.name,
        description=data.description,
        data=df,
        data_definition=Dataset.from_pandas(df).data_definition,
        origin=DatasetOrigin.dataset,
        metadata=data.metadata,
        tags=data.tags,
    )
    return MaterializeDatasetResponse(dataset_id=dataset.id)


# We need this endpoint to export
# some additional models to open api schema
# TODO: fix this endpoint
_filter_model = create_model("Filters", by_string=(FilterByString, ...), by_number=(FilterByNumber, ...))  # type: ignore[call-overload]

FilterModel: TypeAlias = _filter_model  # type: ignore[valid-type]


@get("/models/additional")
async def additional_models() -> List[FilterModel]:  # type: ignore[valid-type]
    """Get additional schema for datasets."""
    return []


def datasets_api(guard: Callable) -> Router:
    """Create datasets API router."""
    return Router(
        "/datasets",
        route_handlers=[
            Router(
                "",
                route_handlers=[
                    additional_models,
                    upload_dataset,
                    update_dataset,
                    delete_dataset,
                    get_dataset,
                    list_datasets,
                    download_dataset,
                    get_dataset_metadata,
                    get_data_definition,
                    materialize_from_source,
                ],
            ),
        ],
    )
