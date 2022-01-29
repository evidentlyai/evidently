import pandas

import pytest

from evidently.model_profile.sections.prob_classification_performance_profile_section import \
    ProbClassificationPerformanceProfileSection

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(
        ProbClassificationPerformanceProfileSection, 'probabilistic_classification_performance'
    )


@pytest.mark.skip('TODO: fix after ProbClassificationPerformanceAnalyzer fix')
@pytest.mark.parametrize(
    'reference_data,current_data', (
        (
            pandas.DataFrame({'target': [1, 0, 1, 0], 'prediction': [1, 0, 1, 0]}),
            pandas.DataFrame({'target': [1, 1, 0, 0], 'prediction': [1, 1, 1, 1]}),
        ),
    )
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    section_result = calculate_section_results(
        ProbClassificationPerformanceProfileSection, reference_data, current_data
    )
    check_profile_section_result_common_part(section_result, 'probabilistic_classification_performance')
    result_data = section_result['data']

    # check metrics structure and types, ignore concrete metrics values
    assert 'metrics' in result_data
    metrics = result_data['metrics']
    assert metrics == {}
