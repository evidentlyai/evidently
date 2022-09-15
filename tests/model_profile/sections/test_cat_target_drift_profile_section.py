import pandas
import pytest
from evidently.model_profile.sections.cat_target_drift_profile_section import CatTargetDriftProfileSection

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(CatTargetDriftProfileSection, "cat_target_drift")


@pytest.mark.parametrize(
    "reference_data,current_data",
    (
        (
            pandas.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 1, 4]}),
            pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]}),
        ),
        (
            pandas.DataFrame({"target": [1, 2, 3, 4]}),
            pandas.DataFrame({"target": [1, 1, 3, 3]}),
        ),
        (
            pandas.DataFrame({"prediction": [1, 2, 3, 4]}),
            pandas.DataFrame({"prediction": [1, 1, 3, 3]}),
        ),
        (
            pandas.DataFrame({"other_data": [1, 2, 3, 4]}),
            pandas.DataFrame({"other_data": [1, 1, 3, 3]}),
        ),
    ),
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    is_target_data_presented = "target" in reference_data
    is_prediction_data_presented = "prediction" in reference_data

    section_result = calculate_section_results(CatTargetDriftProfileSection, reference_data, current_data)
    check_profile_section_result_common_part(section_result, "cat_target_drift")
    result_data = section_result["data"]

    # check metrics structure and types, ignore concrete metrics values
    assert "metrics" in result_data
    metrics = result_data["metrics"]

    if is_target_data_presented:
        # check target metrics
        assert "target_drift" in metrics
        assert isinstance(metrics["target_drift"], float)
        assert "target_name" in metrics
        assert metrics["target_name"] == "target"
        assert "target_type" in metrics
        assert metrics["target_type"] == "cat"

    if is_prediction_data_presented:
        # check prediction metrics
        assert "prediction_drift" in metrics
        assert isinstance(metrics["prediction_drift"], float)
        assert "prediction_name" in metrics
        assert metrics["prediction_name"] == "prediction"
        assert "prediction_type" in metrics
        assert metrics["prediction_type"] == "cat"


@pytest.mark.parametrize(
    "reference_data, current_data",
    (
        (None, None),
        (None, pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]})),
        (pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]}), None),
    ),
)
def test_profile_section_with_missed_data(reference_data, current_data) -> None:
    with pytest.raises(ValueError):
        calculate_section_results(CatTargetDriftProfileSection, reference_data, current_data)
