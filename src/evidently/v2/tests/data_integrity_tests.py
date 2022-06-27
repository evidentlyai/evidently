from numbers import Number
from typing import List
from typing import Optional
from typing import Union

from evidently.v2.metrics.data_integrity_metrics import DataIntegrityMetrics

from .base_test import BaseCheckValueTest


class BaseIntegrityValueTest(BaseCheckValueTest):
    data_integrity_metric: DataIntegrityMetrics

    def __init__(
        self,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        data_integrity_metric: Optional[DataIntegrityMetrics] = None
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric


class TestNumberOfColumns(BaseIntegrityValueTest):
    """Number of all columns in the dataframe, including utility columns (id/index, datetime, target, predictions)"""
    name = "Test Number of Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of columns is {value}"


class TestNumberOfRows(BaseIntegrityValueTest):
    """Number of rows in the dataframe"""
    name = "Test Number of Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of rows is {value}"


class TestNumberOfNANs(BaseIntegrityValueTest):
    """Number of NAN values in the dataframe without aggregation by rows or columns"""
    name = "Test Number of NAN Values"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_nans
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of NANs is {value}"


class TestNumberOfColumnsWithNANs(BaseIntegrityValueTest):
    """Number of columns contained at least one NAN value"""
    name = "Test Number Of Columns With Nulls"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_columns_with_nans
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of columns with NANs is {value}"


class TestNumberOfRowsWithNANs(BaseIntegrityValueTest):
    """Number of rows contained at least one NAN value"""
    name = "Test Number Of Rows With NANs"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_rows_with_nans
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of rows with NANs is {value}"


class TestNumberOfConstantColumns(BaseIntegrityValueTest):
    """Number of columns contained only one unique value"""
    name = "Test Number Of Constant Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_constant_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of constant columns: {value}"


class TestNumberOfEmptyRows(BaseIntegrityValueTest):
    """Number of rows contained all NAN values"""
    name = "Test Number Of Empty Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_empty_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of empty rows: {value}"


class TestNumberOfEmptyColumns(BaseIntegrityValueTest):
    """Number of columns contained all NAN values"""
    name = "Test Number Of Empty Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_empty_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of empty columns: {value}"


class TestNumberOfDuplicatedRows(BaseIntegrityValueTest):
    """How many rows have duplicates in the dataset"""
    name = "Test Number Of Duplicated Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_duplicated_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of duplicated rows: {value}"


class TestNumberOfDuplicatedColumns(BaseIntegrityValueTest):
    """How many columns have duplicates in the dataset"""
    name = "Test Number Of Duplicated Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_duplicated_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of duplicated columns: {value}"
