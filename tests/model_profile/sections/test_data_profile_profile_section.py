import pandas

from evidently.analyzers.utils import ColumnMapping
from evidently.model_profile.sections.data_profile_profile_section import DataProfileProfileSection

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(DataProfileProfileSection, "data_profile")


def test_data_profile_profile_section_with_calculated_results():
    reference_data = pandas.DataFrame(
        {
            "target": [1, 2, 3, 4],
            "numerical_feature": [0.5, 0.0, 4.8, 2.1],
            "categorical_feature": [1, 1, 0, 1],
        }
    )
    data_columns = ColumnMapping(
        numerical_features=["numerical_feature"],
        categorical_features=["categorical_feature"],
        target_names=["drift_target_result"],
    )
    data_drift_profile_section_result = calculate_section_results(
        DataProfileProfileSection, reference_data, reference_data, data_columns
    )
    check_profile_section_result_common_part(data_drift_profile_section_result, "data_profile")
    result_data = data_drift_profile_section_result["data"]

    # check metrics
    assert "metrics" in result_data
    assert "reference" in result_data["metrics"]
    assert "current" in result_data["metrics"]

    assert result_data["metrics"]["reference"] == {
        "categorical_feature": {
            "count": 4,
            "feature_type": "cat",
            "missing": 0,
            "missing (%)": 0.0,
            "most common value": 1,
            "most common value (%)": 0.75,
            "unique": 2,
            "unique (%)": 0.5,
        },
        "numerical_feature": {
            "25%": 0.38,
            "50%": 1.3,
            "75%": 2.78,
            "count": 4.0,
            "feature_type": "num",
            "infinite": 0,
            "infinite (%)": 0.0,
            "max": 4.8,
            "mean": 1.85,
            "min": 0.0,
            "missing": 0,
            "missing (%)": 0.0,
            "most common value": 2.1,
            "most common value (%)": 0.25,
            "std": 2.16,
            "unique": 4,
            "unique (%)": 1.0,
        },
        "target": {
            "25%": 1.75,
            "50%": 2.5,
            "75%": 3.25,
            "count": 4.0,
            "feature_type": "num",
            "infinite": 0,
            "infinite (%)": 0.0,
            "max": 4.0,
            "mean": 2.5,
            "min": 1.0,
            "missing": 0,
            "missing (%)": 0.0,
            "most common value": 4,
            "most common value (%)": 0.25,
            "std": 1.29,
            "unique": 4,
            "unique (%)": 1.0,
        },
    }
