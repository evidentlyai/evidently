import abc
import typing
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently import ColumnType
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.datasets import Dataset
from evidently.future.metrics._legacy import LegacyBasedMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.metrics.base import SingleValue
from evidently.future.metrics.base import SingleValueCalculation
from evidently.future.metrics.base import SingleValueMetric
from evidently.future.metrics.base import TResult
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetricResult
from evidently.model.widget import BaseWidgetInfo

if typing.TYPE_CHECKING:
    from evidently.future.report import Context


class RowCount(SingleValueMetric):
    pass


class RowCountCalculation(SingleValueCalculation[RowCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        return SingleValue(current_data.stats().row_count)

    def display_name(self) -> str:
        return "Row count in dataset"


class ColumnCount(SingleValueMetric):
    column_type: Optional[ColumnType] = None


class ColumnCountCalculation(SingleValueCalculation[ColumnCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        if self.metric.column_type is None:
            return SingleValue(current_data.stats().column_count)
        else:
            return SingleValue(
                len(
                    [
                        col
                        for col, info in current_data._data_definition.columns.items()
                        if info.type == self.metric.column_type
                    ]
                )
            )

    def display_name(self) -> str:
        return f"Column {f'of type {self.metric.column_type.value} ' if self.metric.column_type is not None else ''}count in dataset"


TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)


class DatasetSummaryBasedMetric(
    LegacyBasedMetric[TResult, DatasetSummaryMetric, DatasetSummaryMetricResult], Generic[TResult], abc.ABC
):
    def _get_legacy_metric(self) -> DatasetSummaryMetric:
        return DatasetSummaryMetric()


TDatasetSummaryBasedMetric = TypeVar("TDatasetSummaryBasedMetric", bound=DatasetSummaryBasedMetric)


class DatasetSummaryBasedMetricCalculation(
    LegacyMetricCalculation[TResult, DatasetSummaryMetric, DatasetSummaryMetricResult, TDatasetSummaryBasedMetric],
    Generic[TResult, TDatasetSummaryBasedMetric],
    abc.ABC,
):
    pass


class DuplicatedRowCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class DuplicatedRowCountCalculation(DatasetSummaryBasedMetricCalculation[SingleValue, DuplicatedRowCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_duplicated_rows
        return SingleValue(value)

    def display_name(self) -> str:
        return "Duplicated row count in dataset"


class DuplicatedColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class DuplicatedColumnsCountCalculation(DatasetSummaryBasedMetricCalculation[SingleValue, DuplicatedColumnsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_duplicated_columns
        return SingleValue(value)

    def display_name(self) -> str:
        return "Duplicated column count in dataset"


class AlmostDuplicatedColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class AlmostDuplicatedColumnsCountCalculation(
    DatasetSummaryBasedMetricCalculation[SingleValue, AlmostDuplicatedColumnsCount]
):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_almost_duplicated_columns
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Almost duplicated column count in dataset (eps={self.legacy_metric.almost_duplicated_threshold})"


class AlmostConstantColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class AlmostConstantColumnsCountCalculation(
    DatasetSummaryBasedMetricCalculation[SingleValue, AlmostConstantColumnsCount]
):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_almost_constant_columns
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Almost constant column count in dataset (eps={self.legacy_metric.almost_constant_threshold})"


class EmptyRowsCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class EmptyRowsCountCalculation(DatasetSummaryBasedMetricCalculation[SingleValue, EmptyRowsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_empty_rows
        return SingleValue(value)

    def display_name(self) -> str:
        return "Count of empty rows in dataset"


class EmptyColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class EmptyColumnsCountCalculation(DatasetSummaryBasedMetricCalculation[SingleValue, EmptyColumnsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_empty_columns
        return SingleValue(value)

    def display_name(self) -> str:
        return "Count of empty columns in dataset"


class ConstantColumnsCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class ConstantColumnsCountCalculation(DatasetSummaryBasedMetricCalculation[SingleValue, ConstantColumnsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_constant_columns
        return SingleValue(value)

    def display_name(self) -> str:
        return "Count of constant columns in dataset"


class DatasetMissingValueCount(DatasetSummaryBasedMetric[SingleValue]):
    pass


class DatasetMissingValueCountCalculation(DatasetSummaryBasedMetricCalculation[SingleValue, DatasetMissingValueCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        value = legacy_result.current.number_of_missing_values
        return SingleValue(value)

    def display_name(self) -> str:
        return "Count of missing values in dataset"
