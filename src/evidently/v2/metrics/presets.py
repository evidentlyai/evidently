import abc
import dataclasses
from typing import Dict
from typing import List

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics.base import Metric
from evidently.v2.metrics.base import MetricId
from evidently.v2.metrics.base import MetricResult
from evidently.v2.metrics.base import render_widgets


@dataclasses.dataclass
class PresetResult:
    widget: List[BaseWidgetInfo]

    def _repr_html_(self):
        return render_widgets(self.widget)


class MetricPreset:
    @abc.abstractmethod
    def metrics(self) -> List[Metric]:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(self, metric_results: Dict[MetricId, MetricResult]) -> PresetResult:
        raise NotImplementedError()