import datetime
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy import Engine
from sqlalchemy import insert
from sqlalchemy import select

from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import ByLabelValue
from evidently.core.metric_types import CountValue
from evidently.core.metric_types import DataframeValue
from evidently.core.metric_types import MeanStdValue
from evidently.core.metric_types import MetricResult
from evidently.core.metric_types import SingleValue
from evidently.core.serialization import SnapshotModel
from evidently.legacy.utils.numpy_encoder import numpy_dumps
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import Series
from evidently.ui.service.base import SeriesFilter
from evidently.ui.service.base import SeriesResponse
from evidently.ui.service.base import SeriesSource
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID

from .base import BaseSQLStorage
from .models import MetricsSQLModel
from .models import PointSQLModel
from .models import SnapshotSQLModel

INSERT_CHUNK_SIZE = 1000


def _find_filter_index(
    filters: List[SeriesFilter],
    metric_type: str,
    params: Dict[str, str],
    snapshot_tags: List[str],
    snapshot_metadata: Dict[str, str],
) -> Optional[int]:
    """Find the index of a matching series filter."""
    for idx, series_filter in enumerate(filters):
        if (
            series_filter.metric in ("*", metric_type)
            and series_filter.metric_labels.items() <= params.items()
            and set(series_filter.tags) <= set(snapshot_tags)
            and series_filter.metadata.items() <= snapshot_metadata.items()
        ):
            return idx
    return None


