import datetime
import json
import uuid
from threading import Lock
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import LargeBinary
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import DataDefinition
from evidently.core.metric_types import Metric
from evidently.core.serialization import SnapshotModel
from evidently.legacy.core import new_id
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import BlobMetadata
from evidently.ui.service.base import Project
from evidently.ui.service.base import User
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID
from evidently.ui.service.type_aliases import UserID

JSON_FIELD = Dict[str, Any]

create_db_lock = Lock()


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    type_annotation_map = {JSON_FIELD: JSON, List[str]: JSON, uuid.UUID: Uuid}

    @classmethod
    def create_all(cls, engine):
        """Create all tables for this base."""
        with create_db_lock:
            cls.metadata.create_all(engine)


class UserSQLModel(Base):
    """User model for SQL storage."""

    __tablename__ = "users"

    id: Mapped[UserID] = mapped_column(primary_key=True)
    name: Mapped[str]

    def to_user(self) -> User:
        """Convert model to User object."""
        return User(id=self.id, name=self.name)


class ProjectSQLModel(Base):
    """Project model for SQL storage."""

    __tablename__ = "projects"

    id: Mapped[ProjectID] = mapped_column(primary_key=True, default=new_id)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    dashboard_json: Mapped[JSON_FIELD]
    date_from: Mapped[Optional[datetime.datetime]] = None
    date_to: Mapped[Optional[datetime.datetime]] = None
    created_at: Mapped[Optional[datetime.datetime]] = None
    version: Mapped[str] = mapped_column(default="1")

    author_id: Mapped[UserID] = mapped_column(ForeignKey("users.id"))
    author: Mapped["UserSQLModel"] = relationship()

    def to_project(self) -> Project:
        """Convert model to Project object."""

        project = Project(
            id=self.id,
            name=self.name,
            description=self.description,
            date_from=self.date_from,
            date_to=self.date_to,
            created_at=self.created_at,
            version=self.version,
        )
        return project


class SnapshotSQLModel(Base):
    """Snapshot model for SQL storage."""

    __tablename__ = "snapshots"
    __table_args__ = (Index("snapshots_project_id_idx", "project_id"),)

    id: Mapped[SnapshotID] = mapped_column(primary_key=True, default=new_id)
    project_id: Mapped[ProjectID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))

    name: Mapped[Optional[str]]
    timestamp: Mapped[datetime.datetime]
    metadata_json: Mapped[JSON_FIELD]
    tags: Mapped[List[str]]

    blob_path: Mapped[str]
    blob_size: Mapped[int]

    @classmethod
    def from_snapshot(cls, snapshot: SnapshotModel, project_id: ProjectID, blob: BlobMetadata) -> "SnapshotSQLModel":
        """Create model from Snapshot object."""
        return SnapshotSQLModel(
            project_id=project_id,
            name=snapshot.name,
            timestamp=snapshot.timestamp,
            metadata_json=snapshot.metadata,
            tags=snapshot.tags,
            blob_path=blob.id,
            blob_size=blob.size,
        )

    def load(self, blob_storage) -> SnapshotModel:
        """Load snapshot from blob storage."""
        with blob_storage.open_blob(self.blob_path) as f:
            return parse_obj_as(SnapshotModel, json.load(f))

    def to_snapshot_metadata(self, project: Optional[Project]) -> SnapshotMetadataModel:
        """Convert model to SnapshotMetadataModel object."""
        return SnapshotMetadataModel(
            id=self.id,
            name=self.name,
            timestamp=self.timestamp,
            metadata=self.metadata_json,
            tags=self.tags,
            links=SnapshotLinks(),
        )


class MetricsSQLModel(Base):
    """Metrics model for SQL storage."""

    __tablename__ = "metrics"

    metric_fingerprint: Mapped[str] = mapped_column("metric_hash", index=True, primary_key=True)
    metric_json: Mapped[str]

    @property
    def metric(self) -> Metric:
        """Get metric object from JSON."""
        return parse_obj_as(Metric, json.loads(self.metric_json))  # type: ignore[type-abstract,return-value]


