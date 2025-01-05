import abc
import typing
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently import ColumnType
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.datasets import Dataset
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueCalculation
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metric_types import TMetric
from evidently.future.metric_types import TResult
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.metrics._legacy import TLegacyMetric
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
        definition = current_data._data_definition
        if self.metric.column_type is None:
            return SingleValue(current_data.stats().column_count)
        elif self.metric.column_type == ColumnType.Numerical:
            return SingleValue(len([col for col in definition.get_numerical_features() if current_data.column(col)]))
        elif self.metric.column_type == ColumnType.Categorical:
            return SingleValue(len([col for col in definition.get_categorical_features() if current_data.column(col)]))
        elif self.metric.column_type == ColumnType.Text:
            return SingleValue(len([col for col in definition.get_text_features() if current_data.column(col)]))
        elif self.metric.column_type == ColumnType.Datetime:
            return SingleValue(len([col for col in definition.get_datetime_features() if current_data.column(col)]))

    def display_name(self) -> str:
        return f"Column {f'of type {self.metric.column_type.value} ' if self.metric.column_type is not None else ''}count in dataset"


TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)


class DatasetSummaryBasedMetricCalculation(
    LegacyMetricCalculation[TResult, TMetric, DatasetSummaryMetricResult, DatasetSummaryMetric],
    Generic[TResult, TMetric],
    abc.ABC,
):
    _legacy_metric: Optional[TLegacyMetric] = None

    def legacy_metric(self) -> DatasetSummaryMetric:
        if self._legacy_metric is None:
            self._legacy_metric = DatasetSummaryMetric()
        return self._legacy_metric


class DuplicatedRowCount(SingleValueMetric):
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


class DuplicatedColumnsCount(SingleValueMetric):
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


class AlmostDuplicatedColumnsCount(SingleValueMetric):
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
        return f"Almost duplicated column count in dataset (eps={self.legacy_metric().almost_duplicated_threshold})"


class AlmostConstantColumnsCount(SingleValueMetric):
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
        return f"Almost constant column count in dataset (eps={self.legacy_metric().almost_constant_threshold})"


class EmptyRowsCount(SingleValueMetric):
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


class EmptyColumnsCount(SingleValueMetric):
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


class ConstantColumnsCount(SingleValueMetric):
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


class DatasetMissingValueCount(SingleValueMetric):
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


class RowsWithMissingValuesCount:
    pass
