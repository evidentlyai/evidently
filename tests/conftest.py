import numpy as np
import pandas as pd
import pytest

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import import_string
from evidently.legacy.utils.types import ApproxValue
from evidently.pydantic_utils import TYPE_ALIASES
from evidently.pydantic_utils import PolymorphicModel

# for np.testing.assert_equal to work with ApproxValue
np.core.numeric.ScalarType = np.core.numeric.ScalarType + (ApproxValue,)  # type: ignore[attr-defined]


def smart_assert_equal(actual, expected, path=""):
    if (
        isinstance(actual, BaseModel)
        and isinstance(expected, BaseModel)
        and (
            actual.__class__ is expected.__class__
            or (
                isinstance(actual, PolymorphicModel)
                and isinstance(expected, PolymorphicModel)
                and actual.type == expected.type
            )
        )
    ):
        ignore_not_set = hasattr(expected, "__ignore_not_set__") and expected.__ignore_not_set__
        for field in actual.__fields__.values():
            if ignore_not_set and getattr(expected, field.name) is None:
                continue
            smart_assert_equal(getattr(actual, field.name), getattr(expected, field.name), path=f"{path}.{field.name}")
        return
    if isinstance(actual, pd.Series):
        try:
            np.array_equal(actual.values, expected.values)
        except AssertionError as e:
            raise AssertionError(e.args[0] + f"\npath: {path}")
        return
    if isinstance(actual, pd.DataFrame):
        try:
            np.array_equal(actual.values, expected.values)
        except AssertionError as e:
            raise AssertionError(e.args[0] + f"\npath: {path}")
        return
    if isinstance(actual, list) and isinstance(expected, list):
        for idx in range(len(actual)):
            smart_assert_equal(actual[idx], expected[idx], path=f"{path}[{idx}]")
        return
    if isinstance(actual, dict) and isinstance(expected, dict):
        for key in set(actual.keys()) | set(expected.keys()):
            smart_assert_equal(actual.get(key), expected.get(key), path=f"{path}[{key}]")
        return
    try:
        np.testing.assert_equal(actual, expected, f"path: {path}")
    except AssertionError:
        raise


slow = pytest.mark.slow


def load_all_subtypes(base_class):
    classpaths = [
        cp for (base, _), cp in TYPE_ALIASES.items() if isinstance(base, type) and issubclass(base, base_class)
    ]
    for cp in classpaths:
        try:
            import_string(cp)
        except ImportError as e:
            raise ImportError(f"Cannot import type {cp}") from e
