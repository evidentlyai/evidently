import pandas

import pytest

from evidently.model_profile.sections.num_target_drift_profile_section import NumTargetDriftProfileSection
from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(NumTargetDriftProfileSection, "num_target_drift")


@pytest.mark.parametrize(
    "reference_data,current_data",
    (
        (
            pandas.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 1, 4]}),
            pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]}),
        ),
        (
            pandas.DataFrame({"prediction": [1, 2, 1, 4]}),
            pandas.DataFrame({"prediction": [1, 2, 1, 4]}),
        ),
        (
            pandas.DataFrame({"target": [1, 2, 1, 4]}),
            pandas.DataFrame({"target": [1, 2, 1, 4]}),
        ),
    ),
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    is_target_data_presented = "target" in reference_data
    is_prediction_data_presented = "prediction" in reference_data
    section_result = calculate_section_results(NumTargetDriftProfileSection, reference_data, current_data)
    check_profile_section_result_common_part(section_result, "num_target_drift")
    result_data = section_result["data"]

    # check metrics structure and types, ignore concrete metrics values
    assert "metrics" in result_data
    metrics = result_data["metrics"]

    if is_target_data_presented:
        assert "target_correlations" in metrics
        assert "target_drift" in metrics
        assert "target_name" in metrics
        assert "target_type" in metrics
        assert metrics["target_type"] == "num"

    if is_prediction_data_presented:
        assert "prediction_correlations" in metrics
        assert "prediction_drift" in metrics
        assert "prediction_name" in metrics
        assert "prediction_type" in metrics
        assert metrics["prediction_type"] == "num"
