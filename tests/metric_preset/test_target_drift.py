import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metric_preset import TargetDriftPreset
from evidently.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping",
    (
        (
            pd.DataFrame(),
            None,
            ColumnMapping(),
        ),
        (pd.DataFrame(), pd.DataFrame(), ColumnMapping()),
        (
            pd.DataFrame(
                {
                    "my_target": ["1", "2", "3"],
                    "1": [0.1, 0.2, 0.3],
                    "2": [0.9, 0.8, 0.7],
                    "3": [0.9, 0.8, 0.7],
                    "feature2": ["a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=3),
                }
            ),
            pd.DataFrame(
                {
                    "my_target": ["1", np.NaN, "3", "3", "2", "1"],
                    "1": [0.1, 0.2, np.NaN, 0.2, 0.2, 0.1],
                    "2": [0.9, 0.8, 0.5, 0.8, 0.7, 0.9],
                    "3": [0.9, 0.8, 0.5, 0.8, 0.7, 0.9],
                    "feature2": [np.NaN, "b", "c", "a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=6),
                }
            ),
            ColumnMapping(
                target="my_target",
                prediction=["1", "2", "3"],
                datetime="datetime",
                task="classification",
            ),
        ),
    ),
)
def test_target_drift_preset_with_report(
    current_data: pd.DataFrame, reference_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
) -> None:
    report = Report(metrics=[TargetDriftPreset()])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    result = json.loads(json_result)
    assert "metrics" in result
