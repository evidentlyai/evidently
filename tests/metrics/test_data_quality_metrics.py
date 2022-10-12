import numpy as np
import pandas as pd
import pytest

from evidently.metrics import DataQualityCorrelationMetrics
from evidently.metrics import DataQualityMetrics
from evidently.metrics import DataQualityStabilityMetrics
from evidently.metrics import DataQualityValueListMetric
from evidently.metrics import DataQualityValueQuantileMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


def test_data_quality_metrics() -> None:
    test_dataset = pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None


def test_data_quality_stability_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [1, 1, 2, 2, 5],
            "feature2": [1, 1, 2, 2, 8],
            "target": [1, 0, 1, 1, 0],
            "prediction": [1, 0, 1, 0, 0],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityStabilityMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_not_stable_target == 2
    assert result.number_not_stable_prediction == 4


def test_data_quality_stability_metrics_no_other_columns() -> None:
    curr = pd.DataFrame(
        {
            "target": [1, 0, 1],
            "prediction": [1, 0, 1],
        }
    )
    ref = pd.DataFrame(
        {
            "target": [1, 1, 1],
            "prediction": [1, 1, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityStabilityMetrics()
    result = metric.calculate(data=InputData(current_data=curr, reference_data=ref, column_mapping=data_mapping))
    assert result is not None
    assert result.number_not_stable_target == 0
    assert result.number_not_stable_prediction == 0


@pytest.mark.parametrize(
    "metric_object",
    (
        DataQualityMetrics(),
        DataQualityStabilityMetrics(),
        DataQualityValueListMetric(column_name="feature", values=[1, 0]),
        DataQualityValueQuantileMetric(column_name="feature", quantile=0.5),
        DataQualityCorrelationMetrics(),
    ),
)
def test_data_quality_metrics_with_report(metric_object: Metric) -> None:
    test_dataset = pd.DataFrame(
        {
            "feature": [1, 2, 3, 4, np.nan],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[metric_object])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    assert report.show()
    assert report.json()

    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()
