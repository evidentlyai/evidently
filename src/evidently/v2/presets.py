import abc
import dataclasses
from typing import Dict
from typing import List

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics import Metric
from evidently.v2.metrics import MetricResult
from evidently.v2.metrics.base import MetricId
from evidently.v2.metrics.base import render_widgets
from evidently.v2.report import Context


@dataclasses.dataclass
class PresetResult:
    widget: List[BaseWidgetInfo]

    def _repr_html_(self):
        return render_widgets(self.widget)


class MetricPreset:
    def call(self, context: Context) -> PresetResult:
        return self.calculate({metric.id: context.calculate_metric(metric) for metric in self.metrics()})

    @abc.abstractmethod
    def metrics(self) -> List[Metric]:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(self, metric_results: Dict[MetricId, MetricResult]) -> PresetResult:
        raise NotImplementedError()
