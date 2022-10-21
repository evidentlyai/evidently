import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metric_preset import DataQualityPreset
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
                    "my_target": [1, 2, 3],
                    "prediction": [1, 2, 3],
                    "feature1": [1, 2, 3],
                    "feature2": ["a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=3),
                }
            ),
            pd.DataFrame(
                {
                    "my_target": [1, np.NaN, 3, 3, 2, 1],
                    "prediction": [1, 2, 3, 3, 2, 1],
                    "feature1": [1, 2, 3, np.NaN, 2, np.NaN],
                    "feature2": [np.NaN, "b", "c", "a", "b", "c"],
                    "feature3": [np.NaN, "b", "c", "a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=6),
                }
            ),
            ColumnMapping(
                target="my_target",
                prediction=["feature1", "feature2"],
                datetime="datetime",
            ),
        ),
    ),
)
def test_data_quality_preset(
    current_data: pd.DataFrame, reference_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
) -> None:
    report = Report(metrics=[DataQualityPreset()])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    result = json.loads(json_result)
    assert "metrics" in result
