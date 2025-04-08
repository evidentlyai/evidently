import json
from typing import Optional

import pandas as pd
import pytest

from evidently.legacy.metrics import TargetByFeaturesTable
from evidently.legacy.options.agg_data import RenderOptions
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, data_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"target": [1, 2, 3]}),
            pd.DataFrame({"target": [1, 2, 3]}),
            None,
            TargetByFeaturesTable(),
            {},
        ),
        (
            pd.DataFrame({"target": [1, 2, 3]}),
            pd.DataFrame({"target": [1, 2, 3]}),
            None,
            TargetByFeaturesTable(),
            {},
        ),
    ),
)
def test_target_by_features_table_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: TargetByFeaturesTable,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric], options=Options(render=RenderOptions(raw_data=True)))
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    assert report.show()
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "TargetByFeaturesTable"
    assert result["metrics"][0]["result"] == expected_json
