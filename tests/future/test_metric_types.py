import numpy as np
import pandas as pd
import pytest

from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import SingleValue


@pytest.mark.parametrize(
    "input,output",
    [
        ({np.nan: (1.0, 1.0)}, ({"nan": 1.0}, {"nan": 1.0})),
        ({pd.NA: (1.0, 1.0)}, ({None: 1.0}, {None: 1.0})),
        ({np.int64(7): (3.0, 0.5)}, ({7: 3.0}, {7: 0.5})),
    ],
)
def test_by_label_count_value(input: dict, output: tuple):
    value = ByLabelCountValue(
        counts={k: SingleValue(value=v[0], display_name="test", metric_value_location=None) for k, v in input.items()},
        shares={k: SingleValue(value=v[1], display_name="test", metric_value_location=None) for k, v in input.items()},
        display_name="test",
        metric_value_location=None,
        tests=[],
    )
    assert {"counts": output[0], "shares": output[1]} == value.to_simple_dict()
