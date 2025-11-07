import datetime
from math import ceil
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from litestar.datastructures import UploadFile

from evidently.core.datasets import DataDefinition
from evidently.legacy.core import new_id
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.ui.managers.base import BaseManager
from evidently.legacy.ui.managers.projects import ProjectManager
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import UserID
from evidently.ui.service.datasets.data_source import DatasetDataSource
from evidently.ui.service.datasets.data_source import FileDataSource
from evidently.ui.service.datasets.data_source import SortBy
from evidently.ui.service.datasets.file_io import FileIO
from evidently.ui.service.datasets.file_io import get_upload_file
from evidently.ui.service.datasets.filters import FilterBy
from evidently.ui.service.datasets.metadata import DatasetMetadata
from evidently.ui.service.datasets.metadata import DatasetMetadataFull
from evidently.ui.service.datasets.metadata import DatasetMetadataStorage
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.datasets.models import ColumnDataType
from evidently.ui.service.datasets.models import DatasetColumn
from evidently.ui.service.datasets.models import DatasetPagination
from evidently.ui.service.datasets.models import Metadata
from evidently.ui.service.storage.local.dataset import DatasetFileStorage
from evidently.ui.service.type_aliases import DatasetID

DEFAULT_INDEX_COLUMN = "_evidently_index"
LEGACY_INDEX_COLUMN = "index"

INDEX_COLUMNS = [DEFAULT_INDEX_COLUMN, LEGACY_INDEX_COLUMN]


