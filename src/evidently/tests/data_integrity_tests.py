from abc import ABC
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import infer_dtype_from_object

from evidently.metrics import ColumnRegExpMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import DataIntegrityMetrics
from evidently.metrics import DatasetMissingValuesMetric
from evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValues
from evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetricResult
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import DetailsInfo
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import GroupData
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import approx
from evidently.tests.utils import dataframes_to_table
from evidently.tests.utils import plot_dicts_to_table
from evidently.tests.utils import plot_value_counts_tables_ref_curr
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.generators import BaseGenerator
from evidently.utils.types import Numeric

DATA_INTEGRITY_GROUP = GroupData("data_integrity", "Data Integrity", "")
GroupingTypes.TestGroup.add_value(DATA_INTEGRITY_GROUP)


class BaseIntegrityValueTest(BaseCheckValueTest, ABC):
    group = DATA_INTEGRITY_GROUP.id
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
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            return TestValueCondition(eq=reference_stats.number_of_columns)

        return TestValueCondition(gt=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_columns

    def get_description(self, value: Numeric) -> str:
        return f"The number of columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfColumns)
class TestNumberOfColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_columns"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current dtype"]
        dict_curr = obj.data_integrity_metric.get_result().current.columns_type
        dict_ref = None
        reference_stats = obj.data_integrity_metric.get_result().reference

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
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            return TestValueCondition(eq=approx(reference_stats.number_of_rows, relative=0.1))

        return TestValueCondition(gt=30)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_rows

    def get_description(self, value: Numeric) -> str:
        return f"The number of rows is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfRows)
class TestNumberOfRowsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfRows) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_rows"] = obj.value
        return base


class BaseIntegrityNullValuesTest(BaseCheckValueTest, ABC):
    group = DATA_INTEGRITY_GROUP.id
    metric: DatasetMissingValuesMetric

    def __init__(
        self,
        null_values: Optional[list] = None,
        replace: bool = True,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        metric: Optional[DatasetMissingValuesMetric] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if metric is None:
            self.metric = DatasetMissingValuesMetric(values=null_values, replace=replace)

        else:
            self.metric = metric


class BaseTestNullValuesRenderer(TestRenderer):
    """Common class for tests of null-values.
    Some tests have the same details visualizations.
    """

    @staticmethod
    def _get_number_and_percents_of_nulls(nulls_info: DatasetMissingValues) -> pd.DataFrame:
        """Get a string with nulls numbers and percents from nulls info for results table"""
        result = {}

        for columns_name in nulls_info.number_of_nulls_by_column:
            nulls_count = nulls_info.number_of_nulls_by_column[columns_name]
            percent_count = nulls_info.share_of_nulls_by_column[columns_name] * 100
            result[columns_name] = f"{nulls_count} ({percent_count:.2f}%)"

        return pd.DataFrame.from_dict(
            {
                name: dict(
                    value=nulls_info.number_of_nulls_by_column[name],
                    display=f"{nulls_info.number_of_nulls_by_column[name]}"
                    f" ({nulls_info.share_of_nulls_by_column[name] * 100:.2f}%)",
                )
                for name in nulls_info.number_of_nulls_by_column.keys()
            },
            orient="index",
            columns=["value", "display"],
        )

    def get_table_with_nulls_and_percents_by_column(
        self, info: TestHtmlInfo, metric_result: DatasetMissingValuesMetricResult, name: str
    ) -> TestHtmlInfo:
        """Get a table with nulls number and percents"""
        columns = ["column name", "current number of nulls"]
        dict_curr = self._get_number_and_percents_of_nulls(metric_result.current)
        dict_ref = None
        reference_stats = metric_result.reference

        if reference_stats is not None:
            # add one more column and values for reference data
            columns.append("reference number of nulls")
            dict_ref = self._get_number_and_percents_of_nulls(reference_stats)

        additional_plots = dataframes_to_table(dict_curr, dict_ref, columns, name)
        info.details = additional_plots
        return info

    @staticmethod
    def _replace_null_values_to_description(nulls: dict) -> dict:
        """Replace null values in the dict keys to human-readable string"""
        nulls_naming_mapping = {
            None: "Pandas nulls (None, NAN, etc.)",
            "": '"" (empty string)',
            np.inf: 'Numpy "inf" value',
            -np.inf: 'Numpy "-inf" value',
        }
        return {nulls_naming_mapping.get(k, k): v for k, v in nulls.items()}

    def get_table_with_number_of_nulls_by_null_values(
        self, info: TestHtmlInfo, current_nulls: dict, reference_nulls: Optional[dict], name: str
    ) -> TestHtmlInfo:
        columns = ["null", "current number of nulls"]
        dict_curr = self._replace_null_values_to_description(current_nulls)
        dict_ref: Optional[dict] = None

        if reference_nulls is not None:
            # add one more column and values for reference data
            columns.append("reference number of nulls")
            # cast keys to str because None could be in keys and it is not processed correctly in visual tables
            dict_ref = self._replace_null_values_to_description(reference_nulls)

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, name)
        info.details = additional_plots
        return info


