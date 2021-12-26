import pytest
from pandas import DataFrame

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


@pytest.fixture
def analyzer() -> DataDriftAnalyzer:
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    analyzer = DataDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def _check_feature_metrics(feature_metric: dict, feature_type: str):
    assert 'current_small_hist' in feature_metric
    assert 'feature_type' in feature_metric
    assert feature_metric['feature_type'] == feature_type
    assert 'p_value' in feature_metric
    assert 'ref_small_hist' in feature_metric


def test_data_drift_analyzer_as_dict_format(analyzer: DataDriftAnalyzer) -> None:
    test_data = DataFrame({
        'target': [1, 2, 3, 4],
        'numerical_feature_1': [0.5, 0.0, 4.8, 2.1],
        'numerical_feature_2': [0, 5, 6, 3],
        'numerical_feature_3': [4, 5.5, 4, 0],
        'categorical_feature_1': [1, 1, 0, 1],
        'categorical_feature_2': [0, 1, 0, 0],
    })

    data_columns = ColumnMapping()
    data_columns.numerical_features = ['numerical_feature_1', 'numerical_feature_2']
    data_columns.categorical_features = ['categorical_feature_1', 'categorical_feature_2']
    data_columns.target_names = ['drift_target']
    result = analyzer.calculate(test_data[:2], test_data, data_columns)
    result_as_dict = result.as_dict()
    assert 'cat_feature_names' in result_as_dict
    assert result_as_dict['cat_feature_names'] == ['categorical_feature_1', 'categorical_feature_2']
    assert 'num_feature_names' in result_as_dict
    assert result_as_dict['num_feature_names'] == ['numerical_feature_1', 'numerical_feature_2']

    assert 'options' in result_as_dict
    assert 'target_names' in result_as_dict
    assert result_as_dict['target_names'] == ['drift_target']
    assert 'utility_columns' in result_as_dict

    assert 'metrics' in result_as_dict
    assert 'dataset_drift' in result_as_dict['metrics']
    assert 'n_drifted_features' in result_as_dict['metrics']
    assert 'n_features' in result_as_dict['metrics']
    assert result_as_dict['metrics']['n_features'] == 4
    assert 'dataset_drift' in result_as_dict['metrics']

    assert 'numerical_feature_1' in result_as_dict['metrics']
    _check_feature_metrics(result_as_dict['metrics']['numerical_feature_1'], 'num')
    assert 'numerical_feature_2' in result_as_dict['metrics']
    _check_feature_metrics(result_as_dict['metrics']['numerical_feature_2'], 'num')
    assert 'categorical_feature_1' in result_as_dict['metrics']
    _check_feature_metrics(result_as_dict['metrics']['categorical_feature_1'], 'cat')
    assert 'categorical_feature_2' in result_as_dict['metrics']
    _check_feature_metrics(result_as_dict['metrics']['categorical_feature_2'], 'cat')
