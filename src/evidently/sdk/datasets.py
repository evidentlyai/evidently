import io
import json
import typing
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from requests import Response

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.ui.workspace.cloud import NamedBytesIO
from evidently.legacy.ui.workspace.cloud import read_multipart_response
from evidently.sdk.models import SnapshotLink
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID

if typing.TYPE_CHECKING:
    from evidently.ui.workspace import RemoteWorkspace


class DatasetInfo(BaseModel):
    """Information about a dataset stored in the workspace.

    Contains metadata about a dataset including its size, dimensions, origin,
    and associated tags. Returned by `RemoteDatasetsManager.list` and used
    to identify datasets before loading them.
    """

    id: DatasetID
    """Unique dataset identifier."""
    project_id: ProjectID
    """Project this dataset belongs to."""
    name: str
    """Name of the dataset."""
    size_bytes: int
    """Size of the dataset in bytes."""
    row_count: int
    """Number of rows in the dataset."""
    column_count: int
    """Number of columns in the dataset."""
    description: str
    """Description of the dataset."""
    created_at: datetime
    """Creation timestamp."""
    author_name: Optional[str] = None
    """Optional name of the creator."""
    origin: str
    """Origin/source of the dataset."""
    tags: List[str]
    """List of tags associated with the dataset."""
    metadata: Dict[str, MetadataValueType]
    """Additional metadata as key-value pairs."""


class DatasetList(BaseModel):
    """List of datasets with metadata.

    Returned by `RemoteDatasetsManager.list` to provide information about
    all datasets in a project, optionally filtered by origin.
    """

    datasets: List[DatasetInfo]
    """List of `DatasetInfo` objects."""

    def __repr__(self):
        return "\n\n".join(
            f"Dataset: {d.name}\n"
            f"ID: {d.id}\n"
            f"Description: {d.description}\n"
            f"Origin: {d.origin}\n"
            f"Created: {d.created_at}\n"
            f"Size: {d.size_bytes} bytes\n"
            f"Row Count: {d.row_count} Column Count: {d.column_count}\n"
            f"Tags: {', '.join(d.tags)}\n"
            f"Metadata: {', '.join([f'{k}={v}' for k, v in d.metadata.items()])}"
            for d in self.datasets
        )


class RemoteDatasetsManager:
    """Manager for remote datasets stored in a workspace.

    Provides methods to list, load, and upload datasets to/from a remote workspace.
    Access via `RemoteWorkspace.datasets` property.
    """

    def __init__(self, workspace: "RemoteWorkspace", base_dataset_url: str):
        """Initialize the manager.

        Args:
        * `workspace`: `RemoteWorkspace` to use for API calls.
        * `base_dataset_url`: Base URL path for dataset API endpoints (e.g., `"/api/datasets"`).
        """
        self._ws = workspace
        self._base_path = base_dataset_url

    def list(self, project: STR_UUID, origins: Optional[List[str]] = None) -> DatasetList:
        """List all datasets in a project.

        Args:
        * `project`: Project ID.
        * `origins`: Optional list of origin filters (e.g., `["upload", "snapshot"]`).

        Returns:
        * `DatasetList` containing all matching datasets.
        """
        return self._ws._request(
            f"{self._base_path}",
            "GET",
            query_params={"project_id": project, "origin": ",".join(origins) if origins else None},
            response_model=DatasetList,
        )

    def load(self, dataset_id: DatasetID) -> Dataset:
        """Load a dataset by ID.

        Args:
        * `dataset_id`: ID of the dataset to load.

        Returns:
        * `Dataset` object with data and data definition.
        """
        response: Response = self._ws._request(f"{self._base_path}/{dataset_id}/download", "GET")

        metadata, file_content = read_multipart_response(response)

        df = pd.read_parquet(io.BytesIO(file_content))
        data_def = parse_obj_as(DataDefinition, metadata["data_definition"])
        return Dataset.from_pandas(df, data_definition=data_def)

    def add(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str] = None,
        link: Optional[SnapshotLink] = None,
    ):
        """Upload a dataset to the workspace.

        Args:
        * `project_id`: Project ID.
        * `dataset`: `Dataset` object to upload.
        * `name`: Name for the dataset.
        * `description`: Optional description.
        * `link`: Optional `SnapshotLink` to associate with a snapshot.

        Returns:
        * `DatasetID` of the uploaded dataset.
        """
        data_definition = dataset.data_definition.json(exclude_none=True)
        file = NamedBytesIO(b"", "data.parquet")
        dataset.as_dataframe().to_parquet(file)
        file.seek(0)
        qp = {"project_id": str(project_id)}
        if link is not None:
            qp["snapshot_id"] = str(link.snapshot_id)
            qp["dataset_type"] = link.dataset_type
            qp["dataset_subtype"] = link.dataset_subtype
        response: Response = self._ws._request(
            f"{self._base_path}/upload",
            "POST",
            body={
                "name": name,
                "description": description,
                "file": file,
                "data_definition_str": data_definition,
                "metadata_str": json.dumps(dataset.metadata),
                "tags_str": json.dumps(dataset.tags),
            },
            query_params=qp,
            form_data=True,
        )
        return DatasetID(response.json()["dataset"]["id"])
