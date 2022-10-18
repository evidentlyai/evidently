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


def test_data_quality_quantile_metric_with_report() -> None:
    current_data = pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]})
    reference_data = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    metric = ColumnQuantileMetric(column_name="numerical_feature", quantile=0.5)
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnQuantileMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnQuantileMetric"] == {
        "column_name": "numerical_feature",
        "current": 1.5,
        "quantile": 0.5,
        "reference": 2.0,
    }
