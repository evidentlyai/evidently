import numpy as np
import pandas as pd
from pydantic.v1 import BaseModel


def smart_assert_equal(actual, expected, path=""):
    if isinstance(actual, BaseModel) and isinstance(expected, BaseModel) and actual.__class__ is expected.__class__:
        for field in actual.__fields__.values():
            smart_assert_equal(getattr(actual, field.name), getattr(expected, field.name), path=f"{path}.{field.name}")
        return
    if isinstance(actual, pd.Series):
        try:
            pd.testing.assert_series_equal(actual, expected, check_dtype=False)
        except AssertionError as e:
            raise AssertionError(e.args[0] + f"\npath: {path}")
        return
    if isinstance(actual, pd.DataFrame):
        try:
            pd.testing.assert_frame_equal(actual, expected, check_dtype=False)
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
