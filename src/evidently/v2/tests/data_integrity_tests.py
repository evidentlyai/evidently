from abc import ABC
from numbers import Number
from typing import List
from typing import Optional
from typing import Union

import numpy as np

from evidently.v2.metrics.data_integrity_metrics import DataIntegrityMetrics
from evidently.v2.metrics.data_integrity_metrics import DataIntegrityValueByRegexpMetrics
from evidently.v2.renderers.base_renderer import default_renderer
from evidently.v2.renderers.base_renderer import TestRenderer
from evidently.v2.renderers.base_renderer import TestHtmlInfo
from evidently.v2.tests.base_test import BaseCheckValueTest
from evidently.v2.tests.base_test import BaseConditionsTest
from evidently.v2.tests.base_test import Test
from evidently.v2.tests.base_test import TestResult
from evidently.v2.tests.utils import plot_dicts_to_table


class BaseIntegrityValueTest(BaseCheckValueTest, ABC):
    group = "data_integrity"
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
        data_integrity_metric: Optional[DataIntegrityMetrics] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric


class TestNumberOfColumns(BaseIntegrityValueTest):
    """Number of all columns in the data, including utility columns (id/index, datetime, target, predictions)"""

    name = "Test Number of Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of columns is {value}"


@default_renderer(test_type=TestNumberOfColumns)
class TestNumberOfColumnsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current dtype"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.columns_type
        dict_ref = None

        if obj.data_integrity_metric.get_result().reference_stats is not None:
            dict_ref = obj.data_integrity_metric.get_result().reference_stats.columns_type
            columns = columns + ["reference dtype"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_column", "diff")
        info.details = additional_plots
        return info


class TestNumberOfRows(BaseIntegrityValueTest):
    """Number of rows in the data"""

    name = "Test Number of Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of rows is {value}"


class TestNumberOfNANs(BaseIntegrityValueTest):
    """Number of NAN values in the data without aggregation by rows or columns"""

    name = "Test Number of NAN Values"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_nans
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of NANs is {value}"


@default_renderer(test_type=TestNumberOfNANs)
class TestNumberOfNANsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfNANs) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        dict_ref = None

        if obj.data_integrity_metric.get_result().reference_stats is not None:
            dict_ref = obj.data_integrity_metric.get_result().reference_stats.nans_by_columns
            columns = columns + ["reference number of NaNs"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_nans")
        info.details = additional_plots
        return info


class TestNumberOfColumnsWithNANs(BaseIntegrityValueTest):
    """Number of columns contained at least one NAN value"""

    name = "Test Number Of Columns With Nulls"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_columns_with_nans
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of columns with NANs is {value}"


@default_renderer(test_type=TestNumberOfColumnsWithNANs)
class TestNumberOfColumnsWithNANsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfColumnsWithNANs) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        dict_ref = None

        if obj.data_integrity_metric.get_result().reference_stats is not None:
            dict_ref = obj.data_integrity_metric.get_result().reference_stats.nans_by_columns
            columns = columns + ["reference number of NaNs"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_cols_with_nans")
        info.details = additional_plots
        return info


class TestNumberOfRowsWithNANs(BaseIntegrityValueTest):
    """Number of rows contained at least one NAN value"""

    name = "Test Number Of Rows With NANs"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_rows_with_nans
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of rows with NANs is {value}"


class TestNumberOfConstantColumns(BaseIntegrityValueTest):
    """Number of columns contained only one unique value"""

    name = "Test Number Of Constant Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_constant_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of constant columns: {value}"


@default_renderer(test_type=TestNumberOfConstantColumns)
class TestNumberOfConstantColumnsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfConstantColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current nunique"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.number_uniques_by_columns
        dict_ref = None

        if obj.data_integrity_metric.get_result().reference_stats is not None:
            dict_ref = obj.data_integrity_metric.get_result().reference_stats.number_uniques_by_columns
            columns = columns + ["reference nunique"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_cols_with_nans", "curr", True)
        info.details = additional_plots
        return info


class TestNumberOfEmptyRows(BaseIntegrityValueTest):
    """Number of rows contained all NAN values"""

    name = "Test Number Of Empty Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_empty_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of empty rows: {value}"


class TestNumberOfEmptyColumns(BaseIntegrityValueTest):
    """Number of columns contained all NAN values"""

    name = "Test Number Of Empty Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_empty_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of empty columns: {value}"


@default_renderer(test_type=TestNumberOfEmptyColumns)
class TestNumberOfEmptyColumnsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfEmptyColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        dict_ref = None
        if obj.data_integrity_metric.get_result().reference_stats is not None:
            dict_ref = obj.data_integrity_metric.get_result().reference_stats.nans_by_columns
            columns = columns + ["reference number of NaNs"]
        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_empty_columns")
        info.details = additional_plots
        return info


class TestNumberOfDuplicatedRows(BaseIntegrityValueTest):
    """How many rows have duplicates in the dataset"""

    name = "Test Number Of Duplicated Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_duplicated_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of duplicated rows: {value}"


class TestNumberOfDuplicatedColumns(BaseIntegrityValueTest):
    """How many columns have duplicates in the dataset"""

    name = "Test Number Of Duplicated Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().current_stats.number_of_duplicated_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of duplicated columns: {value}"


class BaseIntegrityByColumnsConditionTest(BaseConditionsTest, ABC):
    group = "data_integrity"
    data_integrity_metric: DataIntegrityMetrics
    column_name: str

    def __init__(
        self,
        column_name: str = None,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        data_integrity_metric: Optional[DataIntegrityMetrics] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.column_name = column_name

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric


class TestColumnNANShare(BaseIntegrityByColumnsConditionTest):
    """Test the share of NANs in a column"""

    name = "Test Share of NANs in a Column"

    def check(self):
        nans_by_columns = self.data_integrity_metric.get_result().current_stats.nans_by_columns
        number_of_rows = self.data_integrity_metric.get_result().current_stats.number_of_rows

        if self.column_name not in nans_by_columns:
            status = TestResult.ERROR
            description = f"No column '{self.column_name}' in the metrics data"

        else:
            nans_share = nans_by_columns[self.column_name] / number_of_rows

            if not self.condition.check_value(nans_share):
                status = TestResult.FAIL
                description = f"For column '{self.column_name}' share of NANs is {np.round(nans_share, 3)}"
            else:
                description = f"For column '{self.column_name}' share of NANs is {np.round(nans_share, 3)}"
                status = TestResult.SUCCESS

        return TestResult(name=self.name, description=description, status=status)


class BaseIntegrityByColumnsTest(Test, ABC):
    group = "data_integrity"
    data_integrity_metric: DataIntegrityMetrics
    columns: Optional[List[str]]

    def __init__(
        self, columns: Optional[List[str]] = None, data_integrity_metric: Optional[DataIntegrityMetrics] = None
    ):
        self.columns = columns

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric


class TestAllConstantValues(BaseIntegrityByColumnsTest):
    """Test that there is only one unique value in a column"""

    name = "Test Column Has One Constant Value"
    data_integrity_metric: DataIntegrityMetrics

    def check(self):
        description = "All tested columns have constant values"
        status = TestResult.SUCCESS

        uniques_by_columns = self.data_integrity_metric.get_result().current_stats.number_uniques_by_columns

        if not self.columns:
            check_columns = uniques_by_columns.keys()

        else:
            check_columns = self.columns

        for column_name in check_columns:
            if column_name not in uniques_by_columns:
                status = TestResult.ERROR
                description = f"No column '{column_name}' in the metrics data"
                break

            else:
                uniques_by_column = uniques_by_columns[column_name]

                if uniques_by_column != 1:
                    status = TestResult.FAIL
                    description = f"Column '{column_name}' has {uniques_by_column} unique values"
                    break

        return TestResult(name=self.name, description=description, status=status)


class TestAllUniqueValues(BaseIntegrityByColumnsTest):
    """Test that there is only uniques values in a column"""

    name = "Test Column Has Unique Values Only"

    def check(self):
        description = "All tested columns have unique values"
        status = TestResult.SUCCESS

        uniques_by_columns = self.data_integrity_metric.get_result().current_stats.number_uniques_by_columns
        number_of_rows = self.data_integrity_metric.get_result().current_stats.number_of_rows
        nans_by_columns = self.data_integrity_metric.get_result().current_stats.nans_by_columns

        if not self.columns:
            check_columns = uniques_by_columns.keys()

        else:
            check_columns = self.columns

        for column_name in check_columns:
            if column_name not in uniques_by_columns or column_name not in nans_by_columns:
                status = TestResult.ERROR
                description = f"No column '{column_name}' in the metrics data"
                break

            else:
                uniques_in_column = uniques_by_columns[column_name]
                nans_in_column = nans_by_columns[column_name]

                if uniques_in_column != number_of_rows - nans_in_column:
                    status = TestResult.FAIL
                    description = f"Column '{column_name}' has {uniques_in_column} unique values"
                    break

        return TestResult(name=self.name, description=description, status=status)


class TestColumnsType(Test):
    """This test compares a column type against the specified type"""
    group = "data_integrity"
    name = "Test Columns Type"
    columns_type: dict
    data_integrity_metric: DataIntegrityMetrics

    def __init__(self, columns_type: dict, data_integrity_metric: Optional[DataIntegrityMetrics] = None):
        self.columns_type = columns_type
        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric

    def check(self):
        description = "All columns types are ok"
        status = TestResult.SUCCESS
        data_columns_type = self.data_integrity_metric.get_result().current_stats.columns_type

        if not self.columns_type:
            status = TestResult.ERROR
            description = "Columns type condition is empty"

        else:
            for column_name, column_type in self.columns_type.items():
                real_column_type = data_columns_type.get(column_name)

                if real_column_type is None:
                    status = TestResult.ERROR
                    description = f"No column '{column_name}' in the metrics data"
                    break

                elif column_type != real_column_type:
                    status = TestResult.FAIL
                    description = f"Column '{column_name}' type is {real_column_type}, but expected {column_type}"
                    break

        return TestResult(name=self.name, description=description, status=status)


class TestColumnValueRegexp(BaseConditionsTest):
    group = "data_integrity"
    name = "Test count number of values in a column or in columns matched a regexp"
    metric: DataIntegrityValueByRegexpMetrics

    def __init__(
        self,
        column_name: Optional[Union[str, List[str]]] = None,
        reg_exp: Optional[str] = None,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[DataIntegrityValueByRegexpMetrics] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if (column_name is None or reg_exp is None) and metric is None:
            raise ValueError("Not enough parameters for the test")

        if metric is None:
            self.metric = DataIntegrityValueByRegexpMetrics(column_name=column_name, reg_exp=reg_exp)

        else:
            self.metric = metric

    def check(self):
        status = TestResult.SUCCESS
        description = "All match numbers are in conditions"
        matched_values = self.metric.get_result().matched_values

        for column_name, matched_number in matched_values.items():
            if not self.condition.check_value(matched_number):
                status = TestResult.FAIL
                description = f"Count of matched values for column {column_name} is {matched_number}"
                break

        return TestResult(name=self.name, description=description, status=status)
