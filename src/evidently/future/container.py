import abc
import itertools
from typing import TYPE_CHECKING
from typing import Generator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.model.widget import BaseWidgetInfo

if TYPE_CHECKING:
    from evidently.future.report import Context

MetricOrContainer = Union[Metric, "MetricContainer"]


class MetricContainer(abc.ABC):
    _metrics: Optional[List[MetricOrContainer]] = None

    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[MetricOrContainer]:
        if self._metrics is None:
            self._metrics = list(self.generate_metrics(context))
        return self._metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        return list(itertools.chain(*[widget[1] for widget in child_widgets]))

    def list_metrics(self) -> Generator[Metric, None, None]:
        if self._metrics is None:
            raise ValueError("Metrics weren't composed in container")
        for item in self._metrics:
            if isinstance(item, Metric):
                yield item
            elif isinstance(item, MetricContainer):
                yield from item.list_metrics()
            else:
                raise ValueError(f"invalid metric type {type(item)}")


class ColumnMetricContainer(MetricContainer, abc.ABC):
    def __init__(self, column: str):
        self._column = column
