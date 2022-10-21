import pandas as pd
import pytest

from evidently.metric_preset import ClassificationPerformance
from evidently.metric_preset import DataDriftPreset
from evidently.metric_preset import DataQualityPreset
from evidently.metric_preset import RegressionPerformance
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


@pytest.mark.parametrize(
    "preset",
    (
        ClassificationPerformance(),
        DataDriftPreset(),
        DataQualityPreset(),
        RegressionPerformance(),
    ),
)
def test_metric_presets(preset: MetricPreset):
    current_data = pd.DataFrame(
        {
            "category_feature": ["t", "e", "t"],
            "numerical_feature": [0.4, 0.4, 0.9],
            "target": [3, 2, 1],
            "prediction": [1, 2, 3],
        }
    )
    reference_data = pd.DataFrame(
        {
            "category_feature": ["t"],
            "numerical_feature": [0.4],
            "target": [1],
            "prediction": [1],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[preset])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    assert report.show()
    assert report.json()
