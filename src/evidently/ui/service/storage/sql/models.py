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
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from evidently._pydantic_compat import parse_obj_as
from evidently.core.metric_types import Metric
from evidently.core.serialization import SnapshotModel
from evidently.legacy.core import new_id
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import BlobMetadata
from evidently.ui.service.base import Project
from evidently.ui.service.base import User
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


# Indexes for better query performance
snapshots_project_id_index = Index("snapshots_project_id_idx", SnapshotSQLModel.project_id)


class MetricsSQLModel(Base):
    """Metrics model for SQL storage."""

    __tablename__ = "metrics"

    metric_fingerprint: Mapped[str] = mapped_column("metric_hash", index=True, primary_key=True)
    metric_json: Mapped[str]

    @property
    def metric(self) -> Metric:
        """Get metric object from JSON."""
        return parse_obj_as(Metric, json.loads(self.metric_json))


class PointSQLModel(Base):
    """Point model for storing metric data points."""

    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[ProjectID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    snapshot_id: Mapped[SnapshotID] = mapped_column(ForeignKey("snapshots.id", ondelete="CASCADE"))

    metric_fingerprint: Mapped[str] = mapped_column("metric_hash", index=True)
    timestamp: Mapped[datetime.datetime]

    field_path: Mapped[str] = mapped_column(index=True)
    value: Mapped[str]


# Composite index for better query performance
composite_index = Index("points_snapshot_id_field_path_idx", PointSQLModel.snapshot_id, PointSQLModel.field_path)


class BlobSQLModel(Base):
    """Blob model for storing binary data."""

    __tablename__ = "blobs"

    id: Mapped[str] = mapped_column(primary_key=True)
    data: Mapped[str]
    size: Mapped[int]

    def to_blob_metadata(self):
        """Convert to blob metadata."""
        from evidently.ui.service.base import BlobMetadata

        return BlobMetadata(id=self.id, size=self.size)
