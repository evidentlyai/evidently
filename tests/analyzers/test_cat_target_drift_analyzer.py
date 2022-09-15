import numpy as np
import pytest
from pandas import DataFrame
from pytest import approx

from evidently import ColumnMapping
from evidently.analyzers.cat_target_drift_analyzer import \
    CatTargetDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


@pytest.fixture
def analyzer() -> CatTargetDriftAnalyzer:
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions(confidence=0.5))
    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def test_different_target_column_name(analyzer: CatTargetDriftAnalyzer):
    reference_data = DataFrame({"another_target": ["a"] * 20})
    current_data = DataFrame({"another_target": ["a"] * 20})
    result = analyzer.calculate(reference_data, current_data, ColumnMapping(target="another_target"))
    assert result.columns.utility_columns.target == "another_target"
    assert result.target_metrics.drift_score == 1
    assert result.reference_data_count == 20
    assert result.current_data_count == 20
    assert result.target_metrics.reference_correlations is None
    assert result.target_metrics.current_correlations is None
    assert result.prediction_metrics is None


def test_different_prediction_column_name(analyzer: CatTargetDriftAnalyzer):
    df1 = DataFrame({"another_prediction": ["a"] * 10})
    df2 = DataFrame({"another_prediction": ["a"] * 10})
    result = analyzer.calculate(df1, df2, ColumnMapping(prediction="another_prediction"))
    assert result.prediction_metrics.column_name == "another_prediction"
    assert result.prediction_metrics.drift_score == 1
    assert result.prediction_metrics.reference_correlations is None
    assert result.prediction_metrics.current_correlations is None


def test_computing_of_target_and_prediction(analyzer: CatTargetDriftAnalyzer):
    df1 = DataFrame({"target": ["a"] * 10, "prediction": ["a", "b"] * 5})
    df2 = DataFrame({"target": ["c"] * 10, "prediction": ["b", "c"] * 5})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.000007, abs=1e-06)
    assert result.target_metrics.reference_correlations is None
    assert result.target_metrics.current_correlations is None

    assert result.prediction_metrics.column_name == "prediction"
    assert result.prediction_metrics.drift_score == 0.0
    assert result.prediction_metrics.reference_correlations is None
    assert result.prediction_metrics.current_correlations is None


def test_prediction_is_list(analyzer: CatTargetDriftAnalyzer):
    data = DataFrame(
        {
            "a": range(5),
            "b": range(5),
        }
    )

    result = analyzer.calculate(data, data, ColumnMapping(prediction=["a", "b"]))
    assert result.target_metrics is None

    assert result.prediction_metrics.column_name == "predicted_labels"
    assert result.prediction_metrics.drift_score == 1.0
    assert result.prediction_metrics.reference_correlations is None
    assert result.prediction_metrics.current_correlations is None


def test_prediction_is_large_list(analyzer: CatTargetDriftAnalyzer):
    data = DataFrame(
        {
            "a": range(5),
            "b": range(5),
            "c": range(5),
        }
    )

    result = analyzer.calculate(data, data, ColumnMapping(prediction=["a", "b", "c"]))
    assert result.target_metrics is None

    assert result.prediction_metrics.column_name == "predicted_labels"
    assert result.prediction_metrics.drift_score == 1.0
    assert result.prediction_metrics.reference_correlations is None
    assert result.prediction_metrics.current_correlations is None
