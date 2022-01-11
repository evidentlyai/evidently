import json

from pandas import DataFrame

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider
from evidently.profile_sections.data_drift_profile_section import DataDriftProfileSection
from evidently.utils import NumpyEncoder


def _check_feature_metrics(feature_metric: dict, feature_type: str):
    assert 'current_small_hist' in feature_metric
    assert 'feature_type' in feature_metric
    assert feature_metric['feature_type'] == feature_type
    assert 'p_value' in feature_metric
    assert 'ref_small_hist' in feature_metric


def test_data_drift_profile_section_empty_results():
    data_drift_profile_section = DataDriftProfileSection()
    assert data_drift_profile_section.analyzers() == [DataDriftAnalyzer]
    assert data_drift_profile_section.part_id() == 'data_drift'

    empty_result = data_drift_profile_section.get_results()
    assert empty_result is None


def test_data_drift_profile_section_with_calculated_results():
    # prepare calculated data
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    data_drift_analyzer = DataDriftAnalyzer()
    data_drift_analyzer.options_provider = options_provider
    test_data = DataFrame({
        'target': [1, 2, 3, 4],
        'numerical_feature': [0.5, 0.0, 4.8, 2.1],
        'categorical_feature': [1, 1, 0, 1],
    })
    data_columns = ColumnMapping(
        numerical_features=['numerical_feature'],
        categorical_features=['categorical_feature'],
        target_names=['drift_target_result']
    )
    data_drift_results = data_drift_analyzer.calculate(test_data[:2], test_data, data_columns)
    analyzers_results = {DataDriftAnalyzer: data_drift_results}

    # create data_drift_profile section with the calculated data
    data_drift_profile_section = DataDriftProfileSection()
    data_drift_profile_section.calculate(test_data[:2], test_data, data_columns, analyzers_results)
    data_drift_profile_section_result = data_drift_profile_section.get_results()
    assert 'name' in data_drift_profile_section_result
    assert data_drift_profile_section_result['name'] == 'data_drift'
    assert 'datetime' in data_drift_profile_section_result
    assert isinstance(data_drift_profile_section_result['datetime'], str)
    assert 'data' in data_drift_profile_section_result
    assert isinstance(data_drift_profile_section_result['data'], dict)

    result_data = data_drift_profile_section_result['data']

    assert 'cat_feature_names' in result_data
    assert result_data['cat_feature_names'] == ['categorical_feature']
    assert 'num_feature_names' in result_data
    assert result_data['num_feature_names'] == ['numerical_feature']
    assert 'options' in result_data
    assert 'target_names' in result_data
    assert result_data['target_names'] == ['drift_target_result']
    assert 'utility_columns' in result_data
    assert 'metrics' in result_data
    assert 'dataset_drift' in result_data['metrics']
    assert 'n_drifted_features' in result_data['metrics']
    assert 'n_features' in result_data['metrics']
    assert result_data['metrics']['n_features'] == 2
    assert 'numerical_feature' in result_data['metrics']
    _check_feature_metrics(result_data['metrics']['numerical_feature'], 'num')
    assert 'categorical_feature' in result_data['metrics']
    _check_feature_metrics(result_data['metrics']['categorical_feature'], 'cat')

    # check json serialization
    json.dumps(data_drift_profile_section_result, cls=NumpyEncoder)
