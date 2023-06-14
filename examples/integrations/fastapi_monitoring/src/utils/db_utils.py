from typing import Callable

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker


def open_sqa_session(engine: sqlalchemy.Engine) -> sqlalchemy.orm.Session:
    """Open SQLAlchemy session.

    Args:
        engine (sqlalchemy.engine): SQLAlchemy engine.

    Returns:
        sqlalchemy.orm.Session: class Session.
    """

    Session: Callable = sessionmaker(bind=engine)
    session: sqlalchemy.orm.Session = Session()
    return session
