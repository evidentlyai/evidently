from typing import Any
from typing import Dict

import pandas

import pytest

from evidently.model_profile.sections.regression_performance_profile_section import \
    RegressionPerformanceProfileSection

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def check_regression_performance_metrics_dict(metrics: Dict[str, Any]) -> None:
    assert 'abs_error_std' in metrics
    assert 'abs_perc_error_std' in metrics
    assert 'error_normality' in metrics
    assert 'error_std' in metrics
    assert 'mean_abs_error' in metrics
    assert 'mean_abs_perc_error' in metrics
    assert 'mean_error' in metrics
    assert 'underperformance' in metrics


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(RegressionPerformanceProfileSection, 'regression_performance')


@pytest.mark.parametrize(
    'reference_data,current_data', (
        (pandas.DataFrame({'target': [3, 5, 3, 7], 'prediction': [1, 2, 7, 4]}), None),
        (
            pandas.DataFrame({'target': [1, 9, 3, 4], 'prediction': [1, 4, 1, 4]}),
            pandas.DataFrame({'target': [1, 1, 1, 3], 'prediction': [1, 2, 1, 0]}),
        ),
    )
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    section_result = calculate_section_results(
        RegressionPerformanceProfileSection, reference_data, current_data
    )
    check_profile_section_result_common_part(section_result, 'regression_performance')
    result_data = section_result['data']

    assert 'utility_columns' in result_data

    # check metrics structure and types, ignore concrete metrics values
    assert 'metrics' in result_data
    metrics = result_data['metrics']
    assert 'error_bias' in metrics
    assert 'reference' in metrics
    reference_metrics = metrics['reference']
    check_regression_performance_metrics_dict(reference_metrics)

    if current_data is not None:
        assert 'current' in metrics
        current_metrics = metrics['current']
        check_regression_performance_metrics_dict(current_metrics)
