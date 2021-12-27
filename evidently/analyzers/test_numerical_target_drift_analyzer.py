import numpy as np
import pytest
from pandas import DataFrame
from pytest import approx

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


@pytest.fixture
def analyzer():
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions(confidence=0.5))
    analyzer = NumTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def _assert_result_structure(result):
    assert 'utility_columns' in result
    assert 'cat_feature_names' in result
    assert 'num_feature_names' in result
    assert 'target_names' in result
    assert 'metrics' in result


def test_raises_error_when_target_non_numeric(analyzer):
    df1 = DataFrame({
        'another_target': ['a'] * 10 + ['b'] * 10
    })
    df2 = DataFrame({
        'another_target': ['a'] * 10 + ['b'] * 10
    })

    with pytest.raises(ValueError):
        analyzer.calculate(df1, df2, ColumnMapping(target='another_target'))


def test_different_target_column_name(analyzer):
    df1 = DataFrame({
        'another_target': range(20)
    })
    df2 = DataFrame({
        'another_target': range(20)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping(target='another_target'))
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'another_target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == 1
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'another_target': 1.0}
    assert correlations['current'] == {'another_target': 1.0}


def test_different_prediction_column_name(analyzer):
    df1 = DataFrame({
        'another_prediction': range(20)
    })
    df2 = DataFrame({
        'another_prediction': range(20)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping(prediction='another_prediction'))
    _assert_result_structure(result)
    assert result['metrics']['prediction_name'] == 'another_prediction'
    assert result['metrics']['prediction_type'] == 'num'
    assert result['metrics']['prediction_drift'] == 1
    correlations = result['metrics']['prediction_correlations']
    assert correlations['reference'] == {'another_prediction': 1.0}
    assert correlations['current'] == {'another_prediction': 1.0}


def test_basic_structure_no_drift(analyzer):
    df1 = DataFrame({
        'target': range(20)
    })
    df2 = DataFrame({
        'target': range(20)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == 1
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert correlations['current'] == {'target': 1.0}


def test_basic_structure_no_drift_2(analyzer):
    df1 = DataFrame({
        'target': range(20)
    })
    df2 = DataFrame({
        'target': range(19, -1, -1)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    # because of ks test, target's distribution is the same, hence no drift
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == 1
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert correlations['current'] == {'target': 1.0}


def test_basic_structure_drift(analyzer):
    df1 = DataFrame({
        'target': range(20)
    })
    df2 = DataFrame({
        'target': range(10, 30)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(0.01229, 1e-3)
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert correlations['current'] == {'target': 1.0}


def test_small_sample_size_1(analyzer):
    df1 = DataFrame({
        'target': [0]
    })
    df2 = DataFrame({
        'target': [10]
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == 1.
    correlations = result['metrics']['target_correlations']
    assert np.isnan(correlations['reference']['target'])
    assert np.isnan(correlations['current']['target'])


def test_small_sample_size_2(analyzer):
    df1 = DataFrame({
        'target': [0]
    })
    df2 = DataFrame({
        'target': range(10)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(0.3636, abs=1e-3)
    correlations = result['metrics']['target_correlations']
    assert np.isnan(correlations['reference']['target'])
    assert correlations['current'] == {'target': 1.0}


def test_small_sample_size_3(analyzer):
    df1 = DataFrame({
        'target': range(10)
    })
    df2 = DataFrame({
        'target': [10]
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(0.1818, abs=1e-3)
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert np.isnan(correlations['current']['target'])


def test_computing_of_target_and_prediction(analyzer):
    df1 = DataFrame({
        'target': range(10),
        'prediction': range(1, 11)
    })
    df2 = DataFrame({
        'target': range(5, 15),
        'prediction': range(2, 12)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['prediction_name'] == 'prediction'
    assert result['metrics']['prediction_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(0.16782, abs=1e-3)
    assert result['metrics']['prediction_drift'] == 1.
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert correlations['current'] == {'target': 1.0}
    correlations = result['metrics']['prediction_correlations']
    assert correlations['reference'] == {'prediction': 1.0}
    assert correlations['current'] == {'prediction': 1.0}


def test_computing_of_only_prediction(analyzer):
    df1 = DataFrame({
        'prediction': range(1, 11)
    })
    df2 = DataFrame({
        'prediction': range(3, 13)
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['prediction_name'] == 'prediction'
    assert result['metrics']['prediction_type'] == 'num'
    assert result['metrics']['prediction_drift'] == approx(0.99445, abs=1e-3)
    correlations = result['metrics']['prediction_correlations']
    assert correlations['reference'] == {'prediction': 1.0}
    assert correlations['current'] == {'prediction': 1.0}


def test_computing_with_nans(analyzer):
    df1 = DataFrame({
        'target': list(range(20)) + [np.nan, np.inf]
    })
    df2 = DataFrame({
        'target': [np.nan, np.inf] + list(range(10, 30))
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(0.02004, abs=1e-3)
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert correlations['current'] == {'target': 1.0}


def test_computing_uses_a_custom_function(analyzer):
    df1 = DataFrame({
        'target': range(20)
    })
    df2 = DataFrame({
        'target': range(10)
    })

    options = DataDriftOptions(num_target_stattest_func=lambda x, y: np.pi)
    analyzer.options_provider.add(options)
    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(np.pi, abs=1e-4)
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'target': 1.0}
    assert correlations['current'] == {'target': 1.0}


def test_computing_of_correlations_between_columns(analyzer):
    df1 = DataFrame({
        'target': range(20),
        'num_1': range(0, -20, -1),
        'num_2': range(10, -10, -1),
        'cat_1': ['a'] * 20
    })
    df2 = DataFrame({
        'target': range(10),
        'num_1': range(0, -10, -1),
        'num_2': range(10, 0, -1),
        'cat_1': ['b'] * 10
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'target'
    assert result['metrics']['target_type'] == 'num'
    assert result['metrics']['target_drift'] == approx(0.06228, abs=1e-4)
    correlations = result['metrics']['target_correlations']
    assert correlations['reference'] == {'num_1': -1.0, 'num_2': -1.0, 'target': 1.0}
    assert correlations['current'] == {'num_1': -1.0, 'num_2': -1.0, 'target': 1.0}


def test_computing_of_correlations_between_columns_fails_for_second_data_when_columns_missing(analyzer):
    df1 = DataFrame({
        'target': range(20),
        'num_1': range(0, -20, -1),
        'num_2': range(10, -10, -1),
        'cat_1': ['a'] * 20
    })
    df2 = DataFrame({
        'target': range(10)
    })

    with pytest.raises(ValueError):
        analyzer.calculate(df1, df2, ColumnMapping())


def test_computing_of_correlations_between_columns_fails_for_second_data_when_columns_missing_2(analyzer):
    df1 = DataFrame({
        'prediction': range(20),
        'num_1': range(0, -20, -1),
        'num_2': range(10, -10, -1),
        'cat_1': ['a'] * 20
    })
    df2 = DataFrame({
        'prediction': range(10),
        'num_1': range(0, -10, -1),
    })

    with pytest.raises(ValueError):
        analyzer.calculate(df1, df2, ColumnMapping())
