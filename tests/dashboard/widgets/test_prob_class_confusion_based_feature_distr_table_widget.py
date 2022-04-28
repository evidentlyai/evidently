from typing import Optional

import pandas as pd

import pytest

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.widgets.prob_class_confusion_based_feature_distr_table_widget import (
    ProbClassConfusionBasedFeatureDistrTable,
)


@pytest.fixture
def widget() -> ProbClassConfusionBasedFeatureDistrTable:
    options_provider = OptionsProvider()

    widget = ProbClassConfusionBasedFeatureDistrTable("test_widget")
    widget.options_provider = options_provider
    return widget


def test_prob_class_conf_distr_table_widget_analyzer_list(widget: ProbClassConfusionBasedFeatureDistrTable) -> None:
    assert widget.analyzers() == [ProbClassificationPerformanceAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, dataset, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "target": ["label_a", "label_a", "label_a", "label_b", "label_b", "label_b"],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                    "num_feature": [2, 4, 3, 5, 3, 1],
                    "cat_feature_1": [2, 4, 3, 5, 1, 2],
                    "cat_feature_2": ["a", "b", "a", "d", "a", "c"],
                }
            ),
            None,
            ColumnMapping(
                target="target",
                prediction=["label_a", "label_b"],
                numerical_features=["num_feature"],
                categorical_features=["cat_feature_1", "cat_feature_2"],
            ),
            None,
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame(
                {
                    "target": ["label_a", "label_a", "label_a", "label_b", "label_b", "label_b"],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                    "num_feature": [2, 4, 3, 5, 3, 1],
                    "cat_feature_1": [2, 4, 3, 5, 1, 2],
                    "cat_feature_2": ["a", "b", "a", "d", "a", "c"],
                }
            ),
            pd.DataFrame(
                {
                    "target": ["label_a", "label_a", "label_a", "label_b", "label_b", "label_b"],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                    "num_feature": [2, 4, 3, 5, 3, 1],
                    "cat_feature_1": [2, 4, 3, 5, 1, 2],
                    "cat_feature_2": ["a", "b", "a", "d", "a", "c"],
                }
            ),
            ColumnMapping(
                target="target",
                prediction=["label_a", "label_b"],
                numerical_features=["num_feature"],
                categorical_features=["cat_feature_1", "cat_feature_2"],
            ),
            "current",
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
    ),
)
def test_prob_class_conf_distr_table_widget_simple_case(
    widget: ProbClassConfusionBasedFeatureDistrTable,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    dataset: Optional[str],
    expected_result: BaseWidgetInfo,
) -> None:
    if dataset is not None:
        widget.dataset = dataset

    analyzer = ProbClassificationPerformanceAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(
        reference_data, current_data, data_mapping, {ProbClassificationPerformanceAnalyzer: analyzer_results}
    )

    assert result.type == expected_result.type
    assert result.title == expected_result.title
    assert result.size == expected_result.size
    assert result.params is not None
