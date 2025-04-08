from typing import Any

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.features.is_valid_python_feature import IsValidPython


@pytest.mark.parametrize(
    ("column_value", "expected"),
    [
        ("print('Hello')", True),
        ("x = 5 + 3", True),
        ("def foo():\n    return 'bar'", True),
        ("for i in range(10): print(i)", True),
        ("print('Hello'", False),
        ("for i in range(5) print(i)", False),
        ("def foo(\n    return 'bar'", False),
        ("if True print('yes')", False),
        (None, False),
        ("12", True),
        ("Sorry I can't answer this", False),
        ("{'name': 'test', 'age': 13}", True),
    ],
)
def test_is_valid_python_apply(column_value: Any, expected: bool):
    is_python = IsValidPython("TestColumnName")
    actual = is_python.apply(column_value)
    assert actual == expected


test_data = pd.DataFrame(
    {
        "TestColumnName": [
            "print('Hello')",
            "def foo():\n    return 'bar'",
            "def foo(\n    return 'bar'",
            None,
            "{'name': 'test', 'age': 13}",
            np.nan,
        ]
    }
)


@pytest.mark.parametrize(
    ("expected"),
    [[True, True, False, False, True, False]],
)
def test_is_valid_python(expected: bool):
    is_python = IsValidPython("TestColumnName")
    actual = is_python.generate_feature(test_data, None)
    assert actual[is_python._feature_column_name()].tolist() == expected
