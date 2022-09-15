from typing import Any
from typing import Dict
from typing import Optional

import pandas
import pytest

from evidently.model_profile.sections.classification_performance_profile_section import (
    ClassificationPerformanceProfileSection,
)

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def check_classification_performance_metrics_dict(metrics: Dict[str, Any]) -> None:
    assert "accuracy" in metrics
    assert "f1" in metrics
    assert "metrics_matrix" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "metrics_matrix" in metrics
    metrics_matrix = metrics["metrics_matrix"]
    assert isinstance(metrics_matrix, dict)
    assert "accuracy" in metrics_matrix
    assert "macro avg" in metrics_matrix
    assert "weighted avg" in metrics_matrix
    confusion_matrix = metrics["confusion_matrix"]
    assert "labels" in confusion_matrix
    assert isinstance(confusion_matrix["labels"], list)
    assert "values" in confusion_matrix
    assert isinstance(confusion_matrix["values"], list)


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(ClassificationPerformanceProfileSection, "classification_performance")


@pytest.mark.parametrize(
    "reference_data,current_data",
    (
        (pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]}), None),
        (
            pandas.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 1, 4]}),
            pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]}),
        ),
    ),
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    section_result = calculate_section_results(ClassificationPerformanceProfileSection, reference_data, current_data)
    check_profile_section_result_common_part(section_result, "classification_performance")
    result_data = section_result["data"]

    # check metrics structure and types, ignore concrete metrics values
    assert "metrics" in result_data
    metrics = result_data["metrics"]
    assert "reference" in metrics
    check_classification_performance_metrics_dict(metrics["reference"])

    if current_data is not None:
        assert "current" in metrics
        check_classification_performance_metrics_dict(metrics["current"])


@pytest.mark.parametrize(
    "reference_data, current_data",
    (
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
def test_profile_section_with_missed_target_and_prediction_columns(
    reference_data: pandas.DataFrame, current_data: pandas.DataFrame
) -> None:
    section_result = calculate_section_results(ClassificationPerformanceProfileSection, reference_data, current_data)
    check_profile_section_result_common_part(section_result, "classification_performance")
    result_data = section_result["data"]
    assert "metrics" in result_data
    assert result_data["metrics"] == {}


@pytest.mark.parametrize(
    "reference_data, current_data",
    (
        (None, None),
        (None, pandas.DataFrame({"target": [1, 1, 3, 3], "prediction": [1, 2, 1, 4]})),
    ),
)
def test_profile_section_with_missed_data(
    reference_data: Optional[pandas.DataFrame], current_data: Optional[pandas.DataFrame]
) -> None:
    with pytest.raises(ValueError):
        calculate_section_results(ClassificationPerformanceProfileSection, reference_data, current_data)
