import json
from datetime import datetime

import numpy as np
import pandas as pd

import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.tests import TestNumberOfColumns
from evidently.tests import TestNumberOfRows
from evidently.tests import TestNumberOfNANs
from evidently.tests import TestNumberOfColumnsWithNANs
from evidently.tests import TestNumberOfRowsWithNANs
from evidently.tests import TestNumberOfConstantColumns
from evidently.tests import TestNumberOfEmptyRows
from evidently.tests import TestNumberOfEmptyColumns
from evidently.tests import TestNumberOfDuplicatedRows
from evidently.tests import TestNumberOfDuplicatedColumns
from evidently.tests import TestColumnsType
from evidently.tests import TestColumnNANShare
from evidently.tests import TestAllConstantValues
from evidently.tests import TestAllUniqueValues
from evidently.tests import TestColumnValueRegexp
from evidently.test_suite import TestSuite


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
            "number_of_columns": 3,
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
            "number_of_columns": 3,
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
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 4}}, "number_of_rows": 4},
        "status": "SUCCESS",
    }


@pytest.mark.parametrize(
    "test_dataset, conditions, result",
    (
        (pd.DataFrame({"target": [0, 0, 0, 1]}), {"eq": 0}, True),
        (pd.DataFrame({"target": [0, 0, None, 1], "numeric": [None, None, None, 1]}), {"lt": 3}, False),
    ),
)
def test_data_integrity_test_number_of_nans_no_errors(
    test_dataset: pd.DataFrame, conditions: dict, result: bool
) -> None:
    suite = TestSuite(tests=[TestNumberOfNANs(**conditions)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert bool(suite) is result


def test_data_integrity_test_number_of_columns_with_nans() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 2, None, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfColumnsWithNANs(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfColumnsWithNANs(eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_number_of_rows_with_nans() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": [None, "d", "p", "n"], "numerical_feature": [0, 2, None, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfRowsWithNANs(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfRowsWithNANs(eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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


def test_data_integrity_test_constant_columns_json_render() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 0, 0, 0], "target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestNumberOfConstantColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The number of constant columns is 1. The test threshold is lte=1.",
        "group": "data_integrity",
        "name": "Number of Constant Columns",
        "parameters": {"condition": {}, "number_of_constant_columns": 1},
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
            "number_of_duplicated_rows": 3,
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
        "parameters": {"condition": {"lte": 1}, "number_of_duplicated_columns": 1},
        "status": "SUCCESS",
    }


def test_data_integrity_test_columns_type() -> None:
    current_dataset = pd.DataFrame({"numerical_feature": [1, 2, 3], "target": ["1", "1", "1"]})
    reference_dataset = pd.DataFrame(
        {
            "numerical_feature": [1.0, 2.4, 3.0],
            "target": [True, False, True],
            "datetime": [datetime.now(), datetime.now(), datetime.now()],
        }
    )
    suite = TestSuite(tests=[TestColumnsType()])
    suite.run(current_data=current_dataset, reference_data=current_dataset, column_mapping=ColumnMapping())
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
    assert suite

    suite = TestSuite(tests=[TestColumnsType(columns_type={"numerical_feature": "number"})])
    suite.run(current_data=current_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_columns_type_to_json() -> None:
    current_dataset = pd.DataFrame({"numerical_feature": [1, 2, 3], "my_target": [True, False, True]})
    suite = TestSuite(tests=[TestColumnsType()])
    suite.run(
        current_data=current_dataset, reference_data=current_dataset, column_mapping=ColumnMapping(target="my_target")
    )
    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The number of columns with a type mismatch is 0 out of 2.",
        "group": "data_integrity",
        "name": "Column Types",
        "parameters": {
            "columns": [
                {"actual_type": "bool_", "column_name": "my_target", "expected_type": "bool_"},
                {"actual_type": "int64", "column_name": "numerical_feature", "expected_type": "int64"},
            ]
        },
        "status": "SUCCESS",
    }


def test_data_integrity_test_columns_nan_share() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 2, np.nan], "feature2": [1, 2, np.nan], "target": ["1", "1", "1"]})

    suite = TestSuite(tests=[TestColumnNANShare(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestColumnNANShare(column_name="feature1", lt=0.1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnNANShare(column_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_columns_nan_share_json_render() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 2, np.nan, 4], "feature2": [1, 2, np.nan, 1]})

    suite = TestSuite(tests=[TestColumnNANShare(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The share of NA values in feature1 is 0.25. The test threshold is eq=0.25 ± 0.025.",
        "group": "data_integrity",
        "name": "Share of NA Values",
        "parameters": {
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.25}},
            "nans_by_columns": {"feature1": 1, "feature2": 1},
            "number_of_rows": 4,
            "share_of_nans": 0.25,
        },
        "status": "SUCCESS",
    }


def test_data_integrity_test_columns_all_constant_values() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 1, np.nan], "feature2": [1, 2, np.nan], "target": ["1", "1", "1"]})
    suite = TestSuite(tests=[TestAllConstantValues(columns=[])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestAllConstantValues(columns=["not_exists_feature", "feature1", "feature2", "target"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestAllConstantValues(columns=["feature1"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestAllConstantValues(columns=["feature1", "feature2"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestAllConstantValues(columns=["target"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_columns_all_unique_values() -> None:
    test_dataset = pd.DataFrame(
        {"feature1": [1, 1, 2, 3], "feature2": [1, 2, np.nan, 4], "target": ["1", "2", "3", ""]}
    )
    suite = TestSuite(tests=[TestAllUniqueValues(columns=[])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestAllUniqueValues(columns=["not_exists_feature", "feature1", "feature2", "target"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestAllUniqueValues(columns=["feature2"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestAllUniqueValues(columns=["feature1", "feature2"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestAllUniqueValues(columns=["target"])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_column_values_match_regexp() -> None:
    test_dataset = pd.DataFrame({"feature1": ["a", "aa", "baa"], "feature2": ["b", "bb", "baa"], "target": [1, 2, 3]})
    suite = TestSuite(tests=[TestColumnValueRegexp(column_name="feature1", reg_exp=r"a.*", eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestColumnValueRegexp(column_name="feature2", reg_exp=r"c.*", lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(
        tests=[
            TestColumnValueRegexp(column_name="feature1", reg_exp=r"a.*", eq=2),
            TestColumnValueRegexp(column_name="feature2", reg_exp=r"b.*", eq=2),
        ]
    )
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(
        tests=[
            TestColumnValueRegexp(column_name="feature1", reg_exp=r"a.*", eq=2),
            TestColumnValueRegexp(column_name="feature2", reg_exp=r"b.*", eq=3),
        ]
    )
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