class TestNumberOfDifferentNulls(BaseIntegrityNullValuesTest):
    """Check a number of different encoded nulls."""

    name = "Different Types of Nulls and Missing Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_null_values = self.metric.get_result().reference

        if reference_null_values is not None:
            return TestValueCondition(eq=reference_null_values.number_of_different_nulls)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_of_different_nulls

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of differently encoded types of nulls and missing values is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestNumberOfDifferentNulls)
class TestNumberOfDifferentNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestNumberOfDifferentNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_different_nulls"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfDifferentNulls) -> TestHtmlInfo:
        """Get a table with a null value and number of the value in the dataset"""
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        current_nulls = metric_result.current.different_nulls

        if metric_result.reference is None:
            reference_nulls = None

        else:
            reference_nulls = metric_result.reference.different_nulls

        return self.get_table_with_number_of_nulls_by_null_values(
            info, current_nulls, reference_nulls, "number_of_different_nulls"
        )


class TestNumberOfNulls(BaseIntegrityNullValuesTest):
    """Check a number of null values."""

    name = "The Number of Nulls"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_null_values = self.metric.get_result().reference

        if reference_null_values is not None:
            curr_number_of_rows = self.metric.get_result().current.number_of_rows
            ref_number_of_rows = reference_null_values.number_of_rows
            mult = curr_number_of_rows / ref_number_of_rows
            return TestValueCondition(lte=approx(reference_null_values.number_of_missed_values * mult, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_of_missed_values

    def get_description(self, value: Numeric) -> str:
        return f"The number of nulls and missing values is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfNulls)
class TestNumberOfNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestNumberOfNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_nulls"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfNulls) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        return self.get_table_with_nulls_and_percents_by_column(info, metric_result, "number_of_nulls")


class TestShareOfNulls(BaseIntegrityNullValuesTest):
    """Check a share of null values."""

    name = "Share of Nulls"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            return TestValueCondition(lte=approx(reference.share_of_missed_values, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.share_of_missed_values

    def get_description(self, value: Numeric) -> str:
        return f"The share of nulls and missing values is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestShareOfNulls)
class TestShareOfNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestShareOfNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["share_of_nulls"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfNulls) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        return self.get_table_with_nulls_and_percents_by_column(info, metric_result, "share_of_nulls")


class TestNumberOfColumnsWithNulls(BaseIntegrityNullValuesTest):
    """Check a number of columns with a null value."""

    name = "The Number of Columns With Nulls"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            return TestValueCondition(lte=reference.number_of_columns_with_nulls)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_of_columns_with_nulls

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of columns with nulls and missing values is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestNumberOfColumnsWithNulls)
class TestNumberOfColumnsWithNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestNumberOfColumnsWithNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_columns_with_nulls"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfNulls) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        return self.get_table_with_nulls_and_percents_by_column(info, metric_result, "number_of_columns_with_nulls")


class TestShareOfColumnsWithNulls(BaseIntegrityNullValuesTest):
    """Check a share of columns with a null value."""

    name = "The Share of Columns With Nulls"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            return TestValueCondition(lte=reference.share_of_columns_with_nulls)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.share_of_columns_with_nulls

    def get_description(self, value: Numeric) -> str:
        return (
            f"The share of columns with nulls and missing values is {value:.3g}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestShareOfColumnsWithNulls)
class TestShareOfColumnsWithNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestShareOfColumnsWithNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["share_of_columns_with_nulls"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfNulls) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        return self.get_table_with_nulls_and_percents_by_column(info, metric_result, "share_of_columns_with_nulls")


class TestNumberOfRowsWithNulls(BaseIntegrityNullValuesTest):
    """Check a number of rows with a null value."""

    name = "The Number Of Rows With Nulls"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            curr_number_of_rows = self.metric.get_result().current.number_of_rows
            ref_number_of_rows = reference.number_of_rows
            mult = curr_number_of_rows / ref_number_of_rows
            return TestValueCondition(lte=approx(reference.number_of_rows_with_nulls * mult, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_of_rows_with_nulls

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of rows with nulls and missing values is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestNumberOfRowsWithNulls)
class TestNumberOfRowsWithNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestNumberOfRowsWithNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_rows_with_nulls"] = obj.value
        return base


class TestShareOfRowsWithNulls(BaseIntegrityNullValuesTest):
    """Check a share of rows with a null value."""

    name = "The Share of Rows With Nulls"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            return TestValueCondition(lte=approx(reference.share_of_rows_with_nulls, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.share_of_rows_with_nulls

    def get_description(self, value: Numeric) -> str:
        return (
            f"The share of rows with nulls and missing values is {value:.3g}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestShareOfRowsWithNulls)
class TestShareOfRowsWithNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestShareOfRowsWithNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["share_of_rows_with_nulls"] = obj.value
        return base


class BaseIntegrityColumnNullValuesTest(BaseCheckValueTest, ABC):
    group = DATA_INTEGRITY_GROUP.id
    metric: DatasetMissingValuesMetric
    column_name: str

    def __init__(
        self,
        column_name: str,
        null_values: Optional[list] = None,
        replace: bool = True,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        metric: Optional[DatasetMissingValuesMetric] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.column_name = column_name

        if metric is None:
            self.metric = DatasetMissingValuesMetric(values=null_values, replace=replace)

        else:
            self.metric = metric


class TestColumnNumberOfDifferentNulls(BaseIntegrityColumnNullValuesTest):
    """Check a number of differently encoded empty/null values in one column."""

    name = "Different Types of Nulls and Missing Values in a Column"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_null_values = self.metric.get_result().reference

        if reference_null_values is not None:
            if self.column_name not in reference_null_values.number_of_different_nulls_by_column:
                raise ValueError(
                    f"Cannot define test default conditions: no column '{self.column_name}' in reference dataset."
                )

            ref_value = reference_null_values.number_of_different_nulls_by_column[self.column_name]
            return TestValueCondition(lte=ref_value)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        metric_data = self.metric.get_result().current
        return metric_data.number_of_different_nulls_by_column[self.column_name]

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of differently encoded types of nulls and missing values in the column **{self.column_name}** "
            f"is {value}. The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestColumnNumberOfDifferentNulls)
class TestColumnNumberOfDifferentNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestColumnNumberOfDifferentNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_different_nulls"] = obj.value
        base["parameters"]["column_name"] = obj.column_name
        return base

    def render_html(self, obj: TestColumnNumberOfDifferentNulls) -> TestHtmlInfo:
        """Get a table with a null value and number of the value in the dataset"""
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        current_nulls = metric_result.current.different_nulls_by_column[obj.column_name]

        if metric_result.reference is None:
            reference_nulls = None

        else:
            reference_nulls = metric_result.reference.different_nulls_by_column[obj.column_name]

        return self.get_table_with_number_of_nulls_by_null_values(
            info, current_nulls, reference_nulls, "number_of_different_nulls"
        )


class TestColumnNumberOfNulls(BaseIntegrityColumnNullValuesTest):
    """Check a number of empty/null values in one column."""

    name = "The Number of Nulls in a Column"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_null_values = self.metric.get_result().reference

        if reference_null_values is not None:
            curr_number_of_rows = self.metric.get_result().current.number_of_rows
            ref_number_of_rows = reference_null_values.number_of_rows
            mult = curr_number_of_rows / ref_number_of_rows
            ref_value = reference_null_values.number_of_nulls_by_column[self.column_name]
            return TestValueCondition(lte=approx(ref_value * mult, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_of_nulls_by_column[self.column_name]

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of nulls and missing values in the column **{self.column_name}** is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestColumnNumberOfNulls)
class TestColumnNumberOfNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestColumnNumberOfNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_null_values"] = obj.value
        base["parameters"]["column_name"] = obj.column_name
        return base


class TestColumnShareOfNulls(BaseIntegrityColumnNullValuesTest):
    """Check a share of empty/null values in one column."""

    name = "The Share of Nulls in a Column"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            ref_value = reference.share_of_nulls_by_column[self.column_name]
            return TestValueCondition(lte=approx(ref_value, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.share_of_nulls_by_column[self.column_name]

    def get_description(self, value: Numeric) -> str:
        return (
            f"The share of nulls and missing values in the column **{self.column_name}** is {value:.3g}. "
            f"The test threshold is {self.get_condition()}."
        )


class TestAllColumnsShareOfNulls(BaseGenerator):
    def generate(self, columns_info: DatasetColumns) -> List[TestColumnShareOfNulls]:
        return [TestColumnShareOfNulls(column_name=name) for name in columns_info.get_all_columns_list()]


@default_renderer(wrap_type=TestColumnShareOfNulls)
class TestColumnShareOfNullsRenderer(BaseTestNullValuesRenderer):
    def render_json(self, obj: TestColumnShareOfNulls) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["share_of_null_values"] = obj.value
        base["parameters"]["column_name"] = obj.column_name
        return base


class TestNumberOfConstantColumns(BaseIntegrityValueTest):
    """Number of columns contained only one unique value"""

    name = "Number of Constant Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            value = reference_stats.number_of_constant_columns
            return TestValueCondition(lte=value)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_constant_columns

    def get_description(self, value: Numeric) -> str:
        return f"The number of constant columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfConstantColumns)
class TestNumberOfConstantColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfConstantColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_constant_columns"] = obj.value
        return base

    def render_html(self, obj: TestNumberOfConstantColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current nunique"]
        dict_curr = obj.data_integrity_metric.get_result().current.number_uniques_by_columns
        dict_ref = {}
        reference_stats = obj.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            dict_ref = reference_stats.number_uniques_by_columns
            columns = columns + ["reference nunique"]

        additional_plots = plot_dicts_to_table(dict_curr, dict_ref, columns, "number_of_constant_cols", "curr", True)
        info.details = additional_plots
        return info


class TestNumberOfEmptyRows(BaseIntegrityValueTest):
    """Number of rows contained all NAN values"""

    name = "Number of Empty Rows"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            ref_number_of_empty_rows = reference_stats.number_of_empty_rows
            curr_number_of_rows = self.data_integrity_metric.get_result().current.number_of_rows
            ref_number_of_rows = reference_stats.number_of_rows
            mult = curr_number_of_rows / ref_number_of_rows
            return TestValueCondition(eq=approx(ref_number_of_empty_rows * mult, 0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_empty_rows

    def get_description(self, value: Numeric) -> str:
        return f"Number of Empty Rows is {value}. The test threshold is {self.get_condition()}."


class TestNumberOfEmptyColumns(BaseIntegrityValueTest):
    """Number of columns contained all NAN values"""

    name = "Number of Empty Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            return TestValueCondition(lte=reference_stats.number_of_empty_columns)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_empty_columns

    def get_description(self, value: Numeric) -> str:
        return f"Number of Empty Columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfEmptyColumns)
class TestNumberOfEmptyColumnsRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfEmptyColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        columns = ["column name", "current number of NaNs"]
        dict_curr = obj.data_integrity_metric.get_result().current.nans_by_columns
        dict_ref = {}
        reference_stats = obj.data_integrity_metric.get_result().reference

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
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            ref_num_of_duplicates = reference_stats.number_of_duplicated_rows
            curr_number_of_rows = self.data_integrity_metric.get_result().current.number_of_rows
            ref_number_of_rows = reference_stats.number_of_rows
            mult = curr_number_of_rows / ref_number_of_rows
            return TestValueCondition(eq=approx(ref_num_of_duplicates * mult, 0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_duplicated_rows

    def get_description(self, value: Numeric) -> str:
        return f"The number of duplicate rows is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfDuplicatedRows)
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
        if self.condition.has_condition():
            return self.condition

        reference_stats = self.data_integrity_metric.get_result().reference

        if reference_stats is not None:
            value = reference_stats.number_of_duplicated_columns
            return TestValueCondition(lte=value)

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.data_integrity_metric.get_result().current.number_of_duplicated_columns

    def get_description(self, value: Numeric) -> str:
        return f"The number of duplicate columns is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestNumberOfDuplicatedColumns)
class TestNumberOfDuplicatedColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestNumberOfDuplicatedColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["number_of_duplicated_columns"] = obj.value
        return base


class BaseIntegrityByColumnsConditionTest(BaseCheckValueTest, ABC):
    group = DATA_INTEGRITY_GROUP.id
    data_integrity_metric: DataIntegrityMetrics

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

    def groups(self) -> Dict[str, str]:
        if self.column_name is not None:
            return {GroupingTypes.ByFeature.id: self.column_name}
        return {}


class BaseIntegrityOneColumnTest(Test, ABC):
    group = DATA_INTEGRITY_GROUP.id
    data_integrity_metric: ColumnSummaryMetric
    column_name: str

    def __init__(self, column_name: str, data_integrity_metric: Optional[ColumnSummaryMetric] = None):
        self.column_name = column_name

        if data_integrity_metric is None:
            self.data_integrity_metric = ColumnSummaryMetric(column_name)

        else:
            self.data_integrity_metric = data_integrity_metric

    def groups(self) -> Dict[str, str]:
        return {GroupingTypes.ByFeature.id: self.column_name}


class TestColumnAllConstantValues(BaseIntegrityOneColumnTest):
    """Test that there is only one unique value in a column"""

    name = "All Constant Values in a Column"
    data_integrity_metric: ColumnSummaryMetric

    def check(self):
        uniques_in_column = self.data_integrity_metric.get_result().current_characteristics.unique
        number_of_rows = self.data_integrity_metric.get_result().current_characteristics.number_of_rows
        column_name = self.column_name

        description = (
            f"The number of the unique values in the column **{column_name}** "
            f"is {uniques_in_column} out of {number_of_rows}"
        )

        if uniques_in_column <= 1:
            status = TestResult.FAIL

        else:
            status = TestResult.SUCCESS

        return TestResult(name=self.name, description=description, status=status, groups=self.groups())


@default_renderer(wrap_type=TestColumnAllConstantValues)
class TestColumnAllConstantValuesRenderer(TestRenderer):
    def render_html(self, obj: TestColumnAllConstantValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        counts_data = obj.data_integrity_metric.get_result().plot_data.counts_of_values
        if counts_data is not None:
            curr_df = counts_data["current"]
            ref_df = None
            if "reference" in counts_data.keys():
                ref_df = counts_data["reference"]
            additional_plots = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, "AllConstantValues")
            info.details = additional_plots
        return info


class TestColumnAllUniqueValues(BaseIntegrityOneColumnTest):
    """Test that there is only uniques values in a column"""

    name = "All Unique Values in a Column"

    def check(self):
        uniques_in_column = self.data_integrity_metric.get_result().current_characteristics.unique
        number_of_rows = self.data_integrity_metric.get_result().current_characteristics.number_of_rows
        nans_in_column = self.data_integrity_metric.get_result().current_characteristics.missing
        column_name = self.column_name

        description = (
            f"The number of the unique values in the column **{column_name}** "
            f"is {uniques_in_column}  out of {number_of_rows}"
        )

        if uniques_in_column != number_of_rows - nans_in_column:
            status = TestResult.FAIL

        else:
            status = TestResult.SUCCESS

        return TestResult(name=self.name, description=description, status=status, groups=self.groups())


@default_renderer(wrap_type=TestColumnAllUniqueValues)
class TestColumnAllUniqueValuesRenderer(TestRenderer):
    def render_html(self, obj: TestColumnAllUniqueValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        counts_data = obj.data_integrity_metric.get_result().plot_data.counts_of_values
        if counts_data is not None:
            curr_df = counts_data["current"]
            ref_df = None
            if "reference" in counts_data.keys():
                ref_df = counts_data["reference"]
            additional_plots = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, "AllUniqueValues")
            info.details = additional_plots
        return info


class TestColumnsType(Test):
    """This test compares columns type against the specified ones or a reference dataframe"""

    group = DATA_INTEGRITY_GROUP.id
    name = "Column Types"
    columns_type: Optional[dict]
    data_integrity_metric: DataIntegrityMetrics

    @dataclasses.dataclass
    class Result(TestResult):
        columns_types: Dict[str, Tuple[str, str]] = dataclasses.field(default_factory=dict)

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
        data_columns_type = self.data_integrity_metric.get_result().current.columns_type

        if self.columns_type is None:
            if self.data_integrity_metric.get_result().reference is None:
                status = TestResult.ERROR
                description = "Cannot compare column types without conditions or a reference"
                return TestResult(name=self.name, description=description, status=status)

            # get types from reference
            columns_type = self.data_integrity_metric.get_result().reference.columns_type

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
            description=f"The number of columns with a type "
            f"mismatch is {invalid_types_count} out of {len(columns_type)}.",
            status=status,
            columns_types=columns_types,
        )


@default_renderer(wrap_type=TestColumnsType)
class TestColumnsTypeRenderer(TestRenderer):
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


class TestColumnValueRegExp(BaseCheckValueTest, ABC):
    group = DATA_INTEGRITY_GROUP.id
    name = "RegExp Match"
    metric: ColumnRegExpMetric
    column_name: Optional[str]

    def __init__(
        self,
        column_name: Optional[str] = None,
        reg_exp: Optional[str] = None,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        metric: Optional[ColumnRegExpMetric] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.column_name = column_name

        if (column_name is None or reg_exp is None) and metric is None:
            raise ValueError("Not enough parameters for the test")

        if metric is None:
            if reg_exp is None:
                raise ValueError("Regexp should be present")

            if column_name is None:
                raise ValueError("Column name should be present")

            self.metric = ColumnRegExpMetric(column_name=column_name, reg_exp=reg_exp)

        else:
            self.metric = metric

    def groups(self) -> Dict[str, str]:
        if self.column_name is not None:
            return {GroupingTypes.ByFeature.id: self.column_name}
        return {}

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        metric_result = self.metric.get_result()

        if metric_result.reference:
            ref_value = metric_result.reference.number_of_not_matched
            mult = metric_result.current.number_of_rows / metric_result.reference.number_of_rows

            if mult is not None:
                return TestValueCondition(eq=approx(ref_value * mult, relative=0.1))

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        return self.metric.get_result().current.number_of_not_matched

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of the mismatched values in the column **{self.column_name}** is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestColumnValueRegExp)
class TestColumnValueRegExpRenderer(TestRenderer):
    def render_html(self, obj: TestColumnValueRegExp) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        metric_result = obj.metric.get_result()

        if metric_result.current.table_of_not_matched:
            curr_df = pd.DataFrame(metric_result.current.table_of_not_matched.items())
            curr_df.columns = ["x", "count"]

        else:
            curr_df = pd.DataFrame(columns=["x", "count"])

        ref_df = None

        if metric_result.reference is not None and metric_result.reference.table_of_not_matched:
            ref_df = pd.DataFrame(metric_result.reference.table_of_not_matched.items())
            ref_df.columns = ["x", "count"]

        additional_plots = plot_value_counts_tables_ref_curr(
            column_name, curr_df, ref_df, f"{column_name}_ColumnValueRegExp"
        )
        info.details = additional_plots
        return info
