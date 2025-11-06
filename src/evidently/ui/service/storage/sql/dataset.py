import datetime
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence

from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update

from evidently.ui.service.datasets.metadata import DatasetMetadata
from evidently.ui.service.datasets.metadata import DatasetMetadataFull
from evidently.ui.service.datasets.metadata import DatasetMetadataStorage
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.datasets.metadata import DatasetTracingParams
from evidently.ui.service.storage.sql.base import BaseSQLStorage
from evidently.ui.service.storage.sql.models import DatasetSQLModel
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID


class SQLDatasetMetadataStorage(BaseSQLStorage, DatasetMetadataStorage):
    """SQL storage implementation for dataset metadata."""

    async def add_dataset_metadata(self, user_id: UserID, project_id: ProjectID, dataset: DatasetMetadata) -> DatasetID:
        """Add a new dataset metadata."""
        with self.session as session:
            model = DatasetSQLModel.from_dataset_metadata(dataset, user_id)
            session.add(model)
            session.commit()
            return model.id

    async def update_dataset_metadata(self, dataset_id: DatasetID, new_metadata: DatasetMetadata):
        """Update dataset metadata."""
        if dataset_id is None:
            return
        with self.session as session:
            now = datetime.datetime.now()

            param_dict = {
                "updated_at": now,
                "name": new_metadata.name,
                "description": new_metadata.description,
                "size_bytes": new_metadata.size_bytes,
                "row_count": new_metadata.row_count,
                "column_count": new_metadata.column_count,
                "data_definition": json.loads(new_metadata.data_definition.json()),
                "is_draft": new_metadata.is_draft,
                "draft_params": new_metadata.draft_params,
                "source": json.loads(new_metadata.source.json()),
                "metadata_json": new_metadata.metadata,
                "tags": new_metadata.tags,
            }
            params: Dict[str, Any] = {key: value for key, value in param_dict.items() if value is not None}

            session.execute(update(DatasetSQLModel).where(DatasetSQLModel.id == dataset_id).values(**params))

            session.commit()

    async def update_dataset_tracing_metadata(self, dataset_id: DatasetID, tracing_metadata: DatasetTracingParams):
        """Update tracing metadata for a dataset."""
        with self.session as session:
            session.execute(
                update(DatasetSQLModel)
                .where(DatasetSQLModel.id == dataset_id)
                .values(tracing_params=json.loads(tracing_metadata.json()))
            )
            session.commit()

    async def get_dataset_metadata(self, dataset_id: DatasetID) -> Optional[DatasetMetadataFull]:
        """Get dataset metadata by ID."""
        with self.session as session:
            from sqlalchemy.orm import selectinload

            query = (
                select(DatasetSQLModel)
                .options(
                    selectinload(DatasetSQLModel.project),
                    selectinload(DatasetSQLModel.author),
                )
                .where(DatasetSQLModel.id == dataset_id)
                .where(DatasetSQLModel.deleted.is_(None))
            )
            dataset: Optional[DatasetSQLModel] = session.scalar(query)
            if dataset is None:
                return None
            return dataset.to_dataset_metadata()

    async def list_datasets_metadata(
        self,
        project_id: ProjectID,
        limit: Optional[int],
        origin: Optional[List[DatasetOrigin]],
        draft: Optional[bool],
    ) -> List[DatasetMetadataFull]:
        """List datasets metadata."""
        with self.session as session:
            from sqlalchemy.orm import selectinload

            order_by_created_at = DatasetSQLModel.created_at.asc()
            query = (
                select(DatasetSQLModel)
                .options(
                    selectinload(DatasetSQLModel.project),
                    selectinload(DatasetSQLModel.author),
                )
                .where(DatasetSQLModel.project_id == project_id)
                .where(DatasetSQLModel.deleted.is_(None))
            )
            if draft is not None:
                query = query.where(DatasetSQLModel.is_draft == bool(draft))
            if origin is not None:
                query = query.where(DatasetSQLModel.origin.in_([st.value for st in origin]))
            query = query.order_by(order_by_created_at)
            if limit is not None:
                query = query.limit(limit)
            models: Sequence[DatasetSQLModel] = session.scalars(query).all()

            return [m.to_dataset_metadata() for m in models]

    async def mark_dataset_deleted(self, dataset_id: DatasetID):
        """Mark a dataset as deleted (soft delete)."""
        with self.session as session:
            session.execute(
                update(DatasetSQLModel)
                .where(DatasetSQLModel.id == dataset_id)
                .values(deleted=datetime.datetime.utcnow())
            )
            session.commit()

    async def delete_dataset_metadata(self, dataset_id: DatasetID):
        """Permanently delete dataset metadata."""
        with self.session as session:
            session.execute(delete(DatasetSQLModel).where(DatasetSQLModel.id == dataset_id))
            session.commit()

    async def datasets_count(self, project_id: ProjectID) -> int:
        """Count datasets in a project."""
        with self.session as session:
            result = session.execute(
                select(func.count(DatasetSQLModel.id))
                .where(DatasetSQLModel.project_id == project_id)
                .where(DatasetSQLModel.deleted.is_(None))
            ).scalar()
            return result or 0
