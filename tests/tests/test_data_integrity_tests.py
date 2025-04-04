import json
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestColumnAllConstantValues
from evidently.legacy.tests import TestColumnAllUniqueValues
from evidently.legacy.tests import TestColumnNumberOfDifferentMissingValues
from evidently.legacy.tests import TestColumnNumberOfMissingValues
from evidently.legacy.tests import TestColumnRegExp
from evidently.legacy.tests import TestColumnShareOfMissingValues
from evidently.legacy.tests import TestColumnsType
from evidently.legacy.tests import TestNumberOfColumns
from evidently.legacy.tests import TestNumberOfColumnsWithMissingValues
from evidently.legacy.tests import TestNumberOfConstantColumns
from evidently.legacy.tests import TestNumberOfDifferentMissingValues
from evidently.legacy.tests import TestNumberOfDuplicatedColumns
from evidently.legacy.tests import TestNumberOfDuplicatedRows
from evidently.legacy.tests import TestNumberOfEmptyColumns
from evidently.legacy.tests import TestNumberOfEmptyRows
from evidently.legacy.tests import TestNumberOfMissingValues
from evidently.legacy.tests import TestNumberOfRows
from evidently.legacy.tests import TestNumberOfRowsWithMissingValues
from evidently.legacy.tests import TestShareOfColumnsWithMissingValues
from evidently.legacy.tests import TestShareOfMissingValues
from evidently.legacy.tests import TestShareOfRowsWithMissingValues


