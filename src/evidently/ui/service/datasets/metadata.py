import datetime
import json
import posixpath
import re
from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import EVIDENTLY_DATASET_EXT
from evidently.core.datasets import DataDefinition
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.ui.type_aliases import DatasetID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import UserID
from evidently.ui.service.datasets.data_source import DataSource
from evidently.ui.service.storage.fslocation import FSLocation

UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


class DatasetOrigin(Enum):
    """Origin of a dataset."""

    file = "file"
    tracing = "tracing"
    dataset = "dataset"


class DatasetTracingParams(BaseModel):
    """Parameters for tracing-based datasets."""

    session_type: Optional[str] = None
    session_field: Optional[str] = None
    user_field: Optional[str] = None
    dialog_split_time_seconds: Optional[int] = None
    user_message_field: Optional[str] = None
    assistant_message_field: Optional[str] = None


class DatasetMetadata(BaseModel):
    """Metadata for a dataset."""

    id: DatasetID
    project_id: ProjectID
    author_id: UserID
    name: str
    description: str
    data_definition: DataDefinition
    source: DataSource
    size_bytes: int
    row_count: int
    column_count: int
    all_columns: List[str]
    is_draft: bool
    draft_params: Optional[dict]
    origin: DatasetOrigin
    metadata: Dict[str, MetadataValueType] = {}
    tags: List[str] = []
    tracing_params: Optional[DatasetTracingParams] = None


class DatasetMetadataFull(DatasetMetadata):
    """Full dataset metadata with timestamps and author name."""

    created_at: datetime.datetime
    updated_at: datetime.datetime
    author_name: str


class DatasetMetadataStorage(ABC):
    """Interface for dataset metadata storage."""

    @abstractmethod
    async def add_dataset_metadata(
        self,
        user_id: UserID,
        project_id: ProjectID,
        dataset: DatasetMetadata,
    ) -> DatasetID:
        """Add a new dataset metadata."""
        raise NotImplementedError

    @abstractmethod
    async def update_dataset_metadata(self, dataset_id: DatasetID, new_metadata: DatasetMetadata):
        """Update dataset metadata."""
        raise NotImplementedError

    @abstractmethod
    async def update_dataset_tracing_metadata(self, dataset_id: DatasetID, tracing_metadata: DatasetTracingParams):
        """Update tracing metadata for a dataset."""
        raise NotImplementedError

    @abstractmethod
    async def get_dataset_metadata(self, dataset_id: DatasetID) -> Optional[DatasetMetadataFull]:
        """Get dataset metadata by ID."""
        raise NotImplementedError

    @abstractmethod
    async def mark_dataset_deleted(self, dataset_id: DatasetID):
        """Mark a dataset as deleted (soft delete)."""
        raise NotImplementedError

    @abstractmethod
    async def delete_dataset_metadata(self, dataset_id: DatasetID):
        """Permanently delete dataset metadata."""
        raise NotImplementedError

    @abstractmethod
    async def list_datasets_metadata(
        self,
        project_id: ProjectID,
        limit: Optional[int],
        origin: Optional[List[DatasetOrigin]],
        draft: Optional[bool],
    ) -> List[DatasetMetadataFull]:
        """List datasets metadata."""
        raise NotImplementedError

    @abstractmethod
    async def datasets_count(self, project_id: ProjectID) -> int:
        """Count datasets in a project."""
        raise NotImplementedError


