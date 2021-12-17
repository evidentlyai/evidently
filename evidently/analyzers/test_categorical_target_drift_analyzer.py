import pytest
import numpy as np
from pandas import DataFrame
from pytest import approx

from evidently import ColumnMapping
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


@pytest.fixture
def analyzer():
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions(confidence=0.5))
    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def _assert_result_structure(result) -> None:
    assert 'utility_columns' in result
    assert 'cat_feature_names' in result
    assert 'num_feature_names' in result
    assert 'target_names' in result
    assert 'metrics' in result
    assert result['metrics']['target_type'] == 'cat'


def test_different_target_column_name(analyzer) -> None:
    df1 = DataFrame({
        'another_target': ['a'] * 10 + ['b'] * 10
    })
    df2 = DataFrame({
        'another_target': ['a'] * 10 + ['b'] * 10
    })

    result = analyzer.calculate(df1, df2, ColumnMapping(target='another_target'))
    _assert_result_structure(result)
    assert result['metrics']['target_name'] == 'another_target'


def test_basic_structure_no_drift(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a'] * 10 + ['b'] * 10
    })
    df2 = DataFrame({
        'target': ['a'] * 10 + ['b'] * 10
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(1)
    assert result['metrics']['target_name'] == 'target'


def test_computing_some_drift(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a'] * 10 + ['b'] * 10
    })
    df2 = DataFrame({
        'target': ['a'] * 6 + ['b'] * 15
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0.1597, abs=1e-4)
    assert result['metrics']['target_name'] == 'target'


def test_small_sample_size(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a', 'b']
    })
    df2 = DataFrame({
        'target': ['b']
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0.386, abs=1e-2)
    assert result['metrics']['target_name'] == 'target'


def test_different_labels_1(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a', 'b']
    })
    df2 = DataFrame({
        'target': ['c']
    })

    # FIXME: RuntimeWarning: divide by zero encountered in true_divide
    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0., abs=1e-2)
    assert result['metrics']['target_name'] == 'target'


def test_different_labels_2(analyzer) -> None:
    df1 = DataFrame({
        'target': ['c'] * 10
    })
    df2 = DataFrame({
        'target': ['a', 'b'] * 10
    })

    # FIXME: RuntimeWarning: divide by zero encountered in true_divide
    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0., abs=1e-2)
    assert result['metrics']['target_name'] == 'target'


def test_computation_of_categories_as_numbers(analyzer) -> None:
    df1 = DataFrame({
        'target': [0, 1] * 10
    })
    df2 = DataFrame({
        'target': [1] * 5
    })

    # FIXME: RuntimeWarning: divide by zero encountered in true_divide
    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0.04122, abs=1e-3)
    assert result['metrics']['target_name'] == 'target'


def test_computing_of_target_and_prediction(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a', 'b'] * 10,
        'prediction': ['b', 'c'] * 10
    })
    df2 = DataFrame({
        'target': ['b', 'c'] * 5,
        'prediction': ['a', 'b'] * 5
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0., abs=1e-3)
    assert result['metrics']['prediction_name'] == 'prediction'
    assert result['metrics']['prediction_type'] == 'cat'


def test_computing_of_only_prediction(analyzer) -> None:
    df1 = DataFrame({
        'prediction': ['b', 'c'] * 10
    })
    df2 = DataFrame({
        'prediction': ['a', 'b'] * 5
    })
    # FIXME: wtf: RuntimeWarning: divide by zero encountered in true_divide ?
    result = analyzer.calculate(df1, df2, ColumnMapping())
    assert result['metrics']['prediction_drift'] == approx(0., abs=1e-3)
    assert 'utility_columns' in result
    assert 'cat_feature_names' in result
    assert 'num_feature_names' in result
    assert 'metrics' in result
    assert result['metrics']['prediction_name'] == 'prediction'
    assert result['metrics']['prediction_type'] == 'cat'


def test_computing_with_nans(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a'] * 10 + ['b'] * 10 + [np.nan] * 2 + [np.inf] * 2,
        'prediction': ['a'] * 10 + ['b'] * 10 + [np.nan] * 2 + [np.inf] * 2
    })
    df2 = DataFrame({
        'target': ['a'] * 3 + ['b'] * 7 + [np.nan] * 2,
        'prediction': ['a'] * 3 + ['b'] * 7 + [np.nan] * 2
    })

    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0.29736, abs=1e-4)
    assert result['metrics']['prediction_drift'] == approx(0.29736, abs=1e-4)
    assert result['metrics']['target_name'] == 'target'

    df3 = DataFrame({
        'target': ['a'] * 3 + ['b'] * 7 + [np.nan] * 20,
        'prediction': ['a'] * 3 + ['b'] * 7 + [np.nan] * 20
    })
    result = analyzer.calculate(df1, df3, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(0.29736, abs=1e-4)
    assert result['metrics']['prediction_drift'] == approx(0.29736, abs=1e-4)
    assert result['metrics']['target_name'] == 'target'


def test_computing_uses_a_custom_function(analyzer) -> None:
    df1 = DataFrame({
        'target': ['a'] * 10 + ['b'] * 10
    })
    df2 = DataFrame({
        'target': ['a'] * 6 + ['b'] * 15
    })

    options = DataDriftOptions()
    options.cat_target_stattest_func = lambda x, y: np.pi
    analyzer.options_provider.add(options)
    result = analyzer.calculate(df1, df2, ColumnMapping())
    _assert_result_structure(result)
    assert result['metrics']['target_drift'] == approx(np.pi, abs=1e-4)
    assert result['metrics']['target_name'] == 'target'
