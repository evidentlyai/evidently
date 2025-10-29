import datetime
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy import Engine
from sqlalchemy import insert

from evidently.core.metric_types import MetricResult
from evidently.core.serialization import SnapshotModel
from evidently.legacy.utils.numpy_encoder import numpy_dumps
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import SeriesFilter
from evidently.ui.service.base import SeriesResponse
from evidently.ui.service.storage.utils import iterate_metric_results_fields
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID

from .base import BaseSQLStorage
from .models import MetricsSQLModel
from .models import PointSQLModel

INSERT_CHUNK_SIZE = 1000


class SQLDataStorage(BaseSQLStorage, DataStorage):
    """SQL-based data storage implementation."""

    def __init__(self, engine: Engine):
        super().__init__(engine)

    @staticmethod
    def _extract_metric_results(snapshot: SnapshotModel) -> List[Tuple[MetricsSQLModel, MetricResult]]:
        """Extract metric results from snapshot."""
        result = []
        for metric_id, metric_result in snapshot.metric_results.items():
            # Create a simplified metric model for storage
            metric_model = MetricsSQLModel(
                metric_fingerprint=metric_id, metric_json=numpy_dumps({"metric_id": metric_id})
            )
            result.append((metric_model, metric_result))
        return result

    @staticmethod
    def _extract_metric_result_points(
        project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel, metric_results
    ) -> Iterator[List[dict]]:
        """Extract metric result points for storage."""
        points_chunk = []
        for metric_model, metric_result in metric_results:
            metric_fingerprint = metric_model.metric_fingerprint
            for field_path, value in iterate_metric_results_fields(metric_result):
                point = {
                    "project_id": project_id,
                    "snapshot_id": snapshot_id,
                    "metric_fingerprint": metric_fingerprint,
                    "timestamp": snapshot.timestamp,
                    "field_path": field_path,
                    "value": value,
                }
                points_chunk.append(point)
                if len(points_chunk) == INSERT_CHUNK_SIZE:
                    yield points_chunk
                    points_chunk.clear()
        if points_chunk:
            yield points_chunk

    async def add_snapshot_points(self, project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel):
        """Add snapshot data points to storage."""
        metric_results = self._extract_metric_results(snapshot)
        metrics = (metric for metric, _ in metric_results)

        with self.session as session:
            # Store metric definitions
            for metric in metrics:
                session.merge(metric)

            # Store data points
            for points_chunk in self._extract_metric_result_points(project_id, snapshot_id, snapshot, metric_results):
                if points_chunk:
                    session.execute(
                        insert(PointSQLModel),
                        points_chunk,
                    )

            session.commit()

    async def get_data_series(
        self,
        project_id: ProjectID,
        series_filter: List[SeriesFilter],
        start_time: Optional[datetime.datetime],
        end_time: Optional[datetime.datetime],
    ) -> SeriesResponse:
        """Get data series for time series analysis."""
        return SeriesResponse(sources=[], series=[])

    async def get_metrics(self, project_id: ProjectID, tags: List[str], metadata: Dict[str, str]) -> List[str]:
        """Get available metrics for a project."""
        return []

    async def get_metric_labels(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
    ) -> List[str]:
        """Get metric labels for a specific metric."""
        return []

    async def get_metric_label_values(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
        label: str,
    ) -> List[str]:
        """Get metric label values for a specific metric and label."""
        return []
