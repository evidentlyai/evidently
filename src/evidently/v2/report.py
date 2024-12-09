from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

from ..base_metric import InputData
from .datasets import Dataset
from .datasets import DatasetColumn
from .metrics.base import Metric
from .metrics.base import MetricId
from .metrics.base import MetricResult

TResultType = TypeVar("TResultType", bound="MetricResult")


class ContextColumnData:
    _column: DatasetColumn
    _labels: Optional[List[object]]

    def __init__(self, column: DatasetColumn):
        self._column = column
        self._labels = None

    def labels(self):
        if self._labels is None:
            self._labels = list(self._column.data.unique())
        return self._labels


class Context:
    _configuration: Optional["Report"]
    _metrics: Dict[MetricId, MetricResult]
    _data_columns: Dict[str, ContextColumnData]

    def __init__(self):
        self._metrics = {}
        self._configuration = None
        self._data_columns = {}

    def init_dataset(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self._data_columns = {
            column_name: ContextColumnData(current_data.column(column_name))
            for column_name, info in current_data._data_definition._columns.items()
        }

    def get_metric_result(self, metric: Metric[TResultType]) -> TResultType:
        raise NotImplementedError()

    def column(self, column_name: str) -> ContextColumnData:
        return self._data_columns[column_name]


class Snapshot:
    _context: Context  # stores report calculation progress

    def __init__(self):
        self._context = Context()

    def run(self, data):
        raise NotImplementedError()


class Report:
    def __init__(self, metrics: List[Metric]):
        pass

    def run(self, data: "InputData") -> Snapshot:
        snapshot = Snapshot()
        snapshot.report = self
        snapshot.run(data)
        return snapshot
