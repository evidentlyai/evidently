import pandas as pd

import pytest

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.widgets.reg_underperform_segments_table_widget import UnderperformSegmTableWidget


@pytest.fixture
def widget() -> UnderperformSegmTableWidget:
    options_provider = OptionsProvider()

    widget = UnderperformSegmTableWidget("test_widget")
    widget.options_provider = options_provider
    return widget


def test_reg_underperform_segments_table_widget_analyzer_list(widget: UnderperformSegmTableWidget) -> None:
    assert widget.analyzers() == [RegressionPerformanceAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 3, 4],
                    "num_feature": [2, 4, 3, 5],
                    "cat_feature": [2, 4, 3, 5],
                }
            ),
            None,
            ColumnMapping(numerical_features=["num_feature"], categorical_features=["cat_feature"]),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 3, 4],
                    "num_feature": [3, 5, 3, 1],
                    "cat_feature": [3, 5, 1, 2],
                }
            ),
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "prediction": [1, 2, 3, 4],
                    "num_feature": [2, 4, 3, 1],
                    "cat_feature": [2, 5, 1, 2],
                }
            ),
            ColumnMapping(numerical_features=["num_feature"], categorical_features=["cat_feature"]),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
    ),
)
def test_reg_underperform_segments_table_widget_simple_case(
    widget: UnderperformSegmTableWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    expected_result: BaseWidgetInfo,
) -> None:
    analyzer = RegressionPerformanceAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(
        reference_data, current_data, data_mapping, {RegressionPerformanceAnalyzer: analyzer_results}
    )

    if expected_result is not None:
        # we have some widget for visualization
        assert result.type == expected_result.type
        assert result.title == expected_result.title
        assert result.size == expected_result.size
        assert result.params is not None

    else:
        # no widget data, show nothing
        assert result is None
