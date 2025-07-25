import json
from inspect import isabstract
from typing import List
from typing import Tuple

import pandas as pd
import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import ColumnCondition
from evidently.core.datasets import ColumnTest
from evidently.core.datasets import Dataset
from evidently.tests.descriptors import EqualsColumnCondition
from evidently.tests.descriptors import GreaterColumnCondition
from evidently.tests.descriptors import GreaterEqualColumnCondition
from evidently.tests.descriptors import IsInColumnCondition
from evidently.tests.descriptors import IsNotInColumnCondition
from evidently.tests.descriptors import LessColumnCondition
from evidently.tests.descriptors import LessEqualColumnCondition
from evidently.tests.descriptors import NotEqualsColumnCondition
from tests.conftest import load_all_subtypes

all_conditions: List[Tuple[ColumnCondition, pd.Series, str, pd.Series]] = [
    (
        GreaterEqualColumnCondition(threshold=2),
        pd.Series([1, 2, 3], name="input"),
        "input: greater or equal to 2.0",
        pd.Series([False, True, True]),
    ),
    (
        GreaterColumnCondition(threshold=2),
        pd.Series([1, 2, 3], name="input"),
        "input greater than 2.0",
        pd.Series([False, False, True]),
    ),
    (
        LessEqualColumnCondition(threshold=2),
        pd.Series([1, 2, 3], name="input"),
        "input: less or equal to 2.0",
        pd.Series([True, True, False]),
    ),
    (
        LessColumnCondition(threshold=2),
        pd.Series([1, 2, 3], name="input"),
        "input: less than 2.0",
        pd.Series([True, False, False]),
    ),
    (
        EqualsColumnCondition(expected=2),
        pd.Series([1, 2, 3], name="input"),
        "input: equals 2",
        pd.Series([False, True, False]),
    ),
    (
        NotEqualsColumnCondition(expected=2),
        pd.Series([1, 2, 3], name="input"),
        "input not equals 2",
        pd.Series([True, False, True]),
    ),
    (
        IsNotInColumnCondition(values={1}),
        pd.Series([1, 2, 3], name="input"),
        "input not in list {1}",
        pd.Series([False, True, True]),
    ),
    (
        IsInColumnCondition(values={2, 3}),
        pd.Series([1, 2, 3], name="input"),
        "input in list {2, 3}",
        pd.Series([False, True, True]),
    ),
]


def test_all_conditions_tested():
    tested_cond_set = {type(p) for p, _, _, _ in all_conditions}
    load_all_subtypes(ColumnCondition)
    all_cond_types = set(s for s in ColumnCondition.__subclasses__() if not isabstract(s))
    assert tested_cond_set == all_cond_types, "Missing tests for conditions " + ", ".join(
        f'({t.__name__}(), pd.Series([], name="input"), "input_test", pd.Series([]))'
        for t in all_cond_types - tested_cond_set
    )


@pytest.mark.parametrize("condition,input,column_name,result", all_conditions)
def test_conditions(condition: ColumnCondition, input: pd.Series, column_name: str, result: pd.Series):
    df = pd.DataFrame(input)

    dataset = Dataset.from_pandas(df)
    dataset.add_descriptor(ColumnTest(str(input.name), condition))
    res_df = dataset.as_dataframe()

    assert column_name in res_df.columns, f"Wrong column name {column_name}, actual: {res_df.columns}"
    values = res_df[column_name].tolist()
    assert values == result.tolist()

    payload = json.loads(condition.json())
    condition2 = parse_obj_as(ColumnCondition, payload)

    assert condition2 == condition
