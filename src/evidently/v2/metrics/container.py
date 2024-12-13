import abc
import itertools
import typing
from typing import Dict
from typing import List
from typing import Optional

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics import Metric
from evidently.v2.metrics import MetricResult
from evidently.v2.metrics.base import MetricId

if typing.TYPE_CHECKING:
    from evidently.v2.report import Context


class MetricContainer:
    _metrics: Optional[List[Metric]] = None

    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> List[Metric]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[Metric]:
        if self._metrics is None:
            self._metrics = self.generate_metrics(context)
        return self._metrics

    def render(self, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        return list(itertools.chain(*[results[metric.id].widget for metric in self._metrics]))
