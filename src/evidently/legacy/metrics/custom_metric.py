from typing import Callable
from typing import List
from typing import Optional
from typing import Union

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import counter


class CustomCallableMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:CustomCallableMetricResult"

    value: float


CustomCallableType = Callable[[InputData], float]


class CustomValueMetric(Metric[CustomCallableMetricResult]):
    class Config:
        type_alias = "evidently:metric:CustomValueMetric"

    func: str
    title: Optional[str] = None
    size: Optional[WidgetSize] = None

    _func: Optional[CustomCallableType] = PrivateAttr(None)

    def __init__(
        self,
        func: Union[CustomCallableType, str],
        title: str = None,
        size: Optional[WidgetSize] = None,
        options: AnyOptions = None,
        **data,
    ):
        if callable(func):
            self._func = func
            self.func = f"{func.__module__}.{func.__name__}"
        else:
            self._func = None
            self.func = func
        self.title = title
        self.size = size
        super().__init__(options, **data)

    def calculate(self, data: InputData) -> CustomCallableMetricResult:
        if self._func is None:
            raise ValueError("CustomCallableMetric is not configured with callable func")
        return CustomCallableMetricResult(value=self._func(data))


@default_renderer(wrap_type=CustomValueMetric)
class CustomValueMetricRenderer(MetricRenderer):
    def render_html(self, obj: CustomValueMetric) -> List[BaseWidgetInfo]:
        return [
            counter(
                counters=[CounterData.float("", obj.get_result().value, 2)],
                title=obj.title or "",
                size=WidgetSize.HALF if obj.size == WidgetSize.HALF else WidgetSize.FULL,
            ),
        ]
