import pandas as pd

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.dashboard.widgets.target_name_widget import TargetNameWidget
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping

import pytest


@pytest.mark.parametrize(
    "kind, analyzer_class, test_data, column_mapping",
    (
        (
            "regression",
            RegressionPerformanceAnalyzer,
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 2, 4],
                }
            ),
            ColumnMapping(),
        ),
        (
            "classification",
            ClassificationPerformanceAnalyzer,
            pd.DataFrame(
                {
                    "target": ["a", "b", "c", "a"],
                    "prediction": ["a", "b", "a", "a"],
                }
            ),
            ColumnMapping(),
        ),
        (
            "prob_classification",
            ProbClassificationPerformanceAnalyzer,
            pd.DataFrame(
                {
                    "target": ["label_a", "label_a", "label_a", "label_b", "label_b", "label_b"],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                }
            ),
            ColumnMapping(prediction=["label_a", "label_b"]),
        ),
    ),
)
def test_target_name_widget_simple_case(
    kind: str, analyzer_class, test_data: pd.DataFrame, column_mapping: ColumnMapping
) -> None:
    analyzer = analyzer_class()
    analyzer.options_provider = OptionsProvider()
    results = analyzer.calculate(test_data, None, column_mapping)

    widget = TargetNameWidget("test_widget", kind)
    assert widget.analyzers() == [analyzer_class]
    result = widget.calculate(test_data, None, column_mapping, {analyzer_class: results})
    assert result is not None
    assert result.title == ""
    assert result.params is not None