class PointSQLModel(Base):
    """Point model for storing metric data points."""

    __tablename__ = "points"
    __table_args__ = (Index("points_project_snapshot_idx", "project_id", "snapshot_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[ProjectID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    snapshot_id: Mapped[SnapshotID] = mapped_column(ForeignKey("snapshots.id", ondelete="CASCADE"))
    metric_type: Mapped[str]
    params: Mapped[Dict[str, str]] = mapped_column(JSON)
    value: Mapped[float]


class BlobSQLModel(Base):
    """Blob model for storing binary data."""

    __tablename__ = "blobs"

    id: Mapped[str] = mapped_column(primary_key=True)
    data: Mapped[bytes] = mapped_column(LargeBinary)
    size: Mapped[int]

    def to_blob_metadata(self):
        """Convert to blob metadata."""
        from evidently.ui.service.base import BlobMetadata

        return BlobMetadata(id=self.id, size=self.size)


class DatasetSQLModel(Base):
    """Dataset model for SQL storage."""

    __tablename__ = "datasets"

    id: Mapped[DatasetID] = mapped_column(primary_key=True, default=new_id)

    project_id: Mapped[ProjectID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    project: Mapped["ProjectSQLModel"] = relationship()

    author_id: Mapped[UserID] = mapped_column(ForeignKey("users.id"))
    author: Mapped["UserSQLModel"] = relationship()

    name: Mapped[str]
    description: Mapped[Optional[str]]

    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]

    data_definition: Mapped[JSON_FIELD]
    source: Mapped[JSON_FIELD]
    origin: Mapped[str]
    size_bytes: Mapped[int]
    row_count: Mapped[int]
    column_count: Mapped[int]

    all_columns: Mapped[List[str]]
    deleted: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    is_draft: Mapped[Optional[bool]] = mapped_column(nullable=False, default=False)
    draft_params: Mapped[JSON_FIELD] = mapped_column(nullable=True, default=None)

    metadata_json: Mapped[JSON_FIELD]
    tags: Mapped[List[str]]

    tracing_params: Mapped[JSON_FIELD] = mapped_column(nullable=True, default=None)

    def to_dataset_metadata(self):
        """Convert model to DatasetMetadataFull."""
        from evidently.ui.service.datasets.data_source import DataSource
        from evidently.ui.service.datasets.metadata import DatasetMetadataFull
        from evidently.ui.service.datasets.metadata import DatasetOrigin
        from evidently.ui.service.datasets.metadata import DatasetTracingParams

        return DatasetMetadataFull(
            name=self.name,
            size_bytes=self.size_bytes,
            row_count=self.row_count,
            column_count=self.column_count,
            description=self.description or "",
            id=self.id,
            project_id=self.project_id,
            author_id=self.author_id,
            all_columns=self.all_columns,
            data_definition=parse_obj_as(DataDefinition, self.data_definition),
            source=parse_obj_as(DataSource, self.source),
            created_at=self.created_at,
            updated_at=self.updated_at,
            author_name=self.author.name if self.author else "Unknown User",
            is_draft=self.is_draft,
            draft_params=self.draft_params,
            origin=DatasetOrigin(self.origin),
            metadata=self.metadata_json,
            tags=self.tags,
            tracing_params=parse_obj_as(DatasetTracingParams, self.tracing_params) if self.tracing_params else None,
        )

    @classmethod
    def from_dataset_metadata(
        cls, dataset, author_id: UserID, timestamp: Optional[datetime.datetime] = None
    ) -> "DatasetSQLModel":
        """Create model from DatasetMetadata."""
        timestamp = timestamp or datetime.datetime.now()
        return DatasetSQLModel(
            name=dataset.name,
            size_bytes=dataset.size_bytes,
            row_count=dataset.row_count,
            column_count=dataset.column_count,
            description=dataset.description,
            id=dataset.id,
            project_id=dataset.project_id,
            all_columns=dataset.all_columns,
            data_definition=json.loads(dataset.data_definition.json()),
            source=json.loads(dataset.source.json()),
            author_id=author_id,
            created_at=timestamp,
            updated_at=timestamp,
            is_draft=dataset.is_draft,
            draft_params=dataset.draft_params,
            origin=dataset.origin.value,
            metadata_json=dataset.metadata,
            tags=dataset.tags,
            tracing_params=json.loads(dataset.tracing_params.json()) if dataset.tracing_params else None,
        )


class SnapshotDatasetsSQLModel(Base):
    """SQL model for snapshot-dataset links."""

    __tablename__ = "snapshot_datasets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    snapshot_id: Mapped[SnapshotID] = mapped_column(ForeignKey("snapshots.id", ondelete="CASCADE"), index=True)
    dataset_id: Mapped[DatasetID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    dataset_type: Mapped[str]  # input/output etc
    dataset_subtype: Mapped[str]  # current/reference/ etc

    __table_args__ = (
        Index("ix_snapshot_datasets_snapshot_id", "snapshot_id"),
        Index("ix_snapshot_datasets_dataset_id", "dataset_id"),
    )
