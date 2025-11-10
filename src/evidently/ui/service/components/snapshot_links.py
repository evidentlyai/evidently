from typing import Callable
from typing import ClassVar

from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import FactoryComponent
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager


class SnapshotDatasetLinksComponent(FactoryComponent[SnapshotDatasetLinksManager], Component):
    """Component for snapshot dataset links manager."""

    class Config:
        is_base_type = True

    __section__: ClassVar[str] = "snapshot_dataset_links"
    dependency_name: ClassVar[str] = "snapshot_dataset_links"
    use_cache: ClassVar[bool] = True

    def dependency_factory(self) -> Callable[..., SnapshotDatasetLinksManager]:
        raise NotImplementedError(self.__class__)
