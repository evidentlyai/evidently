import json

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import DataQualityValueQuantileMetric
from evidently.metrics.base_metric import InputData
from evidently.report import Report


def test_data_quality_quantile_metric_success() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueQuantileMetric(column_name="numerical_feature", quantile=0.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.quantile == 0.5
    assert result.current == 2


def test_data_quality_quantile_metric_value_errors() -> None:
    test_dataset = pd.DataFrame({"category_feature": ["a", "b", "c"]})
    data_mapping = ColumnMapping(categorical_features=["category_feature"])
    metric = DataQualityValueQuantileMetric(column_name="category_feature", quantile=0.5)

    with pytest.raises(ValueError):
        metric.calculate(data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping))


def test_data_quality_quantile_metric_with_report() -> None:
    current_data = pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]})
    reference_data = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    metric = DataQualityValueQuantileMetric(column_name="numerical_feature", quantile=0.5)
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "DataQualityValueQuantileMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["DataQualityValueQuantileMetric"] == {
        "column_name": "numerical_feature",
        "current": 1.5,
        "quantile": 0.5,
        "reference": 2.0,
    }
