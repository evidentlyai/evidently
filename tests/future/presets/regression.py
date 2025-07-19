import pandas as pd
import pytest

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import Regression
from evidently.core.metric_types import MeanStdMetricTests
from evidently.core.report import Report
from evidently.presets import RegressionQuality
from evidently.tests import lt


@pytest.mark.parametrize(
    "preset,expected_tests",
    [
        (RegressionQuality(), 0),
        (RegressionQuality(mean_error_tests=MeanStdMetricTests(mean=[lt(0.1)])), 1),
        (RegressionQuality(mean_error_tests=[lt(0.1)]), 1),
        (RegressionQuality(mean_error_tests=MeanStdMetricTests(std=[lt(0.1)])), 1),
        (RegressionQuality(mae_tests=MeanStdMetricTests(mean=[lt(0.1)])), 1),
        (RegressionQuality(mae_tests=MeanStdMetricTests(std=[lt(0.1)])), 1),
        (RegressionQuality(mape_tests=MeanStdMetricTests(mean=[lt(0.1)])), 1),
        (RegressionQuality(mape_tests=MeanStdMetricTests(std=[lt(0.1)])), 1),
        (RegressionQuality(rmse_tests=[lt(0.1)]), 1),
        (RegressionQuality(r2score_tests=[lt(0.1)]), 1),
        (RegressionQuality(abs_max_error_tests=[lt(0.1)]), 1),
        (RegressionQuality(abs_max_error_tests=[lt(0.1)], include_tests=False), 1),
        (RegressionQuality(abs_max_error_tests=[lt(0.1)], include_tests=True), 1),
        (RegressionQuality(include_tests=True), 0),
    ],
)
def test_regression_quality_preset_tests(preset, expected_tests):
    report = Report([preset])
    dataset = Dataset.from_pandas(
        pd.DataFrame(data=dict(target=[1, 2, 3, 4, 5], prediction=[0, 1, 2, 3, 4])),
        data_definition=DataDefinition(regression=[Regression()]),
    )
    snapshot = report.run(dataset)
    snapshot_data = snapshot.dict()
    assert len(snapshot_data["tests"]) == expected_tests


@pytest.mark.parametrize(
    "preset,expected_tests",
    [
        (RegressionQuality(), 6),
        (RegressionQuality(abs_max_error_tests=[lt(0.1)], include_tests=False), 1),
        (RegressionQuality(abs_max_error_tests=[], include_tests=True), 5),
        (RegressionQuality(include_tests=True), 6),
        (RegressionQuality(include_tests=False), 0),
    ],
)
def test_test_regression_quality_preset_tests_with_reference(preset, expected_tests):
    report = Report([preset], include_tests=True)
    dataset = Dataset.from_pandas(
        pd.DataFrame(data=dict(target=[1, 2, 3, 4, 5], prediction=[0, 1, 2, 3, 4])),
        data_definition=DataDefinition(regression=[Regression()]),
    )
    snapshot = report.run(dataset, reference_data=dataset)
    snapshot_data = snapshot.dict()
    assert len(snapshot_data["tests"]) == expected_tests