def test_data_integrity_test_number_of_columns() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfColumns()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestNumberOfColumns(gte=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfColumns(eq=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_number_of_columns_json_render() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 3], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite
    json_str = suite.json()
    json_result = json.loads(json_str)
    assert json_result["tests"][0] == {
        "description": "The number of columns is 3. The test threshold is eq=3.",
        "group": "data_integrity",
        "name": "Number of Columns",
        "parameters": {
            "condition": {"eq": 3},
            "value": 3,
        },
        "status": "SUCCESS",
    }

    suite = TestSuite(tests=[TestNumberOfColumns(lt=5)])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite
    json_str = suite.json()
    json_result = json.loads(json_str)
    assert json_result["tests"][0] == {
        "description": "The number of columns is 3. The test threshold is lt=5.",
        "group": "data_integrity",
        "name": "Number of Columns",
        "parameters": {
            "condition": {"lt": 5},
            "value": 3,
        },
        "status": "SUCCESS",
    }


def test_data_integrity_test_number_of_rows() -> None:
    test_dataset = pd.DataFrame({"target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestNumberOfRows()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestNumberOfRows(is_in=[10, 3, 50])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfRows(is_in=[10, 3, 50, 4])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestNumberOfRows(gte=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_number_of_rows_json_report() -> None:
    test_dataset = pd.DataFrame({"target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestNumberOfRows()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite
    json_str = suite.json()
    json_result = json.loads(json_str)
    assert json_result["tests"][0] == {
        "description": "The number of rows is 4. The test threshold is eq=4 ± 0.4.",
        "group": "data_integrity",
        "name": "Number of Rows",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 4}}, "value": 4},
        "status": "SUCCESS",
    }


@pytest.mark.parametrize(
    "test_dataset, conditions, result",
    (
        (pd.DataFrame({"target": [0, 0, 0, 1]}), {"eq": 0}, True),
        (pd.DataFrame({"target": [0, 0, None, 1], "numeric": [None, None, None, 1]}), {"lt": 3}, False),
    ),
)
def test_data_integrity_test_number_of_missing_values_no_errors(
    test_dataset: pd.DataFrame, conditions: dict, result: bool
) -> None:
    suite = TestSuite(tests=[TestNumberOfMissingValues(**conditions)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert bool(suite) is result
    assert suite.show()
    assert suite.json()


@pytest.mark.parametrize(
    "test_dataset, conditions, result",
    (
        (pd.DataFrame({"target": [0, 0, 0, 5]}), {"eq": 0}, True),
        (pd.DataFrame({"target": ["", "0", None, "1"], "numeric": [np.inf, None, -np.inf, 1]}), {"lt": 3}, False),
    ),
)
def test_data_integrity_test_number_of_different_missing_values(
    test_dataset: pd.DataFrame, conditions: dict, result: bool
) -> None:
    suite = TestSuite(tests=[TestNumberOfDifferentMissingValues(**conditions)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert bool(suite) is result


def test_data_integrity_test_missing_values_with_different_metrics() -> None:
    test_dataframe = pd.DataFrame({"target": [None, 0, 0, ""]})
    suite = TestSuite(
        tests=[
            TestNumberOfDifferentMissingValues(missing_values=[0], replace=True, eq=1),
            TestNumberOfDifferentMissingValues(missing_values=[0], replace=False, eq=3),
        ]
    )
    suite.run(current_data=test_dataframe, reference_data=None)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_number_of_columns_with_missing_values() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 2, None, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfColumnsWithMissingValues(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfColumnsWithMissingValues(eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_share_of_columns_with_missing_values() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 2, None, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestShareOfColumnsWithMissingValues(lte=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfColumnsWithMissingValues(eq=2 / 3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_number_of_rows_with_missing_values() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 2, None, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfRowsWithMissingValues(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfRowsWithMissingValues(eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_share_of_rows_with_missing_values() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 2, None, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestShareOfRowsWithMissingValues(gt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfRowsWithMissingValues(eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_constant_columns() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 0, 0, 0], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfConstantColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    suite = TestSuite(tests=[TestNumberOfConstantColumns(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfConstantColumns(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_constant_columns_json_render() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 0, 0, 0], "target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestNumberOfConstantColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The number of constant columns is 1. The test threshold is " "lte=1.",
        "group": "data_integrity",
        "name": "Number of Constant Columns",
        "parameters": {"condition": {"lte": 1}, "value": 1},
        "status": "SUCCESS",
    }


def test_data_integrity_test_empty_rows() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": [None, "d", "p", None],
            "numerical_feature": [None, 0, None, None],
            "target": [None, 0, None, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfEmptyRows(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfEmptyRows(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_empty_columns() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": [None, "d", "p", None],
            "numerical_feature": [None, None, None, None],
            "target": [None, 0, None, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfEmptyColumns(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfEmptyColumns(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_duplicated_rows() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "1", "p", None],
            "numerical_feature": ["1", "1", "1", "1"],
            "target": ["1", "1", "1", "1"],
        }
    )
    suite = TestSuite(tests=[TestNumberOfDuplicatedRows()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestNumberOfDuplicatedRows(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfDuplicatedRows(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_duplicated_rows_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "1", "1", "1"],
            "numerical_feature": ["1", "1", "1", "1"],
            "target": ["1", "1", "1", "1"],
        }
    )
    suite = TestSuite(tests=[TestNumberOfDuplicatedRows()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The number of duplicate rows is 3. The test threshold is eq=3 ± 0.3.",
        "group": "data_integrity",
        "name": "Number of Duplicate Rows",
        "parameters": {
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 3.0}},
            "value": 3,
        },
        "status": "SUCCESS",
    }


def test_data_integrity_test_duplicated_columns() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": ["1", "1", "1", "1"], "target": ["1", "1", "1", "1"]})

    suite = TestSuite(tests=[TestNumberOfDuplicatedColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestNumberOfDuplicatedColumns(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfDuplicatedColumns(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_duplicated_columns_json_render() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [1, 1, 1, 1], "target": [1, 1, 1, 1]})
    suite = TestSuite(tests=[TestNumberOfDuplicatedColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The number of duplicate columns is 1. The test threshold is lte=1.",
        "group": "data_integrity",
        "name": "Number of Duplicate Columns",
        "parameters": {"condition": {"lte": 1}, "value": 1},
        "status": "SUCCESS",
    }


def test_data_integrity_test_columns_type() -> None:
    current_dataset = pd.DataFrame(
        {
            "numerical_feature": [1, 2, 3],
            "target": ["1", "1", "1"],
            "datetime": [datetime.now(), datetime.now(), datetime.now()],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "numerical_feature": [1.0, 2.4, 3.0],
            "target": [True, False, True],
            "datetime": [datetime.now(), datetime.now(), datetime.now()],
        }
    )
    suite = TestSuite(tests=[TestColumnsType()])
    suite.run(current_data=current_dataset, reference_data=current_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestColumnsType()])
    suite.run(current_data=current_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnsType(columns_type={})])
    suite.run(current_data=current_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnsType(columns_type={"not_exists": "int64"})])
    suite.run(current_data=current_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(
        tests=[
            TestColumnsType(columns_type={"numerical_feature": np.float64, "target": "bool", "datetime": "datetime"})
        ]
    )
    suite.run(current_data=reference_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestColumnsType(columns_type={"numerical_feature": "number"})])
    suite.run(current_data=current_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


numpy_bool_type_name = np.bool_.__name__


def test_data_integrity_test_columns_type_to_json() -> None:
    current_dataset = pd.DataFrame({"numerical_feature": [1, 2, 3], "my_target": [True, False, True]})
    suite = TestSuite(tests=[TestColumnsType()])
    suite.run(
        current_data=current_dataset, reference_data=current_dataset, column_mapping=ColumnMapping(target="my_target")
    )
    suite._inner_suite.raise_for_error()
    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The number of columns with a type mismatch is 0 out of 2.",
        "group": "data_integrity",
        "name": "Column Types",
        "parameters": {
            "columns": [
                {"actual_type": "int64", "column_name": "numerical_feature", "expected_type": "int64"},
                {
                    "actual_type": numpy_bool_type_name,
                    "column_name": "my_target",
                    "expected_type": numpy_bool_type_name,
                },
            ]
        },
        "status": "SUCCESS",
    }


def test_data_integrity_test_columns_null_share() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 2, np.nan], "feature2": [1, 2, np.nan], "target": ["1", "1", "1"]})

    suite = TestSuite(tests=[TestColumnShareOfMissingValues(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestColumnShareOfMissingValues(column_name="feature1", lt=0.1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnShareOfMissingValues(column_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_columns_null_share_json_render() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 2, np.nan, 4], "feature2": [1, 2, np.nan, 1]})

    suite = TestSuite(tests=[TestColumnShareOfMissingValues(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The share of missing values in the column **feature1** is 0.25. "
        "The test threshold is lte=0.25 ± 0.025.",
        "group": "data_integrity",
        "name": "The Share of Missing Values in a Column",
        "parameters": {
            "column_name": "feature1",
            "condition": {"lte": {"absolute": 1e-12, "relative": 0.1, "value": 0.25}},
            "value": 0.25,
        },
        "status": "SUCCESS",
    }


def test_data_integrity_test_columns_all_constant_values() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 1, np.nan], "feature2": [1, 2, np.nan], "target": ["1", "1", "1"]})

    suite = TestSuite(tests=[TestColumnAllConstantValues(column_name="not_exists_feature")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnAllConstantValues(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_all_unique_values() -> None:
    test_dataset = pd.DataFrame(
        {"feature1": [1, 1, 2, 3], "feature2": [1, 2, np.nan, 4], "target": ["1", "2", "3", ""]}
    )

    suite = TestSuite(tests=[TestColumnAllUniqueValues(column_name="not_exists_feature")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnAllUniqueValues(column_name="feature2")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_column_values_match_regexp() -> None:
    test_dataset = pd.DataFrame({"feature1": ["a", "aa", "baa"], "feature2": ["b", "bb", "baa"], "target": [1, 2, 3]})
    suite = TestSuite(tests=[TestColumnRegExp(column_name="feature1", reg_exp=r"a.*", eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestColumnRegExp(column_name="feature2", reg_exp=r"b.*")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_number_of_missing_values() -> None:
    test_dataset = pd.DataFrame({"feature1": ["n/a", "b", "a"], "feature2": ["b", "", None]})

    suite = TestSuite(tests=[TestNumberOfMissingValues()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestNumberOfMissingValues(lt=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestNumberOfMissingValues(missing_values=["", "n/a", None], replace=True, lt=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite


def test_data_integrity_test_share_of_missing_values() -> None:
    test_dataset = pd.DataFrame({"feature1": ["", None, "None", "a"], "feature2": ["b", "None", None, None]})

    suite = TestSuite(tests=[TestShareOfMissingValues()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestShareOfMissingValues(lt=0.9)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestShareOfMissingValues(missing_values=["", "None"], lt=0.4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestShareOfMissingValues(missing_values=["", "None", False, None], replace=True, lt=0.4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite


def test_data_integrity_test_different_missing_values_one_column() -> None:
    test_dataset = pd.DataFrame({"feature1": ["n/a", "b", "a"], "feature2": ["b", "", None]})

    suite = TestSuite(tests=[TestColumnNumberOfDifferentMissingValues(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_integrity_test_different_missing_values_one_column_no_missing_values() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 2, 3], "feature2": ["b", "", None]})

    suite = TestSuite(
        tests=[
            TestColumnNumberOfDifferentMissingValues(
                column_name="feature1", missing_values=["null", "n/a"], replace=False, eq=0
            )
        ]
    )
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite


def test_data_integrity_test_different_missing_values_one_column_with_defaults() -> None:
    test_dataset = pd.DataFrame({"feature": ["None", "", None]})
    reference_dataset = pd.DataFrame({"feature": ["n/a", "test", None]})
    data_mapping = ColumnMapping()

    suite = TestSuite(
        tests=[
            TestColumnNumberOfDifferentMissingValues(
                column_name="feature", missing_values=["None", "n/a"], replace=False
            )
        ]
    )
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    assert not suite, suite.json()

    another_test_dataset = pd.DataFrame({"feature": ["None", "test", None]})
    suite.run(current_data=another_test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    assert suite, suite.json()


def test_data_integrity_test_number_of_missing_values_one_column() -> None:
    test_dataset = pd.DataFrame({"feature1": ["", None, "None", "a"], "feature2": ["b", "None", None, None]})

    suite = TestSuite(tests=[TestColumnNumberOfMissingValues(column_name="feature1", lt=10)])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()
