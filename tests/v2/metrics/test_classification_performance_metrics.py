from typing import Dict, Optional

import numpy as np
import pandas as pd
import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics import ClassificationPerformanceMetrics
from evidently.v2.metrics.classification_performance_metrics import get_prediction_data


@pytest.mark.parametrize(
    "data,mapping,expected_predictions,expected_probas",
    [
        (
            pd.DataFrame([dict(target="a", prediction="a")]),
            ColumnMapping(prediction="prediction"),
            pd.Series(["a"]),
            None,
        ),
        (
            pd.DataFrame([dict(target="a", pos_proba=0.9)]),
            ColumnMapping(prediction="pos_proba", target_names=["b", "a"]),
            pd.Series(["a"]),
            pd.DataFrame([dict(a=0.9, b=0.1)]),
        ),
    ],
)
def test_prediction_data(
    data: pd.DataFrame, mapping: ColumnMapping, expected_predictions: pd.Series, expected_probas: Optional[pd.DataFrame]
):
    predictions, predictions_probas = get_prediction_data(data, mapping)
    assert predictions.equals(expected_predictions)
    if predictions_probas is None:
        assert expected_probas is None
    else:
        assert np.isclose(predictions_probas, expected_probas).all()


def test_classification_performance_metrics() -> None:
    test_dataset = pd.DataFrame({"target": [1, 1, 1, 1], "prediction": [1, 1, 1, 0]})
    data_mapping = ColumnMapping()
    metric = ClassificationPerformanceMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=None, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.current_metrics.accuracy == 0.75
    assert result.current_metrics.f1 < 0.5
    assert result.current_metrics.precision == 0.5
    assert result.current_metrics.recall == 0.375
