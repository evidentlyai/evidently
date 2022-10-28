import numpy as np
import pytest
from pandas import DataFrame
from pytest import approx

from evidently import ColumnMapping
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider


@pytest.fixture
def analyzer() -> CatTargetDriftAnalyzer:
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions(confidence=0.5))
    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def test_different_target_column_name(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"another_target": ["a"] * 10 + ["b"] * 10})
    df2 = DataFrame({"another_target": ["a"] * 10 + ["b"] * 10})

    result = analyzer.calculate(df1, df2, ColumnMapping(target="another_target"))
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "another_target"
    assert result.prediction_metrics is None


def test_basic_structure_no_drift(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": ["a"] * 10 + ["b"] * 10})
    df2 = DataFrame({"target": ["a"] * 10 + ["b"] * 10})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(1)
    assert result.prediction_metrics is None


def test_computing_some_drift(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": ["a"] * 10 + ["b"] * 10})
    df2 = DataFrame({"target": ["a"] * 6 + ["b"] * 15})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.1597, abs=1e-4)
    assert result.prediction_metrics is None


def test_small_sample_size(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": ["a", "b"]})
    df2 = DataFrame({"target": ["b"]})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.386, abs=1e-2)
    assert result.prediction_metrics is None


def test_different_labels_1(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": ["a", "b"]})
    df2 = DataFrame({"target": ["c"]})

    # FIXME: RuntimeWarning: divide by zero encountered in true_divide
    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.0, abs=1e-2)
    assert result.prediction_metrics is None


def test_different_labels_2(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": ["c"] * 10})
    df2 = DataFrame({"target": ["a", "b"] * 10})

    # FIXME: RuntimeWarning: divide by zero encountered in true_divide
    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.0, abs=1e-2)
    assert result.prediction_metrics is None


def test_computation_of_categories_as_numbers(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": [0, 1] * 10})
    df2 = DataFrame({"target": [1] * 5})

    # FIXME: RuntimeWarning: divide by zero encountered in true_divide
    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.04122, abs=1e-3)
    assert result.prediction_metrics is None


def test_computing_of_target_and_prediction(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"target": ["a", "b"] * 10, "prediction": ["b", "c"] * 10})
    df2 = DataFrame({"target": ["b", "c"] * 5, "prediction": ["a", "b"] * 5})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.0, abs=1e-3)
    assert result.prediction_metrics is not None
    assert result.prediction_metrics.column_name == "prediction"


def test_computing_of_only_prediction(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"another_prediction": ["b", "c"] * 10})
    df2 = DataFrame({"another_prediction": ["a", "b"] * 5})
    # FIXME: wtf: RuntimeWarning: divide by zero encountered in true_divide ?
    result = analyzer.calculate(
        df1, df2, ColumnMapping(prediction="another_prediction")
    )
    assert result.prediction_metrics is not None
    assert result.prediction_metrics.column_name == "another_prediction"
    assert result.prediction_metrics.drift_score == approx(0.0, abs=1e-3)


def test_computing_with_nans(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame(
        {
            "target": ["a"] * 10 + ["b"] * 10 + [np.nan] * 2 + [np.inf] * 2,
            "prediction": ["a"] * 10 + ["b"] * 10 + [np.nan] * 2 + [np.inf] * 2,
        }
    )
    df2 = DataFrame(
        {
            "target": ["a"] * 3 + ["b"] * 7 + [np.nan] * 2,
            "prediction": ["a"] * 3 + ["b"] * 7 + [np.nan] * 2,
        }
    )

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is not None
    assert result.prediction_metrics is not None
    assert result.target_metrics.drift_score == approx(0.29736, abs=1e-4)
    assert result.prediction_metrics.drift_score == approx(0.29736, abs=1e-4)

    df3 = DataFrame(
        {
            "target": ["a"] * 3 + ["b"] * 7 + [np.nan] * 20,
            "prediction": ["a"] * 3 + ["b"] * 7 + [np.nan] * 20,
        }
    )
    result = analyzer.calculate(df1, df3, ColumnMapping())
    assert result.target_metrics is not None
    assert result.prediction_metrics is not None
    assert result.target_metrics.drift_score == approx(0.29736, abs=1e-4)
    assert result.prediction_metrics.drift_score == approx(0.29736, abs=1e-4)


def test_computing_uses_a_custom_function(analyzer: CatTargetDriftAnalyzer) -> None:
    df1 = DataFrame({"some_column": ["a"] * 10 + ["b"] * 10})
    df2 = DataFrame({"some_column": ["a"] * 6 + ["b"] * 15})

    options = DataDriftOptions()
    options.cat_target_stattest_func = lambda x, y, feature_type, threshold: (
        np.pi,
        False,
    )
    analyzer.options_provider.add(options)
    result = analyzer.calculate(df1, df2, ColumnMapping(target="some_column"))
    assert result.target_metrics is not None
    assert result.target_metrics.drift_score == approx(np.pi, abs=1e-4)
    assert result.target_metrics.column_name == "some_column"
