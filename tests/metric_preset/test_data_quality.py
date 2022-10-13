import json
from typing import Optional

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
        (
            pd.DataFrame(),
            pd.DataFrame(),
            ColumnMapping()
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
