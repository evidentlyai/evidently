import pandas as pd
import pytest

from evidently import Dataset
from evidently import Report
from evidently.presets import DataSummaryPreset


@pytest.mark.parametrize("float_dtype", ["float32", "float64"])
@pytest.mark.parametrize("int_dtype", ["int16", "int32", "int64"])
def test_data_summary_convert_dtypes(float_dtype, int_dtype):
    data = pd.DataFrame(
        {
            "amount": pd.Series([i + 0.5 for i in range(12)], dtype=float_dtype),
            "count": pd.Series(range(12), dtype=int_dtype),
            "category": pd.Series([0, 1] * 6, dtype=int_dtype),
            "flag": [True, False] * 6,
        }
    )
    expected = Report([DataSummaryPreset()]).run(Dataset.from_pandas(data)).dict()["metrics"]
    actual = Report([DataSummaryPreset()]).run(Dataset.from_pandas(data.convert_dtypes())).dict()["metrics"]
    assert actual == expected
