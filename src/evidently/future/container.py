import abc
import itertools
from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Sequence
from typing import Union

from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.model.widget import BaseWidgetInfo

if TYPE_CHECKING:
    from evidently.future.report import Context

MetricOrContainer = Union[Metric, "MetricContainer"]


class MetricContainer(abc.ABC):
    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[Metric]:
        metrics = context.container_metrics(hash(self))
        if metrics is None:
            _metrics = self.generate_metrics(context)
            metrics = [
                m for m_or_c in _metrics for m in ((m_or_c,) if isinstance(m_or_c, Metric) else m_or_c.metrics(context))
            ]
            context.set_container_metrics(hash(self), metrics)
        return metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        metrics = context.container_metrics(hash(self))
        if metrics is None:
            raise ValueError("Container metrics missing in context")
        return list(itertools.chain(*[results[metric.to_calculation().id].widget for metric in metrics]))


class ColumnMetricContainer(MetricContainer, abc.ABC):
    def __init__(self, column: str):
        self._column = column
