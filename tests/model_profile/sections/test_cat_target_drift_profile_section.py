import pandas

import pytest

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model_profile.sections.cat_target_drift_profile_section import CatTargetDriftProfileSection
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping

from .helpers import check_profile_section_result_common_part
from .helpers import check_section_no_calculation_results


def test_no_calculation_results() -> None:
    check_section_no_calculation_results(CatTargetDriftProfileSection, 'cat_target_drift')


@pytest.mark.parametrize(
    'reference_data,current_data', (
        (
            pandas.DataFrame({'target': [1, 2, 3, 4], 'prediction': [1, 2, 1, 4]}),
            pandas.DataFrame({'target': [1, 1, 3, 3], 'prediction': [1, 2, 1, 4]}),
        ),
        (
            pandas.DataFrame({'target': [1, 2, 3, 4]}),
            pandas.DataFrame({'target': [1, 1, 3, 3]}),
        ),
        (
            pandas.DataFrame({'prediction': [1, 2, 3, 4]}),
            pandas.DataFrame({'prediction': [1, 1, 3, 3]}),
        ),
        (
            pandas.DataFrame({'other_data': [1, 2, 3, 4]}),
            pandas.DataFrame({'other_data': [1, 1, 3, 3]}),
        )
    )
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    is_target_data_presented = 'target' in reference_data
    is_prediction_data_presented = 'prediction' in reference_data
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    data_columns = ColumnMapping()
    analyzers_results = {CatTargetDriftAnalyzer: analyzer.calculate(reference_data, current_data, data_columns)}
    profile_section = CatTargetDriftProfileSection()
    profile_section.calculate(reference_data, current_data, data_columns, analyzers_results)
    section_result = profile_section.get_results()
    check_profile_section_result_common_part(section_result, 'cat_target_drift')
    result_data = section_result['data']

    assert 'cat_feature_names' in result_data
    assert isinstance(result_data['cat_feature_names'], list)
    assert 'num_feature_names' in result_data
    assert isinstance(result_data['num_feature_names'], list)
    assert 'target_names' in result_data
    assert result_data['target_names'] is None
    assert 'utility_columns' in result_data
    assert 'date' in result_data['utility_columns']
    assert result_data['utility_columns']['date'] is None
    assert 'id' in result_data['utility_columns']
    assert result_data['utility_columns']['id'] is None
    assert 'target' in result_data['utility_columns']

    if is_target_data_presented:
        assert result_data['utility_columns']['target'] == 'target'

    else:
        assert result_data['utility_columns']['target'] is None

    assert 'target' in result_data['utility_columns']

    if is_prediction_data_presented:
        assert result_data['utility_columns']['prediction'] == 'prediction'

    else:
        assert result_data['utility_columns']['prediction'] is None

    # check metrics structure and types, ignore concrete metrics values
    assert 'metrics' in result_data
    metrics = result_data['metrics']

    if is_target_data_presented:
        # check target metrics
        assert 'target_drift' in metrics
        assert isinstance(metrics['target_drift'], float)
        assert 'target_name' in metrics
        assert metrics['target_name'] == 'target'
        assert 'target_type' in metrics
        assert metrics['target_type'] == 'cat'

    if is_prediction_data_presented:
        # check prediction metrics
        assert 'prediction_drift' in metrics
        assert isinstance(metrics['prediction_drift'], float)
        assert 'prediction_name' in metrics
        assert metrics['prediction_name'] == 'prediction'
        assert 'prediction_type' in metrics
        assert metrics['prediction_type'] == 'cat'


@pytest.mark.skip('TODO: fix errors for analyzers and sections if reference_data or current_data is missed')
@pytest.mark.parametrize(
    'reference_data, current_data',
    (
        (None, None),
        (None, pandas.DataFrame({'target': [1, 1, 3, 3], 'prediction': [1, 2, 1, 4]})),
        (pandas.DataFrame({'target': [1, 1, 3, 3], 'prediction': [1, 2, 1, 4]}), None),
    )
)
def test_profile_section_with_missed_data(reference_data, current_data) -> None:
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = options_provider
    data_columns = ColumnMapping()
    profile_section = CatTargetDriftProfileSection()

    with pytest.raises(ValueError):
        analyzers_results = {CatTargetDriftAnalyzer: analyzer.calculate(reference_data, current_data, data_columns)}
        profile_section.calculate(reference_data, current_data, data_columns, analyzers_results)
