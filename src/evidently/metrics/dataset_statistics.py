import abc
import typing
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently.core.datasets import Dataset
from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import CountCalculation
from evidently.core.metric_types import CountMetric
from evidently.core.metric_types import CountValue
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.metric_types import TCountMetric
from evidently.core.metric_types import TResult
from evidently.core.metric_types import TSingleValueMetric
from evidently.legacy.base_metric import MetricResult as LegacyMetricResult
from evidently.legacy.core import ColumnType
from evidently.legacy.metrics import DatasetSummaryMetric
from evidently.legacy.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.metrics._legacy import LegacyMetricCalculation
from evidently.tests import Reference
from evidently.tests import eq
from evidently.tests import gt
from evidently.tests import lte

if typing.TYPE_CHECKING:
    from evidently.core.report import Context


class RowCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [gt(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class RowCountCalculation(SingleValueCalculation[RowCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self.result(current_data.stats().row_count),
            None if reference_data is None else self.result(reference_data.stats().row_count),
        )

    def display_name(self) -> str:
        return "Row count in dataset"


class ColumnCount(SingleValueMetric):
    column_type: Optional[ColumnType] = None

    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [gt(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            eq(Reference()).bind_single(self.get_fingerprint()),
        ]


class ColumnCountCalculation(SingleValueCalculation[ColumnCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_for_dataset(current_data),
            None if reference_data is None else self._calculate_for_dataset(reference_data),
        )

    def display_name(self) -> str:
        return f"Column {f'of type {self.metric.column_type.value} ' if self.metric.column_type is not None else ''}count in dataset"

    def _calculate_for_dataset(self, dataset: Dataset) -> SingleValue:
        definition = dataset._data_definition
        if self.metric.column_type is None:
            return self.result(dataset.stats().column_count)
        elif self.metric.column_type == ColumnType.Numerical:
            return self.result(
                len([col for col in definition.get_numerical_columns() if dataset.column(col)]),
            )
        elif self.metric.column_type == ColumnType.Categorical:
            return self.result(
                len([col for col in definition.get_categorical_columns() if dataset.column(col)]),
            )
        elif self.metric.column_type == ColumnType.Text:
            return self.result(
                len([col for col in definition.get_text_columns() if dataset.column(col)]),
            )
        elif self.metric.column_type == ColumnType.Datetime:
            return self.result(
                len([col for col in definition.get_datetime_columns() if dataset.column(col)]),
            )
        raise ValueError(f"Column count does not support {self.metric.column_type} type")


TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)


class LegacyDatasetSummaryMixin:
    _legacy_metric: Optional[DatasetSummaryMetric] = None

    def legacy_metric(self) -> DatasetSummaryMetric:
        if self._legacy_metric is None:
            self._legacy_metric = DatasetSummaryMetric()
        return self._legacy_metric


class DatasetSummarySingleValueCalculation(
    LegacyDatasetSummaryMixin,
    LegacyMetricCalculation[TResult, TSingleValueMetric, DatasetSummaryMetricResult, DatasetSummaryMetric],
    SingleValueCalculation[TSingleValueMetric],
    Generic[TResult, TSingleValueMetric],
    abc.ABC,
):
    pass


class DatasetSummaryCountValueCalculation(
    LegacyDatasetSummaryMixin,
    LegacyMetricCalculation[TResult, TCountMetric, DatasetSummaryMetricResult, DatasetSummaryMetric],
    CountCalculation[TCountMetric],
    Generic[TResult, TCountMetric],
    abc.ABC,
):
    pass


class DuplicatedRowCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class DuplicatedRowCountCalculation(DatasetSummarySingleValueCalculation[SingleValue, DuplicatedRowCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_duplicated_rows
        return (
            self.result(value),
            None if legacy_result.reference is None else self.result(legacy_result.reference.number_of_duplicated_rows),
        )

    def display_name(self) -> str:
        return "Duplicated row count in dataset"


class DuplicatedColumnsCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            lte(Reference()).bind_single(self.get_fingerprint()),
        ]


class DuplicatedColumnsCountCalculation(DatasetSummarySingleValueCalculation[SingleValue, DuplicatedColumnsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_duplicated_columns
        return (
            self.result(value),
            None
            if legacy_result.reference is None
            else self.result(legacy_result.reference.number_of_duplicated_columns),
        )

    def display_name(self) -> str:
        return "Duplicated column count in dataset"


class AlmostDuplicatedColumnsCount(SingleValueMetric):
    pass


class AlmostDuplicatedColumnsCountCalculation(
    DatasetSummarySingleValueCalculation[SingleValue, AlmostDuplicatedColumnsCount]
):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_almost_duplicated_columns
        return (
            self.result(value),
            None
            if legacy_result.reference is None
            else self.result(legacy_result.reference.number_of_almost_duplicated_columns),
        )

    def display_name(self) -> str:
        return f"Almost duplicated column count in dataset (eps={self.legacy_metric().almost_duplicated_threshold})"


class AlmostConstantColumnsCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            lte(Reference()).bind_single(self.get_fingerprint()),
        ]


class AlmostConstantColumnsCountCalculation(
    DatasetSummarySingleValueCalculation[SingleValue, AlmostConstantColumnsCount]
):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_almost_constant_columns
        return (
            self.result(value),
            None
            if legacy_result.reference is None
            else self.result(legacy_result.reference.number_of_almost_constant_columns),
        )

    def display_name(self) -> str:
        return f"Almost constant column count in dataset (eps={self.legacy_metric().almost_constant_threshold})"


class EmptyRowsCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class EmptyRowsCountCalculation(DatasetSummarySingleValueCalculation[SingleValue, EmptyRowsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_empty_rows
        return (
            self.result(value),
            None if legacy_result.reference is None else self.result(legacy_result.reference.number_of_empty_rows),
        )

    def display_name(self) -> str:
        return "Count of empty rows in dataset"


class EmptyColumnsCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            lte(Reference()).bind_single(self.get_fingerprint()),
        ]


class EmptyColumnsCountCalculation(DatasetSummarySingleValueCalculation[SingleValue, EmptyColumnsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_empty_columns
        return (
            self.result(value),
            None if legacy_result.reference is None else self.result(legacy_result.reference.number_of_empty_columns),
        )

    def display_name(self) -> str:
        return "Count of empty columns in dataset"


class ConstantColumnsCount(SingleValueMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            lte(Reference()).bind_single(self.get_fingerprint()),
        ]


class ConstantColumnsCountCalculation(DatasetSummarySingleValueCalculation[SingleValue, ConstantColumnsCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_constant_columns
        return (
            self.result(value),
            None
            if legacy_result.reference is None
            else self.result(legacy_result.reference.number_of_constant_columns),
        )

    def display_name(self) -> str:
        return "Count of constant columns in dataset"


class DatasetMissingValueCount(CountMetric):
    def _default_tests(self, context: "Context") -> List[BoundTest]:
        return [eq(0).bind_count(self.get_fingerprint(), is_count=True)]

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), is_count=True),
        ]


class DatasetMissingValueCountCalculation(DatasetSummaryCountValueCalculation[CountValue, DatasetMissingValueCount]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: DatasetSummaryMetricResult,
        render: List[BaseWidgetInfo],
    ):
        value = legacy_result.current.number_of_missing_values
        return (
            self.result(value, value / legacy_result.current.number_of_rows),
            None
            if legacy_result.reference is None
            else self.result(
                legacy_result.reference.number_of_missing_values,
                legacy_result.reference.number_of_missing_values / legacy_result.reference.number_of_rows,
            ),
        )

    def display_name(self) -> str:
        return "Count and share of missing values in dataset"
