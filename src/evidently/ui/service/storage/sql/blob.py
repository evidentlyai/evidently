import contextlib
import io
import json
from typing import IO
from typing import Iterator
from typing import Union

from sqlalchemy import Engine
from sqlalchemy import select

from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.utils import NumpyEncoder
from evidently.ui.service.base import BlobStorage
from evidently.ui.service.type_aliases import BlobID
from evidently.ui.service.type_aliases import ProjectID

from .base import BaseSQLStorage
from .models import BlobSQLModel


class SQLBlobStorage(BaseSQLStorage, BlobStorage):
    """SQL-based blob storage implementation."""

    def __init__(self, engine: Engine):
        super().__init__(engine)

    def get_snapshot_blob_id(self, project_id: ProjectID, snapshot: Snapshot) -> BlobID:
        """Generate blob ID for snapshot."""
        return f"{project_id}/{snapshot.id}.json"

    @contextlib.contextmanager
    def open_blob(self, blob_id: BlobID) -> Iterator[IO]:
        """Open blob for reading."""
        with self.session as session:
            blob_model = session.scalar(select(BlobSQLModel).where(BlobSQLModel.id == blob_id))
            if blob_model is None:
                raise FileNotFoundError(f"Blob {blob_id} not found")
            yield io.BytesIO(blob_model.data)

    async def put_blob(self, blob_id: BlobID, obj: Union[str, bytes]) -> BlobID:
        """Store blob data."""
        with self.session as session:
            # Convert string to bytes for storage
            if isinstance(obj, str):
                data = obj.encode("utf-8")
            else:
                data = obj
            size = len(data)

            blob_model = BlobSQLModel(id=blob_id, data=data, size=size)
            session.merge(blob_model)
            session.commit()
        return blob_id

    async def get_blob_metadata(self, blob_id: BlobID):
        """Get blob metadata."""
        with self.session as session:
            blob_model = session.scalar(select(BlobSQLModel).where(BlobSQLModel.id == blob_id))
            if blob_model is None:
                raise FileNotFoundError(f"Blob {blob_id} not found")
            return blob_model.to_blob_metadata()

    def blob_exists(self, blob_id: BlobID) -> bool:
        """Check if blob exists."""
        with self.session as session:
            blob_model = session.scalar(select(BlobSQLModel).where(BlobSQLModel.id == blob_id))
            return blob_model is not None

    async def delete_blob(self, blob_id: BlobID):
        """Delete blob."""
        with self.session as session:
            blob_model = session.scalar(select(BlobSQLModel).where(BlobSQLModel.id == blob_id))
            if blob_model is not None:
                session.delete(blob_model)
                session.commit()

    async def put_snapshot(self, project_id: ProjectID, snapshot: Snapshot):
        """Store snapshot as blob."""
        blob_id = self.get_snapshot_blob_id(project_id, snapshot)
        await self.put_blob(blob_id, json.dumps(snapshot.dict(), cls=NumpyEncoder))
        return await self.get_blob_metadata(blob_id)
