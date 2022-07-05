from datetime import datetime

import numpy as np
import pandas as pd

import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.tests import TestNumberOfColumns
from evidently.v2.tests import TestNumberOfRows
from evidently.v2.tests import TestNumberOfNANs
from evidently.v2.tests import TestNumberOfColumnsWithNANs
from evidently.v2.tests import TestNumberOfRowsWithNANs
from evidently.v2.tests import TestNumberOfConstantColumns
from evidently.v2.tests import TestNumberOfEmptyRows
from evidently.v2.tests import TestNumberOfEmptyColumns
from evidently.v2.tests import TestNumberOfDuplicatedRows
from evidently.v2.tests import TestNumberOfDuplicatedColumns
from evidently.v2.tests import TestColumnsType
from evidently.v2.tests import TestColumnNANShare
from evidently.v2.tests import TestAllConstantValues
from evidently.v2.tests import TestAllUniqueValues
from evidently.v2.tests import TestColumnValueRegexp
from evidently.v2.test_suite import TestSuite


def test_data_integrity_test_number_of_columns() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestNumberOfColumns(gte=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfColumns(eq=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_number_of_rows() -> None:
    test_dataset = pd.DataFrame({"target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestNumberOfRows(is_in=[10, 3, 50])])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfRows(gte=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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
    suite = TestSuite(tests=[TestNumberOfConstantColumns(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfConstantColumns(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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
    suite = TestSuite(tests=[TestNumberOfDuplicatedRows(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfDuplicatedRows(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_duplicated_columns() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": ["1", "1", "1", "1"], "target": ["1", "1", "1", "1"]})
    suite = TestSuite(tests=[TestNumberOfDuplicatedColumns(gte=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfDuplicatedColumns(eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_columns_type() -> None:
    current_dataset = pd.DataFrame({"numerical_feature": [1, 2, 3], "target": ["1", "1", "1"]})
    reference_dataset = pd.DataFrame({
        "numerical_feature": [1., 2.4, 3.],
        "target": [True, False, True],
        "datetime": [datetime.now(), datetime.now(), datetime.now()]
    })
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

    suite = TestSuite(tests=[
        TestColumnsType(columns_type={
            "numerical_feature": np.float64,
            "target": "bool",
            "datetime": "datetime"
        })
    ])
    suite.run(current_data=reference_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestColumnsType(columns_type={"numerical_feature": "number"})])
    suite.run(current_data=current_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_integrity_test_columns_nan_share() -> None:
    test_dataset = pd.DataFrame({"feature1": [1, 2, np.nan], "feature2": [1, 2, np.nan], "target": ["1", "1", "1"]})

    suite = TestSuite(tests=[TestColumnNANShare(lte=0.1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnNANShare(column_name="not_exists_feature")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnNANShare(column_name="feature1", lt=0.1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnNANShare(column_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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
