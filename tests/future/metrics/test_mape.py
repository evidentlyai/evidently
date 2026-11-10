import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import mean_absolute_percentage_error

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import Regression
from evidently.core.report import Report
from evidently.metrics import MAPE


def _dataset(target, prediction):
    return Dataset.from_pandas(
        pd.DataFrame({"target": target, "prediction": prediction}),
        data_definition=DataDefinition(regression=[Regression()]),
    )


@pytest.mark.parametrize(
    "target,prediction,relative_errors",
    [
        ([-1.0, -2.0, -4.0], [-1.1, -1.8, -3.2], [0.1, 0.1, 0.2]),
        ([3.0, -0.5, 2.0, 7.0], [2.5, 0.0, 2.0, 8.0], [1 / 6, 1.0, 0.0, 1 / 7]),
        ([1.0, 2.0, 4.0], [1.1, 1.8, 3.2], [0.1, 0.1, 0.2]),
    ],
    ids=["negative", "mixed", "positive"],
)
def test_mape_report_uses_target_magnitude(target, prediction, relative_errors):
    snapshot = Report([MAPE()]).run(_dataset(target, prediction))
    result = snapshot.dict()["metrics"][0]["value"]

    assert result["mean"] == pytest.approx(100 * mean_absolute_percentage_error(target, prediction))
    assert result["std"] == pytest.approx(np.std(relative_errors, ddof=1))


@pytest.mark.parametrize(
    "zero_handling,expected_mean",
    [("none", 72.5), ("drop", 20.0), ("replace", 35.0)],
)
def test_mape_report_preserves_near_zero_handling(zero_handling, expected_mean):
    metric = MAPE(zero_handling=zero_handling, epsilon=0.1, replace_value=0.5)
    snapshot = Report([metric]).run(_dataset([0.0, -0.05, 1.0, 2.0], [0.2, -0.1, 1.2, 1.6]))

    assert snapshot.dict()["metrics"][0]["value"]["mean"] == pytest.approx(expected_mean)


def test_mape_report_with_negative_reference_targets():
    metric = MAPE()
    current = _dataset([1.0, 2.0, 4.0], [1.1, 1.8, 3.2])
    reference = _dataset([-1.0, -2.0, -4.0], [-0.8, -1.4, -2.4])
    snapshot = Report([metric]).run(current, reference_data=reference)
    result = snapshot.context.get_reference_metric_result(metric.to_calculation().id)

    assert snapshot.dict()["metrics"][0]["value"]["mean"] == pytest.approx(100 * 2 / 15)
    assert result.to_simple_dict() == pytest.approx({"mean": 30.0, "std": 0.1})


def test_mape_report_filters_missing_and_infinite_values():
    dataset = _dataset(
        [3.0, -0.5, 2.0, 7.0, np.nan, -1.0, np.inf, 1.0],
        [2.5, 0.0, 2.0, 8.0, 2.0, np.nan, 1.0, -np.inf],
    )
    snapshot = Report([MAPE()]).run(dataset)

    expected = 100 * mean_absolute_percentage_error([3.0, -0.5, 2.0, 7.0], [2.5, 0.0, 2.0, 8.0])
    assert snapshot.dict()["metrics"][0]["value"]["mean"] == pytest.approx(expected)
