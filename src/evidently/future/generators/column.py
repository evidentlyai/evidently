from itertools import chain
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import Union

from evidently import ColumnType
from evidently.future.container import ColumnMetricContainer
from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
from evidently.future.metric_types import ColumnMetric
from evidently.future.metric_types import MetricId
from evidently.future.report import Context
from evidently.model.widget import BaseWidgetInfo

ColumnTypeStr = Union[ColumnType, str]


class ColumnMetricGenerator(MetricContainer):
    def __init__(
        self,
        metric_type: Union[Type[ColumnMetric], Type[ColumnMetricContainer]],
        columns: Optional[List[str]] = None,
        column_types: Union[ColumnTypeStr, List[ColumnTypeStr], Literal["all"]] = "all",
        metric_kwargs: Optional[Dict[str, Any]] = None,
    ):
        self.metric_type = metric_type
        self.columns = columns
        self.column_types = column_types
        self.metric_kwargs = metric_kwargs or {}

    def _instantiate_metric(self, column: str) -> MetricOrContainer:
        return self.metric_type(column=column, **self.metric_kwargs)

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        if self.columns is not None:
            column_list = self.columns
        else:
            column_types: Union[ColumnTypeStr, List[ColumnTypeStr]]
            if self.column_types == "all":
                column_types = list(ColumnType)
            else:
                column_types = self.column_types
            column_types = column_types if isinstance(column_types, list) else [column_types]
            cts: List[ColumnType] = [ct if isinstance(ct, ColumnType) else ColumnType(ct) for ct in column_types]
            column_list = list(context.data_definition.get_columns(cts))
        return [self._instantiate_metric(column) for column in column_list]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        return list(chain(*[widget[1] for widget in (child_widgets or [])]))
