import abc
import itertools
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
    _metrics: Optional[List[Metric]] = None

    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> List[MetricOrContainer]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[Metric]:
        if self._metrics is None:
            metrics = self.generate_metrics(context)
            self._metrics = [
                m for m_or_c in metrics for m in ((m_or_c,) if isinstance(m_or_c, Metric) else m_or_c.metrics(context))
            ]
        return self._metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        return list(itertools.chain(*[results[metric.to_calculation().id].widget for metric in self._metrics]))


class ColumnMetricContainer(MetricContainer, abc.ABC):
    def __init__(self, column: str):
        self._column = column
