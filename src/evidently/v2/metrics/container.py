import abc
import itertools
from typing import Dict
from typing import List
from typing import Optional

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics import Metric
from evidently.v2.metrics import MetricResult
from evidently.v2.metrics.base import MetricId
from evidently.v2.report import Context


class MetricContainer:
    _metrics: Optional[List[Metric]] = None

    @abc.abstractmethod
    def generate_metrics(self, context: Context) -> List[Metric]:
        raise NotImplementedError()

    def metrics(self, context: Context) -> List[Metric]:
        self._metrics = self.metrics(context)
        return self._metrics

    def render(self, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        return list(itertools.chain(*[results[metric.id].widget for metric in self._metrics]))
