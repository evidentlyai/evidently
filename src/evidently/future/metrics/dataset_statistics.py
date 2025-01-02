import abc
import typing
from typing import Generator
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently import ColumnType
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.datasets import Dataset
from evidently.future.metrics import SingleValue
from evidently.future.metrics import SingleValueMetricTest
from evidently.future.metrics._legacy import LegacyBasedMetric
from evidently.future.metrics.base import MetricId
from evidently.future.metrics.base import MetricTestResult
from evidently.future.metrics.base import SingleValueMetric
from evidently.future.metrics.base import TResult
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetricResult
from evidently.model.widget import BaseWidgetInfo

if typing.TYPE_CHECKING:
    from evidently.future.report import Context


class RowCount(SingleValueMetric):
    def __init__(self, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__("row_count")
        self.with_tests(tests)

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        return SingleValue(current_data.stats().row_count)

    def display_name(self) -> str:
        return "Row count in dataset"


class ColumnCount(SingleValueMetric):
    def __init__(
        self,
        column_type: Optional[ColumnType] = None,
        tests: Optional[List[SingleValueMetricTest]] = None,
    ):
        super().__init__(f"column_count:{column_type.value if column_type is not None else 'all'}")
        self._type = column_type
        self.with_tests(tests)

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        if self._type is None:
            return SingleValue(current_data.stats().column_count)
        else:
            return SingleValue(
                len([col for col, info in current_data._data_definition.columns.items() if info.type == self._type])
            )

    def display_name(self) -> str:
        return f"Column {f'of type {self._type.value} ' if self._type is not None else ''}count in dataset"


TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)


class DatasetSummaryBasedMetric(
    LegacyBasedMetric[TResult, DatasetSummaryMetric, DatasetSummaryMetricResult], Generic[TResult], abc.ABC
):
    def __init__(self, metric_id: MetricId):
        super().__init__(metric_id, DatasetSummaryMetric())


class DuplicatedRowCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("duplicated_rows")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_duplicated_rows
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return "Duplicated row count in dataset"


class DuplicatedColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("duplicated_columns")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_duplicated_columns
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return "Duplicated column count in dataset"


class AlmostDuplicatedColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("almost_duplicated_columns")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_almost_duplicated_columns
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return f"Almost duplicated column count in dataset (eps={self._metric.almost_duplicated_threshold})"


class AlmostConstantColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("almost_constant_columns")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_almost_constant_columns
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return f"Almost constant column count in dataset (eps={self._metric.almost_constant_threshold})"


class EmptyRowsCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("empty_rows_count")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_empty_rows
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return "Count of empty rows in dataset"


class EmptyColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("empty_columns_count")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_empty_columns
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return "Count of empty columns in dataset"


class ConstantColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    def __init__(self):
        super().__init__("constant_columns_count")

    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_constant_columns
        return SingleValue(value)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def display_name(self) -> str:
        return "Count of constant columns in dataset"
