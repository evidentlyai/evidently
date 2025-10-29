import contextlib
import contextvars

from sqlalchemy import Engine
from sqlalchemy.orm import Session

_session_context_var: contextvars.ContextVar[Session] = contextvars.ContextVar("_session_context_var")


@contextlib.contextmanager
def session_context(engine: Engine):
    """Context manager for SQLAlchemy sessions with proper cleanup."""
    current_session = _session_context_var.get(None)
    if current_session is not None:
        yield current_session
        return
    session = Session(bind=engine)
    with session:
        token = _session_context_var.set(session)
        try:
            yield session
        finally:
            _session_context_var.reset(token)


class BaseSQLStorage:
    """Base class for SQL storage implementations."""

    def __init__(self, engine: Engine):
        self.engine = engine

    @property
    def session(self):
        """Get a session context manager."""
        return session_context(self.engine)
