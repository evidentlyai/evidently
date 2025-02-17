from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from evidently import ColumnType
from evidently.future.container import MetricContainer
from evidently.future.metric_types import ColumnMetric
from evidently.future.metric_types import Metric
from evidently.future.report import Context


class ColumnMetricGenerator(MetricContainer):
    def __init__(
        self,
        metric_type: Type[ColumnMetric],
        columns: Optional[List[str]] = None,
        column_types: Optional[Union[ColumnType, List[ColumnType]]] = None,
        metric_kwargs: Optional[Dict[str, Any]] = None,
    ):
        self.metric_type = metric_type
        self.columns = columns
        self.column_types = column_types
        self.metric_kwargs = metric_kwargs or {}

    def _instantiate_metric(self, column: str) -> Metric:
        return self.metric_type(column=column, **self.metric_kwargs)

    def generate_metrics(self, context: "Context") -> List[Metric]:
        if self.columns is not None:
            column_list = self.columns
        else:
            raise NotImplementedError()
        return [self._instantiate_metric(column) for column in column_list]
