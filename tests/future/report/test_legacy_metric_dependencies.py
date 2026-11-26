from typing import List

from evidently import Report
from evidently.core.report import Context
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer


class DependencyValue(MetricResult):
    class Config:
        alias_required = False

    value: int


class LeafMetric(Metric[DependencyValue]):
    class Config:
        alias_required = False

    number: int

    def calculate(self, data: InputData) -> DependencyValue:
        return DependencyValue(value=self.number)


class PairMetric(Metric[DependencyValue]):
    class Config:
        alias_required = False

    first: LeafMetric
    second: LeafMetric

    def calculate(self, data: InputData) -> DependencyValue:
        return DependencyValue(value=self.first.get_result().value * 10 + self.second.get_result().value)


@default_renderer(wrap_type=LeafMetric)
class LeafMetricRenderer(MetricRenderer):
    def render_html(self, obj: LeafMetric) -> List[BaseWidgetInfo]:
        return []


@default_renderer(wrap_type=PairMetric)
class PairMetricRenderer(MetricRenderer):
    def render_html(self, obj: PairMetric) -> List[BaseWidgetInfo]:
        return []


def test_legacy_metric_dependencies_keep_their_own_results():
    context = Context(Report([]))
    metric = PairMetric(first=LeafMetric(number=1), second=LeafMetric(number=2))

    result, _ = context.get_legacy_metric(metric, lambda _context, _task_name: None, None)  # type: ignore[arg-type]

    assert result.value == 12
