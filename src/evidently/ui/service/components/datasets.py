from typing import Annotated
from typing import Dict
from typing import Optional

from litestar.di import Provide
from litestar.params import Dependency
from sqlalchemy import Engine

from evidently.ui.service.api.datasets import datasets_api
from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.components.security import SecurityComponent
from evidently.ui.service.managers.datasets import DatasetManager
from evidently.ui.service.storage.local.dataset import FSSpecDatasetFileStorage
from evidently.ui.service.storage.sql.dataset import SQLDatasetMetadataStorage


class DatasetComponent(Component):
    """Component for dataset management."""

    __service_name__ = "datasets"
    storage_type: Optional[str] = None
    path: str = "workspace"

    def get_api_route_handlers(self, ctx: ComponentContext):
        guard = ctx.get_component(SecurityComponent).get_auth_guard()
        return [datasets_api(guard)]

    def provider_dataset_metadata(self, ctx: ComponentContext):
        """Provider for dataset metadata storage."""

        storage_type = self.storage_type

        if storage_type == "file" or storage_type is None:
            from evidently.ui.service.datasets.metadata import FileDatasetMetadataStorage

            async def factory():
                return FileDatasetMetadataStorage(base_path=self.path)

            return factory
        elif storage_type == "sql":

            def factory(engine: Annotated[Engine, Dependency()]):
                return SQLDatasetMetadataStorage(engine)

            return factory
        raise ValueError(f"Unknown storage type {storage_type}")

    def provider_dataset_file_storage(self):
        """Provider for dataset file storage."""

        async def factory():
            return FSSpecDatasetFileStorage(base_path=self.path)

        return factory

    def provider_dataset_manager(self):
        """Provider for dataset manager."""

        async def factory(
            project_manager: Annotated[object, Dependency(skip_validation=True)],
            dataset_metadata: Annotated[object, Dependency(skip_validation=True)],
            dataset_file_storage: Annotated[object, Dependency(skip_validation=True)],
        ):
            return DatasetManager(
                project_manager=project_manager,
                dataset_metadata=dataset_metadata,
                dataset_file_storage=dataset_file_storage,
            )

        return factory

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        """Get dependencies for dataset components."""
        return {
            "dataset_metadata": Provide(self.provider_dataset_metadata(ctx)),
            "dataset_file_storage": Provide(self.provider_dataset_file_storage()),
            "dataset_manager": Provide(self.provider_dataset_manager()),
        }
