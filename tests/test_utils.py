import json
from datetime import datetime
import pytest

import numpy as np
import pandas as pd

from evidently.utils.numpy_encoder import NumpyEncoder


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
            [_type(0.5) for _type in (np.float, np.float_, np.float16, np.float32, np.float64)],
            "[0.5, 0.5, 0.5, 0.5, 0.5]",
        ),
        ([(_type(1), _type(0)) for _type in (np.bool, np.bool_)], "[[true, false], [true, false]]"),
        (np.array([0, 1, 2.1, np.nan, np.inf, pd.NaT]), "[0, 1, 2.1, NaN, Infinity, null]"),
        (np.empty((0, 0)), "[]"),
        (np.array([[0, 1, 2.1], [0, 1, 2.1], [0, 1, 2.1]]), "[[0.0, 1.0, 2.1], [0.0, 1.0, 2.1], [0.0, 1.0, 2.1]]"),
        (np.ones((2, 3)), "[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]"),
        (np.void(3), "null"),
        # python types
        (
            [321123321123, 0.56, True, False, None, "test", {1: 4}],
            '[321123321123, 0.56, true, false, null, "test", {"1": 4}]',
        ),
    ),
)
def test_numpy_encoder_compatible_types(test_object, expected_json: str) -> None:
    assert json.dumps(test_object, cls=NumpyEncoder) == expected_json, test_object


@pytest.mark.parametrize(
    "test_object, type_name_in_error",
    ((datetime(year=2022, month=1, day=13, hour=12, minute=45, second=32), "datetime"), ({1, 2, 3}, "set")),
)
def test_numpy_encoder_incompatible_types(test_object, type_name_in_error: str) -> None:
    with pytest.raises(TypeError) as error:
        json.dumps(test_object, cls=NumpyEncoder)
        assert type_name_in_error in str(error)
