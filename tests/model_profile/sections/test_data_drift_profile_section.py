import pandas

from evidently import ColumnMapping
from evidently.model_profile.sections.data_drift_profile_section import DataDriftProfileSection

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def _check_feature_metrics(feature_metric: dict, feature_type: str):
    assert 'current_small_hist' in feature_metric
    assert 'feature_type' in feature_metric
    assert feature_metric['feature_type'] == feature_type
    assert 'p_value' in feature_metric
    assert 'ref_small_hist' in feature_metric


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(DataDriftProfileSection, 'data_drift')


def test_data_drift_profile_section_with_calculated_results():
    current_data = pandas.DataFrame({
        'target': [1, 2, 3, 4],
        'numerical_feature': [0.5, 0.0, 4.8, 2.1],
        'categorical_feature': [1, 1, 0, 1],
    })
    reference_data = current_data[:2]
    data_columns = ColumnMapping(
        numerical_features=['numerical_feature'],
        categorical_features=['categorical_feature'],
        target_names=['drift_target_result']
    )
    data_drift_profile_section_result = calculate_section_results(DataDriftProfileSection, reference_data, current_data, data_columns)

    data_columns = ColumnMapping(
        numerical_features=['numerical_feature'],
        categorical_features=['categorical_feature'],
        target_names=['drift_target_result']
    )

    check_profile_section_result_common_part(data_drift_profile_section_result, 'data_drift')
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