class DatasetManager(BaseManager):
    """Manager for dataset operations."""

    project_manager: ProjectManager
    dataset_metadata: DatasetMetadataStorage
    dataset_file_storage: DatasetFileStorage

    async def upload_dataset(
        self,
        user_id: UserID,
        project_id: ProjectID,
        name: str,
        description: Optional[str],
        data: Union[UploadFile, pd.DataFrame],
        data_definition: DataDefinition,
        origin: DatasetOrigin,
        metadata: dict[str, MetadataValueType],
        tags: List[str],
        is_draft: bool = False,
        draft_params: Optional[dict] = None,
    ) -> DatasetMetadata:
        """Upload a dataset."""
        project_model = await self.project_manager.get_project(user_id, project_id)
        if project_model is None:
            raise ValueError(f"Project {project_id} not found")

        file_data = data if isinstance(data, UploadFile) else get_upload_file(data, name)
        io = FileIO(self.dataset_file_storage)
        dataset_id = new_id()
        blob_data = io.save_dataframe_and_calculate_data_definition(
            user_id, project_id, dataset_id, file_data, data_definition
        )

        dataset = DatasetMetadata(
            id=dataset_id,
            project_id=project_id,
            author_id=user_id,
            name=name,
            source=FileDataSource(project_id=project_id, filename=blob_data.filename),
            data_definition=blob_data.data_definition,
            description=description or "",
            size_bytes=blob_data.size_bytes,
            row_count=blob_data.row_count,
            column_count=blob_data.column_count,
            all_columns=blob_data.columns,
            is_draft=is_draft,
            draft_params=draft_params,
            origin=origin,
            metadata=metadata,
            tags=tags,
        )

        try:
            dataset_id = await self.dataset_metadata.add_dataset_metadata(user_id, project_id, dataset)
        except Exception as e:
            self.dataset_file_storage.remove_dataset(blob_data.filename)
            raise e

        return dataset

    async def update_dataset(
        self,
        user_id: UserID,
        dataset_id: DatasetID,
        name: Optional[str],
        description: Optional[str],
        data_definition: Optional[DataDefinition],
        metadata: Optional[dict[str, MetadataValueType]],
        tags: Optional[List[str]],
    ) -> None:
        """Update a dataset."""
        dataset = await self.dataset_metadata.get_dataset_metadata(dataset_id)
        if dataset is None:
            raise ValueError(f"Dataset {dataset_id} not found")

        if name is not None:
            dataset.name = name
        if description is not None:
            dataset.description = description
        if data_definition is not None:
            dataset.data_definition = data_definition
        if metadata is not None:
            dataset.metadata = metadata
        if tags is not None:
            dataset.tags = tags

        await self.dataset_metadata.update_dataset_metadata(dataset_id=dataset_id, new_metadata=dataset)

    async def delete_dataset(self, user_id: UserID, dataset_id: DatasetID) -> None:
        """Delete a dataset."""
        dataset = await self.dataset_metadata.get_dataset_metadata(dataset_id)
        if dataset is None:
            raise ValueError(f"Dataset {dataset_id} not found")
        await self.dataset_metadata.mark_dataset_deleted(dataset.id)

    async def get_dataset_metadata(self, user_id: UserID, dataset_id: DatasetID) -> DatasetMetadata:
        """Get dataset metadata."""
        dataset = await self.dataset_metadata.get_dataset_metadata(dataset_id)
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")
        return dataset

    async def get_dataset(
        self,
        user_id: UserID,
        dataset_id: DatasetID,
        sort_by: Optional[SortBy] = None,
        filter_queries: Optional[List[FilterBy]] = None,
    ) -> Tuple[pd.DataFrame, DatasetMetadata]:
        """Get a dataset as a dataframe."""
        dataset = await self.get_dataset_metadata(user_id, dataset_id)
        if dataset is None:
            raise ValueError(f"Dataset {dataset_id} not found")
        source = DatasetDataSource(filter_by=filter_queries, sort_by=sort_by, user_id=user_id, dataset_id=dataset_id)
        df = await source.materialize(self)
        return df, dataset

    @staticmethod
    def _get_dataset_column_type(df: pd.DataFrame, column_name: str) -> ColumnDataType:
        """Get the type of a dataset column."""
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return ColumnDataType.Numerical
        if pd.api.types.is_datetime64_any_dtype(df[column_name]):
            return ColumnDataType.Datetime
        return ColumnDataType.String

    async def get_dataset_pagination(
        self,
        user_id: UserID,
        dataset_id: DatasetID,
        page_size: Optional[int] = 10,
        current_page: Optional[int] = 1,
        sort_by: Optional[SortBy] = None,
        filter_queries: Optional[List[FilterBy]] = None,
    ) -> DatasetPagination:
        """Get paginated dataset data."""
        df, dataset_metadata = await self.get_dataset(user_id, dataset_id, sort_by, filter_queries)
        total_row_count = df.shape[0]
        df = paginate_df(df, page_size, current_page)

        data_records: list[list] = [
            [item if isinstance(item, (int, float, bool, str, datetime.datetime)) else str(item) for item in x]
            for x in df.values.tolist()
        ]
        columns = [
            DatasetColumn(
                name=column_name,
                type=self._get_dataset_column_type(df, column_name),
                is_index=(column_name in INDEX_COLUMNS),
            )
            for column_name in df.columns
        ]
        result = DatasetPagination(
            page_size=page_size or 10,
            total_pages=ceil(total_row_count / (page_size or 10)),
            current_page=current_page or 1,
            items=data_records,
            metadata=Metadata(
                name=dataset_metadata.name,
                description=dataset_metadata.description or "",
                row_count=total_row_count,
                data_definition=dataset_metadata.data_definition,
                columns=columns,
            ),
        )
        return result

    async def list_datasets(
        self,
        user_id: UserID,
        project_id: ProjectID,
        limit: Optional[int],
        origin: Optional[List[DatasetOrigin]],
        draft: Optional[bool],
    ) -> List[DatasetMetadataFull]:
        """List datasets in a project."""
        return await self.dataset_metadata.list_datasets_metadata(project_id, limit, origin, draft)

    async def datasets_count(self, user_id: UserID, project_id: ProjectID) -> int:
        """Count datasets in a project."""
        return await self.dataset_metadata.datasets_count(project_id)


def paginate_df(
    df: pd.DataFrame,
    page_size: Optional[int],
    current_page: Optional[int],
) -> pd.DataFrame:
    """Paginate a dataframe."""
    if page_size is None or current_page is None:
        return df
    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size
    return df.iloc[start_index:end_index]
