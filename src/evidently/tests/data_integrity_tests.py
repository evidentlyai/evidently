from abc import ABC
from typing import List
from typing import Dict
from typing import Tuple
from typing import Optional
from typing import Union

import dataclasses
from pandas.core.dtypes.common import infer_dtype_from_object

from evidently.model.widget import BaseWidgetInfo
from evidently.metrics.data_integrity_metrics import DataIntegrityMetrics
from evidently.metrics.data_integrity_metrics import DataIntegrityValueByRegexpMetrics
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.base_renderer import DetailsInfo
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import BaseConditionsTest
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import plot_dicts_to_table
from evidently.tests.utils import approx
from evidently.tests.utils import Numeric


class BaseIntegrityValueTest(BaseCheckValueTest, ABC):
    group = "data_integrity"
    data_integrity_metric: DataIntegrityMetrics

    def __init__(
        self,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        data_integrity_metric: Optional[DataIntegrityMetrics] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric


class TestNumberOfColumns(BaseIntegrityValueTest):
    """Number of all columns in the data, including utility columns (id/index, datetime, target, predictions)"""

    name = "Number of Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            return TestValueCondition(eq=reference_stats.number_of_columns)

        return TestValueCondition(gt=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_columns

    def get_description(self, value: Numeric) -> str:
        return f"The number of columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(test_type=TestNumberOfColumns)
class TestNumberOfColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_columns"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current dtype"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.columns_type
        dict_ref = None
        reference_stats = obj.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            dict_ref = reference_stats.columns_type
            columns = columns + ["reference dtype"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_column", "diff")
        info.details = additional_plots
        return info


class TestNumberOfRows(BaseIntegrityValueTest):
    """Number of rows in the data"""

    name = "Number of Rows"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            return TestValueCondition(eq=approx(reference_stats.number_of_rows, relative=0.1))

        return TestValueCondition(gt=30)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_rows

    def get_description(self, value: Numeric) -> str:
        return f"The number of rows is {value}. The test threshold is {self.get_condition()}."


@default_renderer(test_type=TestNumberOfRows)
class TestNumberOfRowsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfRows) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_rows"] = obj.value
        return base


class TestNumberOfNANs(BaseIntegrityValueTest):
    """Number of NAN values in the data without aggregation by rows or columns"""

    name = "Test Number of NAN Values"

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_nans

    def get_description(self, value: Numeric) -> str:
        return f"Number of NANs is {value}"


@default_renderer(test_type=TestNumberOfNANs)
class TestNumberOfNANsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfNANs) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        dict_ref = {}
        reference_stats = obj.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            dict_ref = reference_stats.nans_by_columns
            columns = columns + ["reference number of NaNs"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_nans")
        info.details = additional_plots
        return info


class TestNumberOfColumnsWithNANs(BaseIntegrityValueTest):
    """Number of columns contained at least one NAN value"""

    name = "Test Number Of Columns With Nulls"

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_columns_with_nans

    def get_description(self, value: Numeric) -> str:
        return f"Number of columns with NANs is {value}"


@default_renderer(test_type=TestNumberOfColumnsWithNANs)
class TestNumberOfColumnsWithNANsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfColumnsWithNANs) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        dict_ref = {}
        reference_stats = obj.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            dict_ref = reference_stats.nans_by_columns
            columns = columns + ["reference number of NaNs"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_cols_with_nans")
        info.details = additional_plots
        return info


class TestNumberOfRowsWithNANs(BaseIntegrityValueTest):
    """Number of rows contained at least one NAN value"""

    name = "Test Number Of Rows With NANs"

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_rows_with_nans

    def get_description(self, value: Numeric) -> str:
        return f"Number of rows with NANs is {value}"


class TestNumberOfConstantColumns(BaseIntegrityValueTest):
    """Number of columns contained only one unique value"""

    name = "Number of Constant Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            value = reference_stats.number_of_constant_columns
            return TestValueCondition(lte=value)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_constant_columns

    def get_description(self, value: Numeric) -> str:
        return f"The number of constant columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(test_type=TestNumberOfConstantColumns)
class TestNumberOfConstantColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfConstantColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.condition.as_dict()
        base["parameters"]["number_of_constant_columns"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfConstantColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current nunique"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.number_uniques_by_columns
        dict_ref = {}
        reference_stats = obj.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            dict_ref = reference_stats.number_uniques_by_columns
            columns = columns + ["reference nunique"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_cols_with_nans", "curr", True)
        info.details = additional_plots
        return info


class TestNumberOfEmptyRows(BaseIntegrityValueTest):
    """Number of rows contained all NAN values"""

    name = "Test Number Of Empty Rows"

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_empty_rows

    def get_description(self, value: Numeric) -> str:
        return f"Number of empty rows: {value}"


class TestNumberOfEmptyColumns(BaseIntegrityValueTest):
    """Number of columns contained all NAN values"""

    name = "Test Number Of Empty Columns"

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_empty_columns

    def get_description(self, value: Numeric) -> str:
        return f"Number of empty columns: {value}"


@default_renderer(test_type=TestNumberOfEmptyColumns)
class TestNumberOfEmptyColumnsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfEmptyColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        dict_ref = {}
        reference_stats = obj.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            dict_ref = reference_stats.nans_by_columns
            columns = columns + ["reference number of NaNs"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_empty_columns")
        info.details = additional_plots
        return info


class TestNumberOfDuplicatedRows(BaseIntegrityValueTest):
    """How many rows have duplicates in the dataset"""

    name = "Number of Duplicate Rows"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            ref_num_of_duplicates = reference_stats.number_of_duplicated_rows
            curr_number_of_rows = self.data_integrity_metric.get_result().current_stats.number_of_rows
            ref_number_of_rows = reference_stats.number_of_rows
            mult = curr_number_of_rows / ref_number_of_rows
            return TestValueCondition(eq=approx(ref_num_of_duplicates * mult, 0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_duplicated_rows

    def get_description(self, value: Numeric) -> str:
        return f"The number of duplicate rows is {value}. The test threshold is {self.get_condition()}."


@default_renderer(test_type=TestNumberOfDuplicatedRows)
class TestNumberOfDuplicatedRowsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDuplicatedRows) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_duplicated_rows"] = obj.value
        return base


class TestNumberOfDuplicatedColumns(BaseIntegrityValueTest):
    """How many columns have duplicates in the dataset"""

    name = "Number of Duplicate Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            value = reference_stats.number_of_duplicated_columns
            return TestValueCondition(lte=value)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current_stats.number_of_duplicated_columns

    def get_description(self, value: Numeric) -> str:
        return f"The number of duplicate columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(test_type=TestNumberOfDuplicatedColumns)
class TestNumberOfDuplicatedColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDuplicatedColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_duplicated_columns"] = obj.value
        return base


class BaseIntegrityByColumnsConditionTest(BaseCheckValueTest, ABC):
    group = "data_integrity"
    data_integrity_metric: DataIntegrityMetrics
    column_name: Optional[str]

    def __init__(
        self,
        column_name: Optional[str] = None,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
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

    name = "Share of NA Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference_stats

        if reference_stats is not None:
            ref_nans = reference_stats.nans_by_columns[self.column_name]
            ref_num_of_rows = reference_stats.number_of_rows
            return TestValueCondition(eq=approx(ref_nans / ref_num_of_rows, relative=0.1))

        return TestValueCondition(eq=approx(0))

    def calculate_value_for_test(self) -> Numeric:
        nans_by_columns = self.data_integrity_metric.get_result().current_stats.nans_by_columns
        number_of_rows = self.data_integrity_metric.get_result().current_stats.number_of_rows
        return nans_by_columns[self.column_name] / number_of_rows

    def get_description(self, value: Numeric) -> str:
        return (
            f"The share of NA values in {self.column_name} is {value:.3g}."
            f" The test threshold is {self.get_condition()}."
        )


@default_renderer(test_type=TestColumnNANShare)
class TestColumnNANShareRenderer(TestRenderer):
    def render_json(self, obj: TestColumnNANShare) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["nans_by_columns"] = obj.data_integrity_metric.get_result().current_stats.nans_by_columns
        base["parameters"]["number_of_rows"] = obj.data_integrity_metric.get_result().current_stats.number_of_rows
        base["parameters"]["share_of_nans"] = obj.value
        return base


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
    """This test compares columns type against the specified ones or a reference dataframe"""

    group = "data_integrity"
    name = "Column Types"
    columns_type: Optional[dict]
    data_integrity_metric: DataIntegrityMetrics

    @dataclasses.dataclass
    class Result(TestResult):
        columns_types: Dict[str, Tuple[str, str]]

    def __init__(
        self, columns_type: Optional[dict] = None, data_integrity_metric: Optional[DataIntegrityMetrics] = None
    ):
        self.columns_type = columns_type

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric

    def check(self):
        status = TestResult.SUCCESS
        data_columns_type = self.data_integrity_metric.get_result().current_stats.columns_type

        if self.columns_type is None:
            if self.data_integrity_metric.get_result().reference_stats is None:
                status = TestResult.ERROR
                description = "Cannot compare column types without conditions or a reference"
                return TestResult(name=self.name, description=description, status=status)

            # get types from reference
            columns_type = self.data_integrity_metric.get_result().reference_stats.columns_type

        else:
            columns_type = self.columns_type

            if not columns_type:
                status = TestResult.ERROR
                description = "Columns type condition is empty"
                return TestResult(name=self.name, description=description, status=status)

        invalid_types_count = 0
        columns_types = {}

        for column_name, expected_type_object in columns_type.items():
            real_column_type_object = data_columns_type.get(column_name)

            if real_column_type_object is None:
                status = TestResult.ERROR
                description = f"No column '{column_name}' in the metrics data"
                return TestResult(name=self.name, description=description, status=status)

            expected_type = infer_dtype_from_object(expected_type_object)
            real_column_type = infer_dtype_from_object(real_column_type_object)
            columns_types[column_name] = (real_column_type.__name__, expected_type.__name__)

            if expected_type == real_column_type or issubclass(real_column_type, expected_type):
                # types are matched or expected type is a parent
                continue

            status = TestResult.FAIL
            invalid_types_count += 1

        return self.Result(
            name=self.name,
            description=f"The number of columns with a type mismatch is {invalid_types_count} out of {len(columns_type)}.",
            status=status,
            columns_types=columns_types,
        )


@default_renderer(test_type=TestColumnsType)
class TestNumberOfDriftedFeaturesRenderer(TestRenderer):
    def render_json(self, obj: TestColumnsType) -> dict:
        base = super().render_json(obj)
        base["parameters"]["columns"] = [
            dict(
                column_name=column_name,
                actual_type=types[0],
                expected_type=types[1],
            )
            for column_name, types in obj.get_result().columns_types.items()
        ]
        return base

    def render_html(self, obj: TestColumnsType) -> TestHtmlInfo:
        info = super().render_html(obj)

        info.details = [
            DetailsInfo(
                id="drift_table",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={
                        "header": ["Column Name", "Actual Type", "Expected Type"],
                        "data": [
                            [column_name, *types] for column_name, types in obj.get_result().columns_types.items()
                        ],
                    },
                    size=2,
                ),
            ),
        ]
        return info


class TestColumnValueRegexp(BaseConditionsTest):
    group = "data_integrity"
    name = "Test count number of values in a column or in columns matched a regexp"
    metric: DataIntegrityValueByRegexpMetrics

    def __init__(
        self,
        column_name: Optional[Union[str, List[str]]] = None,
        reg_exp: Optional[str] = None,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        metric: Optional[DataIntegrityValueByRegexpMetrics] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if (column_name is None or reg_exp is None) and metric is None:
            raise ValueError("Not enough parameters for the test")

        if metric is None:
            if reg_exp is None:
                raise ValueError("Regexp should be present")

            if column_name is None:
                raise ValueError("Column name should be present")

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
