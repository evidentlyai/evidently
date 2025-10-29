from typing import Optional

from sqlalchemy.orm import Session

from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

from .models import ProjectSQLModel
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
