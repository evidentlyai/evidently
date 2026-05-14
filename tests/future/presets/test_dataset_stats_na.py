import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.presets import DataDriftPreset
from evidently.presets import DataSummaryPreset


def _make_dataset() -> Dataset:
    df = pd.DataFrame({"a": pd.Series(["x", "y", "z", pd.NA], dtype="string")})
    return Dataset.from_pandas(df, DataDefinition(categorical_columns=["a"]))


def test_data_summary_preset_handles_pd_na():
    """Issue #1616: DataSummaryPreset must not fail on pd.NA in a categorical column."""
    Report([DataSummaryPreset()]).run(current_data=_make_dataset())


def test_data_drift_preset_handles_pd_na():
    """Issue #1616: DataDriftPreset must not fail on pd.NA in a categorical column."""
    Report([DataDriftPreset()]).run(current_data=_make_dataset(), reference_data=_make_dataset())
