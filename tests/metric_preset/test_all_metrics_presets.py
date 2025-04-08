import numpy.testing
import pandas as pd
import pytest

from evidently.legacy.metric_preset import ClassificationPreset
from evidently.legacy.metric_preset import DataDriftPreset
from evidently.legacy.metric_preset import DataQualityPreset
from evidently.legacy.metric_preset import RegressionPreset
from evidently.legacy.metric_preset.metric_preset import MetricPreset
from evidently.legacy.options.agg_data import RenderOptions
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize("raw_data", [False, True])
@pytest.mark.parametrize(
    "preset",
    (
        ClassificationPreset(),
        DataDriftPreset(),
        DataQualityPreset(),
        RegressionPreset(),
    ),
)
def test_metric_presets(preset: MetricPreset, tmp_path, raw_data):
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
    report = Report(metrics=[preset], options=Options(render=RenderOptions(raw_data=raw_data)))
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    report._inner_suite.raise_for_error()
    assert report.show()
    assert report.json()

    path = str(tmp_path / "report.json")
    report.save(path)
    report2 = Report.load(path)
    numpy.testing.assert_equal(report2.as_dict(), report.as_dict())  # has nans
    report2.show()
    report2.save_html(str(tmp_path / "report.html"))
