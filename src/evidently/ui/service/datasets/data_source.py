from abc import ABC
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type

import pandas as pd
from litestar import Response
from typing_extensions import TypeAlias

from evidently._pydantic_compat import BaseModel
from evidently.core.datasets import DataDefinition
from evidently.core.metric_types import AutoAliasMixin
from evidently.pydantic_utils import PolymorphicModel
from evidently.ui.service.datasets.filters import FilterBy
from evidently.ui.service.datasets.filters import filter_df
from evidently.ui.service.errors import EvidentlyServiceError
from evidently.ui.service.storage.local.dataset import DatasetFileStorage
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

if TYPE_CHECKING:
    from evidently.ui.service.managers.datasets import DatasetManager

MaterializedDataset: TypeAlias = pd.DataFrame


class SortBy(BaseModel):
    """Sorting configuration."""

    column: str
    ascending: bool = True


class DatasetReadError(EvidentlyServiceError):
    """Error reading dataset."""

    def to_response(self) -> Response:
        return Response(
            status_code=500,
            content={"detail": "dataset read error"},
        )


class DataSource(AutoAliasMixin, PolymorphicModel, ABC):
    """Base class for data sources."""

    __alias_namespace__: ClassVar = "evidently"
    __alias_type__: ClassVar = "data_source"

    class Config:
        is_base_type = True
        alias_required = True

    async def materialize(self, dataset_manager: "DatasetManager") -> MaterializedDataset:
        """Materialize the data source into a DataFrame."""
        raise NotImplementedError(self.__class__.__name__)

    async def materialize_with_data_definition(
        self, dataset_manager: "DatasetManager", data_definition: DataDefinition
    ) -> tuple[MaterializedDataset, DataDefinition]:
        """Materialize with data definition applied."""
        df = await self.materialize(dataset_manager)
        return self.apply_data_definition(df, data_definition), data_definition

    def apply_data_definition(self, df: MaterializedDataset, data_definition: DataDefinition) -> MaterializedDataset:
        """Apply data definition to dataframe."""
        return df

    def get_original_dataset_id(self) -> Optional[DatasetID]:
        """Get the original dataset ID if this is a dataset source."""
        raise NotImplementedError


class SortedFilteredDataSource(DataSource, ABC):
    """Data source with filtering and sorting support."""

    filter_by: Optional[List[FilterBy]] = None
    sort_by: Optional[SortBy] = None

    def post_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply filtering and sorting to the dataframe."""
        filtered_df = filter_df(df, self.filter_by)
        if self.sort_by:
            filtered_sorted_df = filtered_df.sort_values(by=self.sort_by.column, ascending=self.sort_by.ascending)
        else:
            filtered_sorted_df = filtered_df
        return filtered_sorted_df


class FileDataSource(SortedFilteredDataSource):
    """Data source that reads from a file."""

    project_id: ProjectID
    filename: str
    is_tmp: bool = False

    def read(self, storage: DatasetFileStorage) -> pd.DataFrame:
        """Read the file from storage."""
        try:
            from evidently.ui.service.datasets.file_io import FileIO

            df = FileIO(storage).read_file_from_storage(self.project_id, self.filename)
        except FileNotFoundError:
            raise DatasetReadError(f"No such file {self.filename}")
        return df

    async def materialize(self, dataset_manager: "DatasetManager") -> MaterializedDataset:
        """Materialize the file data source."""
        df = self.read(dataset_manager.dataset_file_storage)
        return self.post_process(df)


class DatasetDataSource(SortedFilteredDataSource):
    """Data source that reads from another dataset."""

    user_id: UserID
    dataset_id: DatasetID

    async def materialize(self, dataset_manager: "DatasetManager") -> MaterializedDataset:
        """Materialize the dataset data source."""
        dataset = await dataset_manager.get_dataset_metadata(self.user_id, self.dataset_id)
        if not dataset:
            raise DatasetReadError(f"Dataset {self.dataset_id} not found")
        df = await dataset.source.materialize(dataset_manager)
        return self.post_process(df)

    def get_original_dataset_id(self) -> Optional[DatasetID]:
        """Get the original dataset ID."""
        return self.dataset_id


class DataSourceDTO(AutoAliasMixin, PolymorphicModel, ABC):
    """DTO for data source serialization."""

    class Config:
        is_base_type = True

    __data_source_type__: ClassVar[Type[DataSource]]
    __alias_type__: ClassVar = "data_source_dto"

    def to_data_source(self, **kwargs) -> DataSource:
        """Convert DTO to data source."""
        kwargs = {k: v for k, v in kwargs.items() if k in self.__data_source_type__.__fields__}
        return self.__data_source_type__(**self.__dict__, **kwargs)

    @staticmethod
    def for_type(data_source_type: Type[DataSource], __module__: str) -> Type["DataSourceDTO"]:
        """Create a DTO type for a data source type."""
        exclude = ("project_id", "user_id")
        namespace = {
            "__annotations__": {n: f.outer_type_ for n, f in data_source_type.__fields__.items() if n not in exclude},
            **{n: f.default for n, f in data_source_type.__fields__.items() if n not in exclude and not f.required},
        }

        new_dto_type: Type[DataSourceDTO] = type(f"{data_source_type.__name__}DTO", (DataSourceDTO,), namespace)
        new_dto_type.__data_source_type__ = data_source_type
        new_dto_type.__module__ = __module__
        return new_dto_type


DatasetDataSourceDTO = DataSourceDTO.for_type(DatasetDataSource, __name__)
FileDataSourceDTO = DataSourceDTO.for_type(FileDataSource, __name__)
