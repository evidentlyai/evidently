import pandas as pd
import pytest

from evidently.analyzers.classification_performance_analyzer import (
    ClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.class_confusion_based_feature_distr_table_widget import (
    ClassConfusionBasedFeatureDistrTable,
)
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> ClassConfusionBasedFeatureDistrTable:
    options_provider = OptionsProvider()

    widget = ClassConfusionBasedFeatureDistrTable("test_widget")
    widget.options_provider = options_provider
    return widget


def test_reg_pred_actual_widget_analyzer_list(
    widget: ClassConfusionBasedFeatureDistrTable,
) -> None:
    assert widget.analyzers() == [ClassificationPerformanceAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 3, 4],
                    "num_feature": [2, 4, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "a", "d"],
                }
            ),
            None,
            ColumnMapping(),
            BaseWidgetInfo(type="big_graph", title="test_widget", size=1),
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 3, 4],
                    "num_feature": [2, 1, 2, 5],
                    "cat_feature_1": [2, 3, 5, 5],
                    "cat_feature_2": ["a", "c", "a", "b"],
                }
            ),
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 3, 4],
                    "num_feature": [2, 1, 2, 5],
                    "cat_feature_1": [2, 3, 5, 5],
                    "cat_feature_2": ["c", "a", "d", "b"],
                }
            ),
            ColumnMapping(),
            BaseWidgetInfo(type="big_graph", title="test_widget", size=1),
        ),
    ),
)
def test_reg_pred_actual_widget_simple_case(
    widget: ClassConfusionBasedFeatureDistrTable,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    expected_result: BaseWidgetInfo,
) -> None:
    analyzer = ClassificationPerformanceAnalyzer()
    analyzer.options_provider = widget.options_provider
    column_mapping = ColumnMapping()
    results = analyzer.calculate(reference_data, current_data, column_mapping)

    assert widget.analyzers() == [ClassificationPerformanceAnalyzer]
    result = widget.calculate(
        reference_data,
        current_data,
        column_mapping,
        {ClassificationPerformanceAnalyzer: results},
    )
    assert result is not None
    assert result.title == "test_widget"
    assert result.params is not None
