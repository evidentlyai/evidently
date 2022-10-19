import numpy as np
import pandas as pd
import pytest

from evidently.metrics import DataQualityCorrelationMetrics
from evidently.metrics import DataQualityMetrics
from evidently.metrics import DataQualityStabilityMetrics
from evidently.metrics import DataQualityValueListMetrics
from evidently.metrics import DataQualityValueQuantileMetrics
from evidently.metrics import DataQualityValueRangeMetrics
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


def test_data_quality_values_in_list_metrics() -> None:
    test_dataset = pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueListMetrics(column_name="category_feature", values=["d"])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_list == 1
    assert result.number_not_in_list == 3
    assert result.share_in_list == 0.25
    assert result.share_not_in_list == 0.75

    metric = DataQualityValueListMetrics(column_name="numerical_feature", values=[2])
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_list == 2
    assert result.number_not_in_list == 2
    assert result.share_in_list == 0.5
    assert result.share_not_in_list == 0.5

    reference_dataset = pd.DataFrame({"category_feature": ["n", "y", "n", "y"], "numerical_feature": [0, 2, 2, 432]})

    metric = DataQualityValueListMetrics(column_name="category_feature")
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_list == 2
    assert result.number_not_in_list == 2
    assert result.share_in_list == 0.5
    assert result.share_not_in_list == 0.5


def test_data_quality_values_in_list_metrics_reference_defaults() -> None:
    current_dataset = pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]})
    reference_dataset = pd.DataFrame({"category_feature": ["n", "n", "p", "n"]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueListMetrics(column_name="category_feature")
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_list == 3
    assert result.number_not_in_list == 1
    assert result.share_in_list == 0.75
    assert result.share_not_in_list == 0.25


def test_data_quality_values_in_range_metrics() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 432]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueRangeMetrics(column_name="numerical_feature", left=0, right=10.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_range == 3
    assert result.number_not_in_range == 1
    assert result.share_in_range == 0.75
    assert result.share_not_in_range == 0.25

    reference_dataset = pd.DataFrame({"numerical_feature": [0, 1, 1, 1]})

    metric = DataQualityValueRangeMetrics(column_name="numerical_feature")
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_range == 1
    assert result.number_not_in_range == 3
    assert result.share_in_range == 0.25
    assert result.share_not_in_range == 0.75

    metric = DataQualityValueRangeMetrics(column_name="numerical_feature", right=5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.number_in_range == 3
    assert result.number_not_in_range == 1
    assert result.share_in_range == 0.75
    assert result.share_not_in_range == 0.25


def test_data_quality_quantile_metrics() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    data_mapping = ColumnMapping()
    metric = DataQualityValueQuantileMetrics(column_name="numerical_feature", quantile=0.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.quantile == 0.5
    assert result.value == 2


def test_data_quality_correlation_metrics() -> None:
    current_dataset = pd.DataFrame(
        {
            "numerical_feature_1": [0, 2, 2, 2, 0],
            "numerical_feature_2": [0, 2, 2, 2, 0],
            "category_feature": [1, 2, 4, 2, 1],
            "target": [0, 2, 2, 2, 0],
            "prediction": [0, 2, 2, 2, 0],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataQualityCorrelationMetrics()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert set(result.current.num_features) == {"numerical_feature_1", "numerical_feature_2", "category_feature"}
    assert result.current.correlation_matrix is not None
    assert result.current.target_prediction_correlation == 1.0
    assert result.current.abs_max_target_features_correlation == 1.0
    assert result.current.abs_max_prediction_features_correlation == 1.0
    assert result.current.abs_max_correlation == 1.0
    assert result.current.abs_max_num_features_correlation == 1.0

    assert result.reference is None


@pytest.mark.parametrize(
    "metric_object",
    (
        DataQualityMetrics(),
        DataQualityStabilityMetrics(),
        DataQualityValueListMetrics(column_name="feature", values=[1, 0]),
        DataQualityValueRangeMetrics(column_name="feature", left=0, right=1),
        DataQualityValueQuantileMetrics(column_name="feature", quantile=0.5),
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
