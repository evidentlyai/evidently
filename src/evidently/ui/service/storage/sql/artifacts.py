import datetime
import json
from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from typing import Sequence

from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from evidently.legacy.core import new_id
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactMetadata
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionID
from evidently.sdk.artifacts import ArtifactVersionMetadata
from evidently.sdk.artifacts import VersionOrLatest
from evidently.ui.service.storage.artifacts import ArtifactStorage
from evidently.ui.service.storage.sql.base import BaseSQLStorage
from evidently.ui.service.storage.sql.models import Base
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID

if TYPE_CHECKING:
    from .models import ProjectSQLModel


class ArtifactModel(Base):
    __tablename__ = "artifacts"

    id: Mapped[ArtifactID] = mapped_column(primary_key=True, default=new_id)
    project_id: Mapped[ProjectID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    project: Mapped["ProjectSQLModel"] = relationship()

    author_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", use_alter=True), nullable=True)

    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]
    description: Mapped[Optional[str]]

    name: Mapped[str] = mapped_column(index=True)

    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_artifact_name_project_id"),)

    def to_artifact(self) -> Artifact:
        return Artifact(
            id=self.id,
            project_id=self.project_id,
            name=self.name,
            metadata=ArtifactMetadata(
                created_at=self.created_at,
                updated_at=self.updated_at,
                author=self.author_id,
                description=self.description,
            ),
        )

    @classmethod
    def from_artifact(cls, artifact: Artifact) -> "ArtifactModel":
        return ArtifactModel(
            id=artifact.id,
            project_id=artifact.project_id,
            name=artifact.name,
            author_id=artifact.metadata.author,
            created_at=artifact.metadata.created_at,
            updated_at=artifact.metadata.updated_at,
            description=artifact.metadata.description,
        )


class ArtifactVersionModel(Base):
    __tablename__ = "artifact_versions"

    id: Mapped[ArtifactVersionID] = mapped_column(primary_key=True, default=new_id)
    artifact_id: Mapped[ArtifactID] = mapped_column(ForeignKey("artifacts.id", ondelete="CASCADE"))
    artifact: Mapped["ArtifactModel"] = relationship()

    author_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", use_alter=True), nullable=True)

    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]
    comment: Mapped[Optional[str]]

    version: Mapped[int] = mapped_column(index=True)
    content: Mapped[str]

    __table_args__ = (UniqueConstraint("artifact_id", "version", name="uq_artifact_version_artifact_id"),)

    def to_artifact_version(self) -> ArtifactVersion:
        try:
            content = json.loads(self.content)
        except json.JSONDecodeError:
            content = self.content
        return ArtifactVersion(
            id=self.id,
            artifact_id=self.artifact_id,
            version=self.version,
            content=content,
            metadata=ArtifactVersionMetadata(
                created_at=self.created_at, updated_at=self.updated_at, author=self.author_id, comment=self.comment
            ),
        )

    @classmethod
    def from_artifact_version(cls, artifact_version: ArtifactVersion) -> "ArtifactVersionModel":
        return ArtifactVersionModel(
            id=artifact_version.id,
            artifact_id=artifact_version.artifact_id,
            version=artifact_version.version,
            content=artifact_version.content.json(),
            author_id=artifact_version.metadata.author,
            created_at=artifact_version.metadata.created_at,
            updated_at=artifact_version.metadata.updated_at,
            comment=artifact_version.metadata.comment,
        )


