from abc import ABC
from abc import abstractmethod

from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID


class SnapshotDatasetLinksManager(ABC):
    """Manager for linking datasets to snapshots."""

    @abstractmethod
    async def get_links(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotLinks:
        """Get dataset links for a snapshot.

        Args:
            project_id: The project ID
            snapshot_id: The snapshot ID
        """
        raise NotImplementedError

    @abstractmethod
    async def link_dataset_snapshot(
        self,
        project_id: ProjectID,
        snapshot_id: SnapshotID,
        dataset_id: DatasetID,
        dataset_type: str,
        dataset_subtype: str,
    ) -> None:
        """Link a dataset to a snapshot.

        Args:
            project_id: The project ID
            snapshot_id: The snapshot ID
            dataset_id: The dataset ID
            dataset_type: Type of dataset link (e.g., "input", "output")
            dataset_subtype: Subtype of dataset link (e.g., "current", "reference")
        """
        raise NotImplementedError
