import abc
import itertools
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Generator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import convert_tests
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel

if TYPE_CHECKING:
    from evidently.core.report import Context

MetricOrContainer = Union[Metric, "MetricContainer"]


class MetricContainer(AutoAliasMixin, EvidentlyBaseModel, abc.ABC):
    __alias_type__: ClassVar[str] = "metric_container"

    class Config:
        is_base_type = True

    include_tests: bool = True

    def __init__(self, include_tests: bool = True, **data):
        self.include_tests = include_tests
        super().__init__(**data)

    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[MetricOrContainer]:
        metric_container_fp = self.get_fingerprint()
        metrics = context.metrics_container(metric_container_fp)
        if metrics is None:
            metrics = list(self.generate_metrics(context))
            context.set_metric_container_data(metric_container_fp, metrics)
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        return list(itertools.chain(*[widget[1] for widget in (child_widgets or [])]))

    def list_metrics(self, context: "Context") -> Generator[Metric, None, None]:
        metrics = context.metrics_container(self.get_fingerprint())
        if metrics is None:
            raise ValueError("Metrics weren't composed in container")
        for item in metrics:
            if isinstance(item, Metric):
                yield item
            elif isinstance(item, MetricContainer):
                yield from item.list_metrics(context)
            else:
                raise ValueError(f"invalid metric type {type(item)}")

    def _get_tests(self, tests):
        if tests is not None:
            return convert_tests(tests)
        if self.include_tests:
            return None
        return []


MetricOrContainer = Union[Metric, MetricContainer]


class ColumnMetricContainer(MetricContainer, abc.ABC):
    column: str

    def __init__(self, column: str, include_tests: bool = True):
        self.column = column
        super().__init__(include_tests=include_tests)
