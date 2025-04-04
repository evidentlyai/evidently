import json
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.utils.numpy_encoder import NumpyEncoder


@pytest.mark.parametrize(
    "test_object, expected_json",
    (
        (
            [np.nan, np.inf, -np.inf],
            "[NaN, Infinity, -Infinity]",
        ),
        (
            [
                _type(42)
                for _type in (
                    np.int_,
                    np.intc,
                    np.intp,
                    np.int8,
                    np.int16,
                    np.int32,
                    np.int64,
                    np.uint8,
                    np.uint16,
                    np.uint32,
                    np.uint64,
                )
            ],
            "[42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42]",
        ),
        (
            [_type(0.5) for _type in (np.double, np.float16, np.float32, np.float64)],
            "[0.5, 0.5, 0.5, 0.5]",
        ),
        (np.array([np.bool_(1), np.bool_(0)]), "[true, false]"),
        (
            np.array([0, 1, 2.1, np.nan, np.inf, pd.NaT]),
            "[0, 1, 2.1, NaN, Infinity, null]",
        ),
        (np.empty((0, 0)), "[]"),
        (
            np.array([[0, 1, 2.1], [0, 1, 2.1], [0, 1, 2.1]]),
            "[[0.0, 1.0, 2.1], [0.0, 1.0, 2.1], [0.0, 1.0, 2.1]]",
        ),
        (np.ones((2, 3)), "[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]"),
        (np.void(3), "null"),
        # pandas date classes
        ([pd.Timestamp(2022, 2, 3, 12)], '["2022-02-03T12:00:00"]'),
        (
            [datetime(year=2022, month=1, day=13, hour=12, minute=45, second=32)],
            '["2022-01-13T12:45:32"]',
        ),
        ([pd.Timedelta(days=1)], '["1 days 00:00:00"]'),
        # python types
        (
            [321123321123, 0.56, True, False, None, "test", {1: 4}],
            '[321123321123, 0.56, true, false, null, "test", {"1": 4}]',
        ),
    ),
)
def test_numpy_encoder_compatible_types(test_object, expected_json: str) -> None:
    assert json.dumps(test_object, cls=NumpyEncoder) == expected_json, test_object


class _UnsupportedJson:
    pass


@pytest.mark.parametrize(
    "test_object, type_name_in_error",
    (
        (_UnsupportedJson(), "_UnsupportedJson"),
        ({1, 2, 3}, "set"),
    ),
)
def test_numpy_encoder_incompatible_types(test_object, type_name_in_error: str) -> None:
    with pytest.raises(TypeError) as error:
        json.dumps(test_object, cls=NumpyEncoder)
        assert type_name_in_error in str(error)
