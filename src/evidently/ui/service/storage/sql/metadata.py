from typing import List
from typing import Optional
from typing import Sequence
from typing import Set

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from evidently.core.serialization import SnapshotModel
from evidently.legacy.ui.dashboards import DashboardConfig
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import BlobMetadata
from evidently.ui.service.base import Project
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.base import User
from evidently.ui.service.errors import SnapshotNotFound
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID
from evidently.ui.service.type_aliases import UserID

from .base import BaseSQLStorage
from .models import ProjectSQLModel
from .models import SnapshotSQLModel
from .models import UserSQLModel


def get_or_create_user(session: Session, user_id: UserID) -> UserSQLModel:
    """Get or create a user in the database."""
    user_model = session.query(UserSQLModel).filter(UserSQLModel.id == user_id).first()
    if user_model is None:
        user_model = UserSQLModel(id=user_id, name="Unknown User")
        session.add(user_model)
        session.flush()
    return user_model


def get_project(session: Session, project_id: ProjectID) -> Optional[ProjectSQLModel]:
    """Get a project by ID."""
    return session.query(ProjectSQLModel).filter(ProjectSQLModel.id == project_id).first()


class SQLProjectMetadataStorage(BaseSQLStorage, ProjectMetadataStorage):
    """SQL-based project metadata storage implementation."""

    async def add_project(self, project: Project, user: User, org_id: Optional[OrgID] = None) -> Project:
        """Add a new project to storage."""
        with self.session as session:
            user_model = get_or_create_user(session, user.id)
            model = ProjectSQLModel(
                id=project.id,
                name=project.name,
                description=project.description,
                dashboard_json=DashboardConfig(name="", tabs=[], panels=[]).dict(),
                date_from=project.date_from,
                date_to=project.date_to,
                author=user_model,
                created_at=project.created_at,
            )
            session.add(model)
            session.commit()
            return project

    async def update_project(self, project: Project) -> Project:
        """Update an existing project."""
        with self.session as session:
            session.execute(
                update(ProjectSQLModel)
                .where(ProjectSQLModel.id == project.id)
                .values(
                    name=project.name,
                    description=project.description,
                    date_from=project.date_from,
                    date_to=project.date_to,
                )
            )
            session.commit()
        return project

    async def get_project(self, project_id: ProjectID) -> Optional[Project]:
        """Get a project by ID."""
        with self.session as session:
            model: Optional[ProjectSQLModel] = get_project(session, project_id)
            if model is None:
                return None
            return model.to_project()

    async def delete_project(self, project_id: ProjectID):
        """Delete a project and all its data."""
        with self.session as session:
            session.execute(delete(ProjectSQLModel).where(ProjectSQLModel.id == project_id))
            session.commit()

    async def list_projects(self, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        """List projects, optionally filtered by IDs."""
        with self.session as session:
            stmt = select(ProjectSQLModel).where(ProjectSQLModel.version == "1")
            if project_ids is not None:
                stmt = stmt.where(ProjectSQLModel.id.in_(project_ids))
            stmt = stmt.order_by(ProjectSQLModel.created_at.desc())
            return [p.to_project() for p in session.scalars(stmt)]

    async def add_snapshot(self, project_id: ProjectID, snapshot: SnapshotModel) -> SnapshotID:
        """Add a new snapshot to a project."""
        with self.session as session:
            # Generate a new snapshot ID
            import uuid6

            snapshot_id = uuid6.uuid7()

            # Create blob metadata
            blob = BlobMetadata(id=f"{project_id}/{snapshot_id}.json", size=0)

            model = SnapshotSQLModel.from_snapshot(snapshot, project_id=project_id, blob=blob)
            model.id = snapshot_id  # Set the generated ID
            session.add(model)
            session.commit()
            return snapshot_id

    async def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        """Delete a snapshot from a project."""
        with self.session as session:
            session.execute(
                delete(SnapshotSQLModel).where(
                    SnapshotSQLModel.project_id == project_id,
                    SnapshotSQLModel.id == snapshot_id,
                )
            )
            session.commit()

    async def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        """Search for projects by name."""
        with self.session as session:
            stmt = select(ProjectSQLModel).where(ProjectSQLModel.name == project_name)
            if project_ids is not None:
                stmt = stmt.where(ProjectSQLModel.id.in_(project_ids))
            return [p.to_project() for p in session.scalars(stmt)]

    async def list_snapshots(
        self,
        project_id: ProjectID,
        include_reports: bool = True,
        include_test_suites: bool = True,
    ) -> List[SnapshotMetadataModel]:
        """List snapshots for a project."""
        with self.session as session:
            project = await self.get_project(project_id)
            models: Sequence[SnapshotSQLModel] = session.scalars(
                select(SnapshotSQLModel).where(SnapshotSQLModel.project_id == project_id)
            )

            return [m.to_snapshot_metadata(project) for m in models]

    async def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadataModel:
        """Get metadata for a specific snapshot."""
        project = await self.get_project(project_id)
        with self.session as session:
            model: Optional[SnapshotSQLModel] = session.scalar(
                select(SnapshotSQLModel).where(
                    SnapshotSQLModel.project_id == project_id,
                    SnapshotSQLModel.id == snapshot_id,
                )
            )
            if model is None:
                raise SnapshotNotFound()
            return model.to_snapshot_metadata(project)

    async def reload_snapshots(self, project_id: ProjectID):
        """Reload snapshots for a project (no-op for SQL storage)."""
        pass
