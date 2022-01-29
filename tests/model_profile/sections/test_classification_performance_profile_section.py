from typing import Any
from typing import Dict

import pandas
import pytest

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model_profile.sections.classification_performance_profile_section import \
    ClassificationPerformanceProfileSection
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping

from .helpers import check_profile_section_result_common_part
from .helpers import check_section_no_calculation_results


def get_section_results(reference_data, current_data) -> dict:
    options_provider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    analyzer = ClassificationPerformanceAnalyzer()
    analyzer.options_provider = options_provider
    data_columns = ColumnMapping()
    analyzers_results = {
        ClassificationPerformanceAnalyzer: analyzer.calculate(reference_data, current_data, data_columns)
    }
    profile_section = ClassificationPerformanceProfileSection()
    profile_section.calculate(reference_data, current_data, data_columns, analyzers_results)
    return profile_section.get_results()


def check_classification_performance_metrics_dict(metrics: Dict[str, Any]) -> None:
    assert 'accuracy' in metrics
    assert 'f1' in metrics
    assert 'metrics_matrix' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'metrics_matrix' in metrics
    metrics_matrix = metrics['metrics_matrix']
    assert isinstance(metrics_matrix, dict)
    assert 'accuracy' in metrics_matrix
    assert 'macro avg' in metrics_matrix
    assert 'weighted avg' in metrics_matrix
    confusion_matrix = metrics['confusion_matrix']
    assert 'labels' in confusion_matrix
    assert isinstance(confusion_matrix['labels'], list)
    assert 'values' in confusion_matrix
    assert isinstance(confusion_matrix['values'], list)


def test_no_calculation_results() -> None:
    check_section_no_calculation_results(ClassificationPerformanceProfileSection, 'classification_performance')


@pytest.mark.parametrize(
    'reference_data,current_data', (
        (pandas.DataFrame({'target': [1, 1, 3, 3], 'prediction': [1, 2, 1, 4]}), None),
        (
            pandas.DataFrame({'target': [1, 2, 3, 4], 'prediction': [1, 2, 1, 4]}),
            pandas.DataFrame({'target': [1, 1, 3, 3], 'prediction': [1, 2, 1, 4]}),
        ),
    )
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    section_result = get_section_results(reference_data, current_data)
    check_profile_section_result_common_part(section_result, 'classification_performance')
    result_data = section_result['data']

    assert 'utility_columns' in result_data
    assert 'date' in result_data['utility_columns']
    assert result_data['utility_columns']['date'] is None
    assert 'id' in result_data['utility_columns']
    assert result_data['utility_columns']['id'] is None
    assert 'target' in result_data['utility_columns']
    assert result_data['utility_columns']['target'] == 'target'
    assert 'prediction' in result_data['utility_columns']
    assert result_data['utility_columns']['prediction'] == 'prediction'

    # check metrics structure and types, ignore concrete metrics values
    assert 'metrics' in result_data
    metrics = result_data['metrics']
    assert 'reference' in metrics
    check_classification_performance_metrics_dict(metrics['reference'])

    if current_data is not None:
        assert 'current' in metrics
        check_classification_performance_metrics_dict(metrics['current'])


@pytest.mark.parametrize(
    'reference_data, current_data',
    (
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
def test_profile_section_with_incorrect_data(reference_data, current_data) -> None:
    section_result = get_section_results(reference_data, current_data)
    check_profile_section_result_common_part(section_result, 'classification_performance')
    result_data = section_result['data']
    assert 'metrics' in result_data
    assert result_data['metrics'] == {}


@pytest.mark.skip('TODO: fix errors for analyzers and sections if reference_data is missed')
@pytest.mark.parametrize(
    'reference_data, current_data',
    (
        (None, None),
        (None, pandas.DataFrame({'target': [1, 1, 3, 3], 'prediction': [1, 2, 1, 4]})),
    )
)
def test_profile_section_with_missed_data(reference_data, current_data) -> None:
    with pytest.raises(ValueError):
        get_section_results(reference_data, current_data)  # noqa
