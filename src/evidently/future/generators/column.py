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
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import ValidationError
from evidently.future.container import ColumnMetricContainer
from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
from evidently.future.metric_types import ColumnMetric
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.report import Context
from evidently.model.widget import BaseWidgetInfo

ColumnTypeStr = Union[ColumnType, str]


class ColumnMetricGenerator(MetricContainer):
    metric_type_alias: str
    _metric_type: Union[Type[ColumnMetric], Type[ColumnMetricContainer]] = PrivateAttr()
    columns: Optional[List[str]] = None
    column_types: Union[ColumnTypeStr, List[ColumnTypeStr], Literal["all"]] = "all"
    metric_kwargs: Dict[str, Any]

    def __init__(
        self,
        metric_type: Optional[Union[Type[ColumnMetric], Type[ColumnMetricContainer]]] = None,
        columns: Optional[List[str]] = None,
        column_types: Union[ColumnTypeStr, List[ColumnTypeStr], Literal["all"]] = "all",
        metric_kwargs: Optional[Dict[str, Any]] = None,
        metric_type_alias: Optional[str] = None,
        include_tests: bool = True,
    ):
        if isinstance(metric_type, type):
            assert issubclass(metric_type, ColumnMetric) or issubclass(
                metric_type, ColumnMetricContainer
            ), "metric_type must be a subclass of ColumnMetric or ColumnMetricContainer"
            metric_type_alias = metric_type.__get_type__()
        if metric_type is None:
            assert metric_type_alias is not None, "metric_type must be specified if metric_type is not provided"
            try:
                metric_type = Metric.load_alias(metric_type_alias)
            except ValidationError:
                metric_type = MetricContainer.load_alias(metric_type_alias)
            assert issubclass(metric_type, ColumnMetric) or issubclass(
                metric_type, ColumnMetricContainer
            ), "metric_type_alias must be an alias of ColumnMetric or ColumnMetricContainer subclass"
        assert metric_type_alias is not None, "metric_type_alias or metric_type must be specified"
        self.metric_type_alias = metric_type_alias
        self._metric_type = metric_type
        self.columns = columns
        self.column_types = column_types
        self.metric_kwargs = metric_kwargs or {}
        super().__init__(include_tests=True)

    def _instantiate_metric(self, column: str) -> MetricOrContainer:
        return self._metric_type(column=column, **self.metric_kwargs)

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
