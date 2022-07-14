import numpy as np
import pytest
from pandas import DataFrame
from pytest import approx

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


@pytest.fixture
def analyzer() -> NumTargetDriftAnalyzer:
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions(confidence=0.5))
    analyzer = NumTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def test_raises_error_when_target_non_numeric(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"another_target": ["a"] * 10 + ["b"] * 10})
    df2 = DataFrame({"another_target": ["a"] * 10 + ["b"] * 10})

    with pytest.raises(ValueError):
        analyzer.calculate(df1, df2, ColumnMapping(target="another_target"))


def test_different_target_column_name(analyzer: NumTargetDriftAnalyzer):
    reference_data = DataFrame({"another_target": range(20)})
    current_data = DataFrame({"another_target": range(20)})

    result = analyzer.calculate(reference_data, current_data, ColumnMapping(target="another_target"))
    assert result.columns.utility_columns.target == "another_target"
    assert result.target_metrics.drift_score == 1
    assert result.reference_data_count == 20
    assert result.current_data_count == 20
    assert result.target_metrics.reference_correlations == {"another_target": 1.0}
    assert result.target_metrics.current_correlations == {"another_target": 1.0}


def test_different_prediction_column_name(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"another_prediction": range(20)})
    df2 = DataFrame({"another_prediction": range(20)})

    result = analyzer.calculate(df1, df2, ColumnMapping(prediction="another_prediction"))
    assert result.prediction_metrics.column_name == "another_prediction"
    assert result.prediction_metrics.drift_score == 1
    assert result.prediction_metrics.reference_correlations == {"another_prediction": 1.0}
    assert result.prediction_metrics.current_correlations == {"another_prediction": 1.0}


def test_basic_structure_no_drift(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(20)})
    df2 = DataFrame({"target": range(20)})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == 1.0
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert result.target_metrics.current_correlations == {"target": 1.0}


def test_basic_structure_no_drift_2(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(20)})
    df2 = DataFrame({"target": range(19, -1, -1)})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    # because of ks test, target's distribution is the same, hence no drift
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == 1.0
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert result.target_metrics.current_correlations == {"target": 1.0}


def test_basic_structure_drift(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(20)})
    df2 = DataFrame({"target": range(10, 30)})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.01229, 1e-3)
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert result.target_metrics.current_correlations == {"target": 1.0}


def test_small_sample_size_1(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": [0]})
    df2 = DataFrame({"target": [10]})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.157, abs=1e-3)
    assert np.isnan(result.target_metrics.reference_correlations["target"])
    assert np.isnan(result.target_metrics.current_correlations["target"])


def test_small_sample_size_2(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": [0]})
    df2 = DataFrame({"target": range(10)})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.3636, abs=1e-3)
    assert np.isnan(result.target_metrics.reference_correlations["target"])
    assert result.target_metrics.current_correlations == {"target": 1.0}


def test_small_sample_size_3(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(10)})
    df2 = DataFrame({"target": [10]})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.1818, abs=1e-3)
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert np.isnan(result.target_metrics.current_correlations["target"])


def test_computing_of_target_and_prediction(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(10), "prediction": range(1, 11)})
    df2 = DataFrame({"target": range(5, 15), "prediction": range(2, 12)})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.16782, abs=1e-3)
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert result.target_metrics.current_correlations == {"target": 1.0}

    assert result.prediction_metrics.column_name == "prediction"
    assert result.prediction_metrics.drift_score == 1.0
    assert result.prediction_metrics.reference_correlations == {"prediction": 1.0}
    assert result.prediction_metrics.current_correlations == {"prediction": 1.0}


def test_computing_of_only_prediction(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"prediction": range(1, 11)})
    df2 = DataFrame({"prediction": range(3, 13)})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics is None
    assert result.prediction_metrics.column_name == "prediction"
    assert result.prediction_metrics.drift_score == approx(0.99445, abs=1e-3)
    assert result.prediction_metrics.reference_correlations == {"prediction": 1.0}
    assert result.prediction_metrics.current_correlations == {"prediction": 1.0}


def test_computing_with_nans(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": list(range(20)) + [np.nan, np.inf]})
    df2 = DataFrame({"target": [np.nan, np.inf] + list(range(10, 30))})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.02004, abs=1e-3)
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert result.target_metrics.current_correlations == {"target": 1.0}


def test_computing_uses_a_custom_function(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(20)})
    df2 = DataFrame({"target": range(10)})

    options = DataDriftOptions(num_target_stattest_func=lambda x, y, feature_type, threshold: (np.pi, False))
    analyzer.options_provider.add(options)
    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(np.pi, abs=1e-4)
    assert result.target_metrics.reference_correlations == {"target": 1.0}
    assert result.target_metrics.current_correlations == {"target": 1.0}


def test_computing_of_correlations_between_columns(analyzer: NumTargetDriftAnalyzer):
    df1 = DataFrame({"target": range(20), "num_1": range(0, -20, -1), "num_2": range(10, -10, -1), "cat_1": ["a"] * 20})
    df2 = DataFrame({"target": range(10), "num_1": range(0, -10, -1), "num_2": range(10, 0, -1), "cat_1": ["b"] * 10})

    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result.target_metrics.column_name == "target"
    assert result.target_metrics.drift_score == approx(0.06228, abs=1e-4)
    assert result.target_metrics.reference_correlations == {"num_1": -1.0, "num_2": -1.0, "target": 1.0}
    assert result.target_metrics.current_correlations == {"num_1": -1.0, "num_2": -1.0, "target": 1.0}


def test_computing_of_correlations_between_columns_fails_for_second_data_when_columns_missing(
    analyzer: NumTargetDriftAnalyzer,
):
    df1 = DataFrame({"target": range(20), "num_1": range(0, -20, -1), "num_2": range(10, -10, -1), "cat_1": ["a"] * 20})
    df2 = DataFrame({"target": range(10)})

    with pytest.raises(ValueError):
        analyzer.calculate(df1, df2, ColumnMapping())


def test_computing_of_correlations_between_columns_fails_for_second_data_when_columns_missing_2(
    analyzer: NumTargetDriftAnalyzer,
):
    df1 = DataFrame(
        {"prediction": range(20), "num_1": range(0, -20, -1), "num_2": range(10, -10, -1), "cat_1": ["a"] * 20}
    )
    df2 = DataFrame(
        {
            "prediction": range(10),
            "num_1": range(0, -10, -1),
        }
    )

    with pytest.raises(ValueError):
        analyzer.calculate(df1, df2, ColumnMapping())


@pytest.mark.parametrize(
    ("reference_data", "current_data"),
    (
        (
            None,
            None,
        ),
        (None, DataFrame({"target": [4, 3, 2, 1]})),
        (
            DataFrame({"target": [1, 2, 3, 4]}),
            None,
        ),
    ),
)
def test_num_target_analyzer_fails_with_not_enough_data(
    analyzer: NumTargetDriftAnalyzer,
    reference_data: DataFrame,
    current_data: DataFrame,
) -> None:
    with pytest.raises(ValueError):
        analyzer.calculate(reference_data, current_data, ColumnMapping())
