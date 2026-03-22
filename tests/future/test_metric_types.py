import numpy as np
import pandas as pd
import pytest

from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import convert_types


@pytest.mark.parametrize(
    "input,output",
    [
        ({np.nan: (1.0, 1.0)}, ({"nan": 1.0}, {"nan": 1.0})),
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


def test_by_label_count_value_pd_na():
    value = ByLabelCountValue(
        counts={pd.NA: SingleValue(value=1.0, display_name="test", metric_value_location=None)},
        shares={pd.NA: SingleValue(value=1.0, display_name="test", metric_value_location=None)},
        display_name="test",
        metric_value_location=None,
        tests=[],
    )
    result = value.to_simple_dict()
    assert None in result["counts"]
    assert result["counts"][None] == 1.0


def test_convert_types_pd_na():
    assert convert_types(pd.NA) is None


def test_convert_types_pd_nat():
    assert convert_types(pd.NaT) is None


def test_convert_types_none():
    assert convert_types(None) is None


def test_convert_types_preserves_np_nan():
    result = convert_types(np.nan)
    assert np.isnan(result)
