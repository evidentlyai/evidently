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


@pytest.mark.parametrize(
    "value",
    [
        pd.NA,
        pd.NaT,
    ],
)
def test_convert_types_handles_pandas_na(value):
    # Regression for #1844: convert_types previously called np.isnan(val) which
    # raises TypeError on pd.NA ("boolean value of NA is ambiguous") and on
    # pd.NaT. Pandas-flavored NA should now collapse to None instead of
    # propagating a TypeError up through ByLabelCountValue construction.
    assert convert_types(value) is None


def test_convert_types_preserves_existing_contracts():
    # Non-NA labels must still flow through untouched, and numpy.nan must
    # round-trip as a float so the ByLabelCountValue serializer keeps emitting
    # the string "nan" (see test_by_label_count_value above).
    assert convert_types(True) is True
    assert convert_types(0) == 0
    assert convert_types(42) == 42
    assert convert_types("class_a") == "class_a"
    assert convert_types(None) is None
    nan_out = convert_types(np.nan)
    assert isinstance(nan_out, float) and np.isnan(nan_out)


def test_by_label_count_value_handles_pd_na_key():
    # End-to-end: ByLabelCountValue construction must not crash when a count
    # dict keyed by pd.NA reaches the convert_types pipeline.
    value = ByLabelCountValue(
        counts={pd.NA: SingleValue(value=1.0, display_name="t", metric_value_location=None)},
        shares={pd.NA: SingleValue(value=1.0, display_name="t", metric_value_location=None)},
        display_name="t",
        metric_value_location=None,
        tests=[],
    )
    # No assertion on key shape — just that construction + dict export succeed.
    out = value.to_simple_dict()
    assert "counts" in out and "shares" in out
