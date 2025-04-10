import datetime
import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.utils import NumpyEncoder
from evidently.legacy.utils.types import ApproxValue


@pytest.mark.parametrize(
    "value,expected",
    [
        *[
            (t(0), "0")
            for t in (
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
        *[(t(1.0), "1.0") for t in (np.double, np.float16, np.float32, np.float64)],
        (np.array([1, 2]), "[1, 2]"),
        (np.bool_(False), "false"),
        (pd.Timedelta(1), '"0 days 00:00:00.000000001"'),
        (np.void(0), "null"),
        (pd.NaT, "null"),
        (pd.Timestamp(year=2000, month=1, day=1), '"2000-01-01T00:00:00"'),
        (datetime.datetime(2000, 1, 1), '"2000-01-01T00:00:00"'),
        (datetime.date(2000, 1, 1), '"2000-01-01"'),
        (ApproxValue(1), '{"value": 1, "relative": 1e-06, "absolute": 1e-12}'),
        (pd.Series([0]), "[0]"),
    ],
)
def test_encoder(value, expected):
    assert json.dumps({"value": value}, cls=NumpyEncoder) == f'{{"value": {expected}}}'
