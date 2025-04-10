import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metric_preset import DataQualityPreset
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, metric, column_mapping",
    (
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
            None,
            DataQualityPreset(columns=["feature1", "feature2"]),
            ColumnMapping(
                target="my_target",
            ),
        ),
        (
            pd.DataFrame(
                {
                    "myid": "some_id",
                    "my_target": [1, 2, 3],
                    "prediction": [1, 2, 3],
                    "feature1": [1, 2, 3],
                    "feature2": ["a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=3),
                }
            ),
            pd.DataFrame(
                {
                    "myid": "some_id",
                    "my_target": [1, np.nan, 3, 3, 2, 1],
                    "prediction": [1, 2, 3, 3, 2, 1],
                    "feature1": [1, 2, 3, np.nan, 2, np.nan],
                    "feature2": [np.nan, "b", "c", "a", "b", "c"],
                    "feature3": [np.nan, "b", "c", "a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=6),
                }
            ),
            DataQualityPreset(),
            ColumnMapping(
                target="my_target",
                id="myid",
                prediction="prediction",
                datetime="datetime",
            ),
        ),
        (
            pd.DataFrame(
                {
                    "myid": "some_id",
                    "my_target": [1, 2, 3],
                    "prediction": [1, 2, 3],
                    "feature1": [1, 2, 3],
                    "feature2": ["a", "b", "c"],
                    "datetime": pd.date_range("2020-01-01", periods=3),
                }
            ),
            None,
            DataQualityPreset(),
            ColumnMapping(
                target="my_target",
                id="myid",
                prediction="prediction",
                datetime="datetime",
            ),
        ),
    ),
)
def test_data_quality_preset(
    current_data: pd.DataFrame,
    reference_data: Optional[pd.DataFrame],
    metric: DataQualityPreset,
    column_mapping: ColumnMapping,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    result = json.loads(json_result)
    assert "metrics" in result
