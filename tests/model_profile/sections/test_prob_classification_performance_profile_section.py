from typing import Any
from typing import Dict

import pandas
import pytest

from evidently.model_profile.sections.prob_classification_performance_profile_section import (
    ProbClassificationPerformanceProfileSection,
)
from evidently.pipeline.column_mapping import ColumnMapping

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def check_prob_classification_performance_metrics_dict(metrics: Dict[str, Any]) -> None:
    assert "accuracy" in metrics
    assert "f1" in metrics
    assert "log_loss" in metrics
    assert "pr_curve" in metrics
    assert "pr_table" in metrics
    assert "precision" in metrics
    assert "roc_auc" in metrics
    assert "roc_curve" in metrics
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
    check_section_without_calculation_results(
        ProbClassificationPerformanceProfileSection, "probabilistic_classification_performance"
    )


@pytest.mark.parametrize(
    "reference_data,current_data",
    (
        (
            pandas.DataFrame(
                {
                    "my_target": ["prediction_1", "prediction_2", "prediction_1", "prediction_2"],
                    "prediction_1": [1, 0, 1, 0],
                    "prediction_2": [1, 0, 1, 0],
                }
            ),
            None,
        ),
        (
            pandas.DataFrame(
                {
                    "my_target": ["prediction_1", "prediction_2", "prediction_1", "prediction_2"],
                    "prediction_1": [1, 0, 1, 0],
                    "prediction_2": [1, 0, 1, 0],
                }
            ),
            pandas.DataFrame(
                {
                    "my_target": ["prediction_1", "prediction_2", "prediction_1", "prediction_2"],
                    "prediction_1": [1, 0, 1, 1],
                    "prediction_2": [1, 1, 1, 0],
                }
            ),
        ),
    ),
)
def test_profile_section_with_calculated_results(reference_data, current_data) -> None:
    columns_mapping = ColumnMapping(target="my_target", prediction=["prediction_1", "prediction_2"])
    section_result = calculate_section_results(
        ProbClassificationPerformanceProfileSection, reference_data, current_data, columns_mapping
    )
    check_profile_section_result_common_part(section_result, "probabilistic_classification_performance")
    result_data = section_result["data"]
    assert "options" in result_data

    # check metrics structure and types, ignore concrete metrics values
    assert "metrics" in result_data
    metrics = result_data["metrics"]
    assert "reference" in metrics
    check_prob_classification_performance_metrics_dict(metrics["reference"])

    if current_data is not None:
        assert "current" in metrics
        check_prob_classification_performance_metrics_dict(metrics["current"])

    else:
        assert "current" not in metrics


@pytest.mark.parametrize(
    "reference_data, current_data",
    (
        (None, None),
        (
            None,
            pandas.DataFrame(
                {
                    "my_target": ["prediction_1", "prediction_2", "prediction_1", "prediction_2"],
                    "prediction_1": [1, 0, 1, 1],
                    "prediction_2": [1, 1, 1, 0],
                }
            ),
        ),
    ),
)
def test_profile_section_with_missed_data(reference_data, current_data) -> None:
    with pytest.raises(ValueError):
        calculate_section_results(ProbClassificationPerformanceProfileSection, reference_data, current_data)
