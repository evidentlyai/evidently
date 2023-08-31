import numpy as np
import pandas as pd
from pydantic import BaseModel


def smart_assert_equal(actual, expected):
    if isinstance(actual, BaseModel) and isinstance(expected, BaseModel) and actual.__class__ is expected.__class__:
        for field in actual.__fields__.values():
            smart_assert_equal(getattr(actual, field.name), getattr(expected, field.name))
        return
    if isinstance(actual, pd.Series):
        pd.testing.assert_series_equal(actual, expected)
        return
    if isinstance(actual, pd.DataFrame):
        pd.testing.assert_frame_equal(actual, expected)
        return
    if isinstance(actual, list) and isinstance(expected, list):
        for idx in range(len(actual)):
            smart_assert_equal(actual[idx], expected[idx])
        return
    if isinstance(actual, dict) and isinstance(expected, dict):
        for key in set(actual.keys()) | set(expected.keys()):
            smart_assert_equal(actual.get(key), expected.get(key))
        return
    np.testing.assert_equal(actual, expected)
