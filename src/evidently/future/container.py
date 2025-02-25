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
    @abc.abstractmethod
    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        raise NotImplementedError()

    def metrics(self, context: "Context") -> List[MetricOrContainer]:
        metric_container_hash = hash(self)
        metrics = context.metrics_container(metric_container_hash)
        if metrics is None:
            metrics = list(self.generate_metrics(context))
            context.set_metric_container_data(metric_container_hash, metrics)
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        return list(itertools.chain(*[widget[1] for widget in (child_widgets or [])]))

    def list_metrics(self, context: "Context") -> Generator[Metric, None, None]:
        metrics = context.metrics_container(hash(self))
        if metrics is None:
            raise ValueError("Metrics weren't composed in container")
        for item in metrics:
            if isinstance(item, Metric):
                yield item
            elif isinstance(item, MetricContainer):
                yield from item.list_metrics(context)
            else:
                raise ValueError(f"invalid metric type {type(item)}")


class ColumnMetricContainer(MetricContainer, abc.ABC):
    def __init__(self, column: str):
        self._column = column
