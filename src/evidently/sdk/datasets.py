import io
import json
import typing
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from requests import Response

from evidently import DataDefinition
from evidently import Dataset
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.ui.workspace.cloud import NamedBytesIO
from evidently.legacy.ui.workspace.cloud import read_multipart_response
from evidently.sdk.models import SnapshotLink
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID

if typing.TYPE_CHECKING:
    from evidently.ui.workspace import CloudWorkspace


class DatasetInfo(BaseModel):
    id: DatasetID
    project_id: ProjectID
    name: str
    size_bytes: int
    row_count: int
    column_count: int
    description: str
    created_at: datetime
    origin: str
    tags: List[str]
    metadata: Dict[str, MetadataValueType]


class DatasetList(BaseModel):
    datasets: List[DatasetInfo]

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
    def __init__(self, workspace: "CloudWorkspace"):
        self._ws = workspace

    def list(self, project: STR_UUID, origins: Optional[List[str]] = None) -> DatasetList:
        return self._ws._request(
            "/api/v2/datasets",
            "GET",
            query_params={"project_id": project, "origin": ",".join(origins) if origins else None},
            response_model=DatasetList,
        )

    def load(self, dataset_id: DatasetID) -> Dataset:
        response: Response = self._ws._request(f"/api/v2/datasets/{dataset_id}/download", "GET")

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
            "/api/v2/datasets/upload",
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
