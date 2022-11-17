import json

import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import ColumnQuantileMetric
from evidently.report import Report


def test_same_type_metric_in_one_json_report() -> None:
    current_data = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [0, 0, 0]})
    reference_data = pd.DataFrame({"feature1": [1, 0, 1, 0], "feature2": [1, 2, 3, 1]})
    report = Report(
        metrics=[
            ColumnQuantileMetric(column_name="feature1", quantile=0.5),
            ColumnQuantileMetric(column_name="feature1", quantile=0.7),
            ColumnQuantileMetric(column_name="feature2", quantile=0.5),
        ]
    )
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    result_json = report.json()
    result = json.loads(result_json)
    assert "timestamp" in result
    assert "results" in result
    assert result["results"] == [
        {
            "metric": "ColumnQuantileMetric",
            "result": {"column_name": "feature1", "current": 2.0, "quantile": 0.5, "reference": 0.5},
        },
        {
            "metric": "ColumnQuantileMetric",
            "result": {"column_name": "feature1", "current": 2.4, "quantile": 0.7, "reference": 1.0},
        },
        {
            "metric": "ColumnQuantileMetric",
            "result": {"column_name": "feature2", "current": 0.0, "quantile": 0.5, "reference": 1.5},
        },
    ]
