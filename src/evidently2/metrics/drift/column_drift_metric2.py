from typing import Any, Dict, Generic, Optional, TypeVar

from evidently.base_metric import ColumnName, MetricResult
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently2.core.calculation import DataType
from evidently2.metrics.drift.column_drift_metric import ColumnDriftResult

ReferenceResultType = TypeVar("ReferenceResultType", bound=MetricResult)
ResultType = TypeVar("ResultType", bound=MetricResult)

class Metric3(EvidentlyBaseModel, Generic[ReferenceResultType, ResultType]):
    def calculate_reference(self, reference: DataType) -> ReferenceResultType:
        raise NotImplementedError

    def calculate(self, ref: ReferenceResultType, current: DataType) -> ResultType:
        raise NotImplementedError


class StatTestReferenceResult(MetricResult):
    pass

class ChiSquareReferenceResult(StatTestReferenceResult):
    value_counts: Dict[Any, int]
    size: int

class ColumnDriftReferenceResult(MetricResult):
    stat_test: str
    stat_test_result: StatTestReferenceResult


class ColumnDriftMetric(Metric3[ColumnDriftReferenceResult, ColumnDriftResult]):
    column_name: ColumnName
    stattest: Optional[str]
    stattest_threshold: Optional[float]

    def calculate_reference(self, reference: DataType) -> ColumnDriftReferenceResult:
        pass

    def calculate(self, ref: ColumnDriftReferenceResult, current: DataType) -> ColumnDriftResult:
        pass