class FileDatasetMetadataStorage(DatasetMetadataStorage):
    """File-based dataset metadata storage."""

    def __init__(self, base_path: str):
        self.location = FSLocation(base_path=base_path)

    def _dataset_dir(self, project_id: ProjectID, dataset_id: DatasetID) -> str:
        """Get the directory path for a dataset."""
        return posixpath.join(str(project_id), "datasets", str(dataset_id))

    def _metadata_path(self, project_id: ProjectID, dataset_id: DatasetID) -> str:
        """Get the metadata file path for a dataset."""
        return posixpath.join(self._dataset_dir(project_id, dataset_id), "metadata.json")

    def _data_path(self, project_id: ProjectID, dataset_id: DatasetID) -> str:
        """Get the dataset data file path."""
        return posixpath.join(self._dataset_dir(project_id, dataset_id), f"data.{EVIDENTLY_DATASET_EXT}")

    async def add_dataset_metadata(self, user_id: UserID, project_id: ProjectID, dataset: DatasetMetadata) -> DatasetID:
        """Add a new dataset metadata."""
        dataset_dir = self._dataset_dir(project_id, dataset.id)
        self.location.makedirs(dataset_dir)

        # Save metadata
        if not isinstance(dataset, DatasetMetadataFull):
            now = datetime.datetime.now()
            dataset = DatasetMetadataFull(**dataset.dict(), author_name="", created_at=now, updated_at=now)
        metadata_path = self._metadata_path(project_id, dataset.id)
        with self.location.open(metadata_path, "w") as f:
            f.write(dataset.json(indent=2))

        return dataset.id

    async def update_dataset_metadata(self, dataset_id: DatasetID, new_metadata: DatasetMetadata):
        """Update dataset metadata."""
        # Load existing metadata to get project_id
        existing = await self.get_dataset_metadata(dataset_id)
        if existing is None:
            raise ValueError(f"Dataset {dataset_id} not found")

        # Update metadata
        metadata_path = self._metadata_path(existing.project_id, dataset_id)
        if not self.location.exists(metadata_path):
            raise ValueError(f"Dataset {dataset_id} not found")

        # Update timestamps
        if not isinstance(new_metadata, DatasetMetadataFull):
            now = datetime.datetime.now()
            new_metadata = DatasetMetadataFull(
                **new_metadata.dict(),
                author_name=existing.author_name,
                created_at=existing.created_at.isoformat(),
                updated_at=now.isoformat(),
            )

        with self.location.open(metadata_path, "w") as f:
            f.write(new_metadata.json(indent=2))

    async def update_dataset_tracing_metadata(self, dataset_id: DatasetID, tracing_metadata: DatasetTracingParams):
        raise NotImplementedError("Tracing datasets are not yet supported")

    async def get_dataset_metadata(self, dataset_id: DatasetID) -> Optional[DatasetMetadataFull]:
        """Get dataset metadata by ID."""
        # Search all projects for the dataset
        for project_dir in self.location.listdir(""):
            if not UUID_REGEX.match(project_dir):
                continue
            project_id = project_dir
            datasets_dir = posixpath.join(project_id, "datasets")
            if not self.location.exists(datasets_dir):
                continue

            for dataset_dir in self.location.listdir(datasets_dir):
                if not UUID_REGEX.match(dataset_dir):
                    continue
                if dataset_dir != str(dataset_id):
                    continue

                metadata_path = self._metadata_path(project_id, dataset_id)
                if not self.location.exists(metadata_path):
                    continue

                with self.location.open(metadata_path, "r") as f:
                    metadata_dict = json.load(f)

                # Convert to DatasetMetadataFull
                return parse_obj_as(DatasetMetadataFull, metadata_dict)

        return None

    async def mark_dataset_deleted(self, dataset_id: DatasetID):
        """Mark a dataset as deleted (soft delete)."""
        existing = await self.get_dataset_metadata(dataset_id)
        if existing is None:
            raise ValueError(f"Dataset {dataset_id} not found")

        metadata_path = self._metadata_path(existing.project_id, dataset_id)
        if not self.location.exists(metadata_path):
            raise ValueError(f"Dataset {dataset_id} not found")

        # Load, mark as deleted, and save
        with self.location.open(metadata_path, "r") as f:
            metadata_dict = json.load(f)

        metadata_dict["deleted"] = True
        metadata_dict["updated_at"] = datetime.datetime.now().isoformat()

        with self.location.open(metadata_path, "w") as f:
            json.dump(metadata_dict, f, indent=2, default=str)

    async def delete_dataset_metadata(self, dataset_id: DatasetID):
        """Permanently delete dataset metadata."""
        existing = await self.get_dataset_metadata(dataset_id)
        if existing is None:
            raise ValueError(f"Dataset {dataset_id} not found")

        dataset_dir = self._dataset_dir(existing.project_id, dataset_id)
        if self.location.exists(dataset_dir):
            self.location.rmtree(dataset_dir)

    async def list_datasets_metadata(
        self,
        project_id: ProjectID,
        limit: Optional[int],
        origin: Optional[List[DatasetOrigin]],
        draft: Optional[bool],
    ) -> List[DatasetMetadataFull]:
        """List datasets metadata."""
        datasets_dir = posixpath.join(str(project_id), "datasets")
        if not self.location.exists(datasets_dir):
            return []

        datasets = []
        for dataset_dir in self.location.listdir(datasets_dir):
            if not UUID_REGEX.match(dataset_dir):
                continue

            dataset_id = dataset_dir
            metadata_path = self._metadata_path(project_id, dataset_id)
            if not self.location.exists(metadata_path):
                continue

            try:
                with self.location.open(metadata_path, "r") as f:
                    metadata_dict = json.load(f)

                # Skip if deleted
                if metadata_dict.get("deleted", False):
                    continue

                # Filter by origin
                if origin is not None:
                    dataset_origin = DatasetOrigin(metadata_dict.get("origin"))
                    if dataset_origin not in origin:
                        continue

                # Filter by draft
                if draft is not None:
                    is_draft = metadata_dict.get("is_draft", False)
                    if is_draft != draft:
                        continue

                dataset_metadata = parse_obj_as(DatasetMetadataFull, metadata_dict)
                datasets.append(dataset_metadata)
            except Exception:
                # Skip malformed datasets
                continue

        # Sort by created_at descending
        datasets.sort(key=lambda x: x.created_at, reverse=True)

        if limit is not None:
            datasets = datasets[:limit]

        return datasets

    async def datasets_count(self, project_id: ProjectID) -> int:
        """Count datasets in a project."""
        datasets_dir = posixpath.join(str(project_id), "datasets")
        if not self.location.exists(datasets_dir):
            return 0

        count = 0
        for dataset_dir in self.location.listdir(datasets_dir):
            if not UUID_REGEX.match(dataset_dir):
                continue

            dataset_id = dataset_dir
            metadata_path = self._metadata_path(project_id, dataset_id)
            if not self.location.exists(metadata_path):
                continue

            try:
                with self.location.open(metadata_path, "r") as f:
                    metadata_dict = json.load(f)

                # Don't count deleted datasets
                if metadata_dict.get("deleted", False):
                    continue

                count += 1
            except Exception:
                # Skip malformed datasets
                continue

        return count


class NoopDatasetMetadataStorage(DatasetMetadataStorage):
    """No-op implementation for testing."""

    async def add_dataset_metadata(self, user_id: UserID, project_id: ProjectID, dataset: DatasetMetadata) -> DatasetID:
        from evidently.legacy.ui.type_aliases import ZERO_UUID

        return ZERO_UUID

    async def update_dataset_metadata(self, dataset_id: DatasetID, new_metadata: DatasetMetadata):
        pass

    async def update_dataset_tracing_metadata(self, dataset_id: DatasetID, tracing_metadata: DatasetTracingParams):
        pass

    async def get_dataset_metadata(self, dataset_id: DatasetID) -> Optional[DatasetMetadataFull]:
        return None

    async def mark_dataset_deleted(self, dataset_id: DatasetID):
        pass

    async def delete_dataset_metadata(self, dataset_id: DatasetID):
        pass

    async def list_datasets_metadata(
        self,
        project_id: ProjectID,
        limit: Optional[int],
        origin: Optional[List[DatasetOrigin]],
        draft: Optional[bool],
    ) -> List[DatasetMetadataFull]:
        return []

    async def datasets_count(self, project_id: ProjectID) -> int:
        return 0