def _collect_series(data, filters: Optional[List[SeriesFilter]]) -> SeriesResponse:
    """Collect data points into series format."""
    sources = []
    series = {}
    last_snapshot = None
    index = 0
    series_filters_map: Dict[tuple, int] = {}

    for metric_type, params, snapshot_id, timestamp, snapshot_tags, snapshot_metadata, value in data:
        snapshot_meta = SeriesSource(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            tags=snapshot_tags,
            metadata=snapshot_metadata,
        )
        if last_snapshot is None:
            last_snapshot = snapshot_id
            sources.append(snapshot_meta)
        if last_snapshot != snapshot_id:
            last_snapshot = snapshot_id
            sources.append(snapshot_meta)
            index += 1

        series_id = metric_type + ":" + ",".join([f"{k}={v}" for k, v in params.items()])

        key = (
            metric_type,
            frozenset(params.items()),
            frozenset(snapshot_tags),
            frozenset(snapshot_metadata.items()),
        )

        filter_index: int
        if filters is None:
            filter_index = 0
        else:
            stored_index = series_filters_map.get(key)
            if stored_index is not None:
                filter_index = stored_index
            else:
                found_index = _find_filter_index(filters, metric_type, params, snapshot_tags, snapshot_metadata)
                if found_index is None:
                    continue
                filter_index = found_index
                series_filters_map[key] = found_index

        try:
            value_float = float(value)
        except (ValueError, TypeError):
            continue

        if series_id not in series:
            series[series_id] = Series(
                metric_type=metric_type,
                filter_index=filter_index,
                params=params,
                values=([None] * index) + [value_float],
            )
        else:
            if len(series[series_id].values) < index:
                series[series_id].values.extend([None] * (index - len(series[series_id].values)))
            series[series_id].values.append(value_float)

    return SeriesResponse(
        sources=sources,
        series=list(series.values()),
    )


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

    def _extract_params(self, result: MetricResult) -> Dict[str, str]:
        """Extract params from metric result."""
        params: Dict[str, str] = {}
        if result.metric_value_location is None:
            return params
        for k, v in result.metric_value_location.param.items():
            if k in params:
                raise ValueError("duplicated key?")
            params[k] = str(v)
        for k, v in result.metric_value_location.metric.params.items():
            if k in ["type", "tests", "count_tests", "share_tests", "mean_tests", "std_tests"]:
                continue
            params[k] = str(v)
        return params

    def _extract_metric_type(self, result: MetricResult) -> str:
        """Extract metric type from metric result."""
        if result.metric_value_location is None:
            return ""
        return result.metric_value_location.metric.params.get("type", "")

    def _extract_metric_result_points(
        self, project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel, metric_results
    ) -> Iterator[List[dict]]:
        """Extract metric result points for storage."""
        points_chunk: List[dict] = []

        for metric_model, metric_result in metric_results:
            if isinstance(metric_result, SingleValue):
                self._add_point_to_chunk(points_chunk, project_id, snapshot_id, metric_result)
            elif isinstance(metric_result, ByLabelValue):
                for value in metric_result.values.values():
                    self._add_point_to_chunk(points_chunk, project_id, snapshot_id, value)
            elif isinstance(metric_result, CountValue):
                self._add_point_to_chunk(points_chunk, project_id, snapshot_id, metric_result.count)
                self._add_point_to_chunk(points_chunk, project_id, snapshot_id, metric_result.share)
            elif isinstance(metric_result, MeanStdValue):
                self._add_point_to_chunk(points_chunk, project_id, snapshot_id, metric_result.mean)
                self._add_point_to_chunk(points_chunk, project_id, snapshot_id, metric_result.std)
            elif isinstance(metric_result, ByLabelCountValue):
                for value in metric_result.counts.values():
                    self._add_point_to_chunk(points_chunk, project_id, snapshot_id, value)
                for value in metric_result.shares.values():
                    self._add_point_to_chunk(points_chunk, project_id, snapshot_id, value)
            elif isinstance(metric_result, DataframeValue):
                for value in metric_result.iter_single_values():
                    self._add_point_to_chunk(points_chunk, project_id, snapshot_id, value)
            else:
                raise ValueError(f"type {type(metric_result)} isn't supported")

            if len(points_chunk) >= INSERT_CHUNK_SIZE:
                yield points_chunk
                points_chunk.clear()

        if points_chunk:
            yield points_chunk

    def _add_point_to_chunk(
        self, points_chunk: List[dict], project_id: ProjectID, snapshot_id: SnapshotID, result: SingleValue
    ):
        """Add a single value result as a point to the chunk."""
        if result.metric_value_location is None:
            raise ValueError("metric_value_location should be set")

        params = self._extract_params(result)
        metric_type = self._extract_metric_type(result)

        point = {
            "project_id": project_id,
            "snapshot_id": snapshot_id,
            "metric_type": metric_type,
            "params": params,
            "value": result.value,
        }
        points_chunk.append(point)

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

    async def get_metrics(self, project_id: ProjectID, tags: List[str], metadata: Dict[str, str]) -> List[str]:
        """Get available metrics for a project."""
        with self.session as session:
            # Query snapshots matching tags and metadata
            snapshot_query = select(SnapshotSQLModel.id).where(SnapshotSQLModel.project_id == project_id)

            # Filter by tags (all tags must be present)
            for tag in tags:
                snapshot_query = snapshot_query.where(SnapshotSQLModel.tags.contains([tag]))

            # Filter by metadata (all metadata items must match)
            for key, value in metadata.items():
                snapshot_query = snapshot_query.where(SnapshotSQLModel.metadata_json[key].as_string() == value)

            # Get snapshot IDs that match
            matching_snapshot_ids = [row[0] for row in session.execute(snapshot_query)]

            if not matching_snapshot_ids:
                return []

            # Query distinct metric types from points for these snapshots
            metrics_query = (
                select(PointSQLModel.metric_type)
                .where(PointSQLModel.project_id == project_id, PointSQLModel.snapshot_id.in_(matching_snapshot_ids))
                .distinct()
            )

            metrics = [row[0] for row in session.execute(metrics_query) if row[0]]
            return list(set(metrics))

    async def get_metric_labels(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
    ) -> List[str]:
        """Get metric labels for a specific metric."""
        with self.session as session:
            # Query snapshots matching tags and metadata
            snapshot_query = select(SnapshotSQLModel.id).where(SnapshotSQLModel.project_id == project_id)

            for tag in tags:
                snapshot_query = snapshot_query.where(SnapshotSQLModel.tags.contains([tag]))

            for key, value in metadata.items():
                snapshot_query = snapshot_query.where(SnapshotSQLModel.metadata_json[key].as_string() == value)

            matching_snapshot_ids = [row[0] for row in session.execute(snapshot_query)]

            if not matching_snapshot_ids:
                return []

            # Query params from points for the specified metric type
            points_query = (
                select(PointSQLModel.params)
                .where(
                    PointSQLModel.project_id == project_id,
                    PointSQLModel.snapshot_id.in_(matching_snapshot_ids),
                    PointSQLModel.metric_type == metric,
                )
                .distinct()
            )

            labels = set()
            for (params_dict,) in session.execute(points_query):
                if params_dict:
                    for key in params_dict.keys():
                        if key != "type":
                            labels.add(key)

            return list(labels)

    async def get_metric_label_values(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
        label: str,
    ) -> List[str]:
        """Get metric label values for a specific metric and label."""
        with self.session as session:
            # Query snapshots matching tags and metadata
            snapshot_query = select(SnapshotSQLModel.id).where(SnapshotSQLModel.project_id == project_id)

            for tag in tags:
                snapshot_query = snapshot_query.where(SnapshotSQLModel.tags.contains([tag]))

            for key, value in metadata.items():
                snapshot_query = snapshot_query.where(SnapshotSQLModel.metadata_json[key].as_string() == value)

            matching_snapshot_ids = [row[0] for row in session.execute(snapshot_query)]

            if not matching_snapshot_ids:
                return []

            # Query params from points for the specified metric type
            points_query = select(PointSQLModel.params).where(
                PointSQLModel.project_id == project_id,
                PointSQLModel.snapshot_id.in_(matching_snapshot_ids),
                PointSQLModel.metric_type == metric,
            )

            values = set()
            for (params_dict,) in session.execute(points_query):
                if params_dict and label in params_dict:
                    value = params_dict[label]
                    if value and value != "None":
                        values.add(str(value))

            return list(values)

    async def get_data_series(
        self,
        project_id: ProjectID,
        series_filter: List[SeriesFilter],
        start_time: Optional[datetime.datetime],
        end_time: Optional[datetime.datetime],
    ) -> SeriesResponse:
        """Get data series for time series analysis."""
        with self.session as session:
            # Build query joining points with snapshots
            expr = select(
                PointSQLModel.metric_type,
                PointSQLModel.params,
                SnapshotSQLModel.id,
                SnapshotSQLModel.timestamp,
                SnapshotSQLModel.tags,
                SnapshotSQLModel.metadata_json,
                PointSQLModel.value,
            ).join(SnapshotSQLModel, PointSQLModel.snapshot_id == SnapshotSQLModel.id)

            if start_time is not None:
                expr = expr.where(SnapshotSQLModel.timestamp >= start_time)
            if end_time is not None:
                expr = expr.where(SnapshotSQLModel.timestamp <= end_time)

            expr = expr.where(PointSQLModel.project_id == project_id)

            # Order by timestamp and snapshot_id
            expr = expr.order_by(SnapshotSQLModel.timestamp.asc(), SnapshotSQLModel.id.asc())

            # Execute query and filter in Python
            data_results = []
            for metric_type, params, snapshot_id, timestamp, tags, metadata, value in session.execute(expr):
                if not params:
                    params = {}

                # Apply series filter matching
                matched = False
                for filter_item in series_filter:
                    if filter_item.metric not in ("*", metric_type):
                        continue
                    if params.items() < filter_item.metric_labels.items():
                        continue
                    if not (set(tags) >= set(filter_item.tags)):
                        continue
                    if not (dict(metadata).items() >= filter_item.metadata.items()):
                        continue
                    matched = True
                    break

                if not matched:
                    continue

                data_results.append(
                    (
                        metric_type,
                        params,
                        snapshot_id,
                        timestamp,
                        tags,
                        dict(metadata),
                        value,
                    )
                )

            return _collect_series(data_results, series_filter)
