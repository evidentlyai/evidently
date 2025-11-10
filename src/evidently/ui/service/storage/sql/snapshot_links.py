from typing import Sequence

from sqlalchemy import Engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from evidently.legacy.suite.base_suite import DatasetInputOutputLinks
from evidently.legacy.suite.base_suite import DatasetLinks
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager
from evidently.ui.service.storage.sql.models import SnapshotDatasetsSQLModel
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID


def get_snapshot_links(session: Session, snapshot_id: SnapshotID) -> SnapshotLinks:
    """Get snapshot links from database."""
    input_output_links = DatasetInputOutputLinks(output=DatasetLinks(), input=DatasetLinks())
    links: Sequence[SnapshotDatasetsSQLModel] = session.scalars(
        select(SnapshotDatasetsSQLModel).where(SnapshotDatasetsSQLModel.snapshot_id == snapshot_id)
    ).all()
    for link in links:
        if link.dataset_type not in ("input", "output"):
            continue
        dataset_type: DatasetLinks = getattr(input_output_links, link.dataset_type)
        if link.dataset_subtype in ("current", "reference"):
            setattr(dataset_type, link.dataset_subtype, link.dataset_id)
        else:
            dataset_type.additional[link.dataset_subtype] = link.dataset_id
    return SnapshotLinks(datasets=input_output_links)


class SQLSnapshotDatasetLinksManager(SnapshotDatasetLinksManager):
    """SQL implementation of SnapshotDatasetLinksManager."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    async def get_links(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotLinks:
        """Get dataset links for a snapshot."""
        with Session(self.engine) as session:
            return get_snapshot_links(session, snapshot_id)

    async def link_dataset_snapshot(
        self,
        project_id: ProjectID,
        snapshot_id: SnapshotID,
        dataset_id: DatasetID,
        dataset_type: str,
        dataset_subtype: str,
    ) -> None:
        """Link a dataset to a snapshot."""
        with Session(self.engine) as session:
            model = SnapshotDatasetsSQLModel(
                snapshot_id=snapshot_id,
                dataset_id=dataset_id,
                dataset_type=dataset_type,
                dataset_subtype=dataset_subtype,
            )
            session.add(model)
            session.commit()
