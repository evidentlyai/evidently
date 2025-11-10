import json
import posixpath

from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.suite.base_suite import DatasetInputOutputLinks
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.legacy.utils.numpy_encoder import numpy_dumps
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager
from evidently.ui.service.storage.fslocation import FSLocation
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID


def _get_links_path(project_id: ProjectID, snapshot_id: SnapshotID) -> str:
    """Get the path to the links file for a snapshot."""
    return posixpath.join(str(project_id), "snapshots", f"{snapshot_id}.links.json")


class FileSnapshotDatasetLinksManager(SnapshotDatasetLinksManager):
    """File-based implementation of SnapshotDatasetLinksManager."""

    def __init__(self, base_path: str):
        self.location = FSLocation(base_path=base_path)

    async def get_links(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotLinks:
        """Get dataset links for a snapshot."""
        links_path = _get_links_path(project_id, snapshot_id)

        if not self.location.exists(links_path):
            return SnapshotLinks(datasets=DatasetInputOutputLinks())

        with self.location.open(links_path, "r") as f:
            links_data = json.load(f)
            input_output_links = parse_obj_as(DatasetInputOutputLinks, links_data)

        return SnapshotLinks(datasets=input_output_links)

    async def link_dataset_snapshot(
        self,
        project_id: ProjectID,
        snapshot_id: SnapshotID,
        dataset_id: DatasetID,
        dataset_type: str,
        dataset_subtype: str,
    ) -> None:
        """Link a dataset to a snapshot."""
        links_path = _get_links_path(project_id, snapshot_id)

        # Create directory if it doesn't exist
        self.location.makedirs(posixpath.dirname(links_path))

        # Load existing links or create new
        if self.location.exists(links_path):
            with self.location.open(links_path, "r") as f:
                links_data = json.load(f)
                input_output_links = parse_obj_as(DatasetInputOutputLinks, links_data)
        else:
            input_output_links = DatasetInputOutputLinks()

        # Get the appropriate dataset links object
        dataset_links = getattr(input_output_links, dataset_type)

        # Set or update the link
        if dataset_subtype in ("current", "reference"):
            setattr(dataset_links, dataset_subtype, dataset_id)
        else:
            dataset_links.additional[dataset_subtype] = dataset_id

        # Save
        with self.location.open(links_path, "w") as f:
            f.write(numpy_dumps(input_output_links.dict(), indent=2))