class SQLArtifactStorage(BaseSQLStorage, ArtifactStorage):
    async def list_artifacts(self, project_id: ProjectID) -> List[Artifact]:
        with self.session as session:
            artifacts: Sequence[ArtifactModel] = session.scalars(
                select(ArtifactModel).where(ArtifactModel.project_id == project_id)
            )
            return [a.to_artifact() for a in artifacts]

    async def get_artifact(self, artifact_id: ArtifactID) -> Optional[Artifact]:
        with self.session as session:
            try:
                artifact_model: ArtifactModel = session.get_one(ArtifactModel, artifact_id)
            except NoResultFound:
                return None
            return artifact_model.to_artifact()

    async def get_artifact_by_name(self, project_id: ProjectID, name: str) -> Optional[Artifact]:
        with self.session as session:
            artifact_model = session.scalar(
                select(ArtifactModel).where(ArtifactModel.project_id == project_id, ArtifactModel.name == name)
            )
            return artifact_model.to_artifact() if artifact_model is not None else None

    async def add_artifact(self, project_id: ProjectID, artifact: Artifact) -> Artifact:
        with self.session as session:
            model = ArtifactModel.from_artifact(artifact)
            if artifact.id == ZERO_UUID:
                model.id = new_id()
            model.project_id = project_id
            model.created_at = datetime.datetime.now()
            model.updated_at = datetime.datetime.now()
            session.add(model)
            a = model.to_artifact()
            try:
                session.commit()
            except IntegrityError:
                raise ValueError(f"Artifact with name '{artifact.name}' already exists")
            return a

    async def delete_artifact(self, artifact_id: ArtifactID) -> None:
        with self.session as session:
            session.execute(delete(ArtifactModel).where(ArtifactModel.id == artifact_id))
            session.commit()

    async def update_artifact(self, artifact_id: ArtifactID, artifact: Artifact) -> None:
        from evidently.ui.service.errors import ArtifactNotFound

        with self.session as session:
            existing = session.scalar(select(ArtifactModel).where(ArtifactModel.id == artifact_id))
            if existing is None:
                raise ArtifactNotFound()
            existing.name = artifact.name
            existing.updated_at = datetime.datetime.now()
            existing.description = artifact.metadata.description
            session.commit()

    async def list_artifact_versions(self, artifact_id: ArtifactID) -> List[ArtifactVersion]:
        with self.session as session:
            versions: Sequence[ArtifactVersionModel] = session.scalars(
                select(ArtifactVersionModel).where(ArtifactVersionModel.artifact_id == artifact_id)
            )
            return [v.to_artifact_version() for v in versions]

    async def get_artifact_version(self, artifact_version_id: ArtifactVersionID) -> Optional[ArtifactVersion]:
        with self.session as session:
            try:
                version_model: ArtifactVersionModel = session.get_one(ArtifactVersionModel, artifact_version_id)
            except NoResultFound:
                return None
            return version_model.to_artifact_version()

    async def get_artifact_version_by_version(
        self, artifact_id: ArtifactID, version: VersionOrLatest
    ) -> Optional[ArtifactVersion]:
        with self.session as session:
            version_value = version
            if isinstance(version, str):
                assert version == "latest"
                version_value = session.query(func.max(ArtifactVersionModel.version)).where(
                    ArtifactVersionModel.artifact_id == artifact_id
                )
            version_model: ArtifactVersionModel = session.scalar(
                select(ArtifactVersionModel).where(
                    ArtifactVersionModel.artifact_id == artifact_id, ArtifactVersionModel.version == version_value
                )
            )
            return version_model.to_artifact_version() if version_model is not None else None

    async def add_artifact_version(self, artifact_id: ArtifactID, artifact_version: ArtifactVersion) -> ArtifactVersion:
        with self.session as session:
            model = ArtifactVersionModel.from_artifact_version(artifact_version)
            model.artifact_id = artifact_id
            model.id = new_id()
            model.created_at = datetime.datetime.now()
            model.updated_at = datetime.datetime.now()
            session.add(model)
            version = model.to_artifact_version()
            try:
                session.commit()
            except IntegrityError:
                raise ValueError(f"Version {artifact_version.version} already exists for artifact {artifact_id}")
            return version

    async def delete_artifact_version(self, artifact_version_id: ArtifactVersionID) -> None:
        with self.session as session:
            session.execute(delete(ArtifactVersionModel).where(ArtifactVersionModel.id == artifact_version_id))
            session.commit()
