from typing import Callable

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker
from src.utils.models import Base


def open_sqa_session(engine: sqlalchemy.engine) -> sqlalchemy.orm.Session:
    """Open SQLAlchemy session.

    Args:
        engine (sqlalchemy.engine): SQLAlchemy engine.

    Returns:
        sqlalchemy.orm.Session: class Session.
    """

    Session: Callable = sessionmaker(bind=engine)
    session: sqlalchemy.orm.Session = Session()
    return session


def add_or_update_by_ts(session: sqlalchemy.orm.Session, record: Base) -> None:
    """Add or update record by timestamp.

    Args:
        session (sqlalchemy.orm.Session): SQLAlchemy session object.
        record (Base): New record.
    """

    # Search record with the same timestamp
    query = session.query(type(record)).filter_by(timestamp=record.timestamp)

    # If such record found
    if query.count() > 0:
        # update record (row) by the new values
        query.update(
            {
                column: getattr(record, column)
                for column in record.__table__.columns.keys()
                if column != "id"
            }
        )
    else:
        # If not found then add new record (row)
        session.add(record)
