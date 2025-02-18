import abc
import typing
from typing import Dict
from typing import List
from typing import Optional

from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.model.widget import BaseWidgetInfo

if typing.TYPE_CHECKING:
    from evidently.future.report import Context

MetricOrContainer = typing.Union[Metric, "MetricContainer"]


class MetricContainer(abc.ABC):
    _metrics: Optional[List[MetricOrContainer]] = None

    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> List[MetricOrContainer]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[MetricOrContainer]:
        if self._metrics is None:
            self._metrics = self.generate_metrics(context)
        return self._metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        result: List[BaseWidgetInfo] = []
        for metric in self._metrics:
            if isinstance(metric, Metric):
                result.extend(results[metric.to_calculation().id].widget)
            else:
                result.extend(metric.render(context, results))
        return result


class ColumnMetricContainer(MetricContainer, abc.ABC):
    def __init__(self, column: str):
        self._column = column
