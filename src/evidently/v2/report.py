from typing import Dict
from typing import List
from typing import TypeVar

from ..base_metric import InputData
from .metrics.base import Metric
from .metrics.base import MetricId
from .metrics.base import MetricResult

TResultType = TypeVar("TResultType", bound="MetricResult")


class Context:
    _configuration: "Report"
    _metrics: Dict[MetricId, MetricResult]

    def get_metric_result(self, metric: Metric[TResultType]) -> TResultType:
        raise NotImplementedError()


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
