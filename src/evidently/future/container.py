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


class MetricContainer:
    _metrics: Optional[List[Metric]] = None

    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> List[Metric]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[Metric]:
        if self._metrics is None:
            self._metrics = self.generate_metrics(context)
        return self._metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        return list(itertools.chain(*[results[metric.to_calculation().id].widget for metric in self._metrics]))
