import abc
import dataclasses
from typing import Dict
from typing import List

from evidently.future.metrics.base import MetricCalculationBase
from evidently.future.metrics.base import MetricId
from evidently.future.metrics.base import MetricResult
from evidently.future.metrics.base import render_widgets
from evidently.model.widget import BaseWidgetInfo


@dataclasses.dataclass
class PresetResult:
    widget: List[BaseWidgetInfo]

    def _repr_html_(self):
        return render_widgets(self.widget)


class MetricPreset:
    @abc.abstractmethod
    def metrics(self) -> List[MetricCalculationBase]:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(self, metric_results: Dict[MetricId, MetricResult]) -> PresetResult:
        raise NotImplementedError()
