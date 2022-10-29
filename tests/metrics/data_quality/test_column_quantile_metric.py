import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import ColumnQuantileMetric
from evidently.metrics.base_metric import InputData
from evidently.report import Report


def test_data_quality_quantile_metric_success() -> None:
    test_dataset = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    data_mapping = ColumnMapping()
    metric = ColumnQuantileMetric(column_name="numerical_feature", quantile=0.5)
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.quantile == 0.5
    assert result.current == 2


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, error_message",
    (
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            ColumnQuantileMetric(column_name="test", quantile=0.5),
            "Column 'test' is not in current data.",
        ),
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, 3]}),
            ColumnQuantileMetric(column_name="test", quantile=0.5),
            "Column 'test' is not in reference data.",
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c"]}),
            None,
            ColumnQuantileMetric(column_name="category_feature", quantile=0.5),
            "Column 'category_feature' in current data is not numeric.",
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, "a"]}),
            ColumnQuantileMetric(column_name="feature", quantile=0.5),
            "Column 'feature' in reference data is not numeric.",
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            ColumnQuantileMetric(column_name="feature", quantile=-0.5),
            "Quantile should all be in the interval (0, 1].",
        ),
    ),
)
def test_data_quality_quantile_metric_value_errors(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: ColumnQuantileMetric,
    error_message: str,
) -> None:
    data_mapping = ColumnMapping()

    with pytest.raises(ValueError) as error:
        metric.calculate(
            data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
        )

    assert error.value.args[0] == error_message


@pytest.mark.parametrize(
    "current, reference, column_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]}),
            pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]}),
            ColumnMapping(),
            ColumnQuantileMetric(column_name="numerical_feature", quantile=0.5),
            {
                "column_name": "numerical_feature",
                "current": 1.5,
                "quantile": 0.5,
                "reference": 2.0,
            },
        ),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1, 2, 2, 5],
                    "feature2": [1, 1, 2, 2, 8],
                    "my_target": [1, 0, 1, 1, 0],
                    "prediction": [1, 0, 1, 0, 0],
                }
            ),
            None,
            ColumnMapping(target="my_target"),
            ColumnQuantileMetric(column_name="my_target", quantile=0.5),
            {"column_name": "my_target", "current": 1.0, "quantile": 0.5, "reference": None},
        ),
        (
            pd.DataFrame(
                {
                    "my_target": [1, np.NaN, 3] * 1000,
                    "my_prediction": [1, 2, np.NaN] * 1000,
                    "feature_1": [1, 2, 3] * 1000,
                    "feature_2": ["a", np.NaN, "a"] * 1000,
                }
            ),
            pd.DataFrame(
                {
                    "my_target": [1, 2, 3] * 10000,
                    "my_prediction": [1, 2, 1] * 10000,
                    "feature_1": [1, 2, 3] * 10000,
                    "feature_2": ["a", "a", "a"] * 10000,
                }
            ),
            ColumnMapping(target="my_target", prediction="my_prediction"),
            ColumnQuantileMetric(column_name="my_target", quantile=0.5),
            {"column_name": "my_target", "current": 2.0, "quantile": 0.5, "reference": 2.0},
        ),
    ),
)
def test_column_quantile_metric_with_report(
    current: pd.DataFrame,
    reference: Optional[pd.DataFrame],
    column_mapping: ColumnMapping,
    metric: ColumnQuantileMetric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current, reference_data=reference, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnQuantileMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnQuantileMetric"] == expected_json
