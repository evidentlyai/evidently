from typing import Optional

import pandas as pd
import pytest

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.dashboard.widgets.reg_pred_vs_actual_widget import RegPredActualWidget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> RegPredActualWidget:
    options_provider = OptionsProvider()

    widget = RegPredActualWidget("test_widget")
    widget.options_provider = options_provider
    return widget


def test_reg_pred_actual_widget_analyzer_list(widget: RegPredActualWidget) -> None:
    assert widget.analyzers() == [RegressionPerformanceAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, dataset, expected_result",
    (
        (
            pd.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 3, 4]}),
            None,
            ColumnMapping(),
            None,
            BaseWidgetInfo(type="big_graph", title="test_widget", size=1),
        ),
        (
            pd.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 3, 4]}),
            ColumnMapping(),
            "reference",
            BaseWidgetInfo(type="big_graph", title="test_widget", size=1),
        ),
    ),
)
def test_reg_pred_actual_widget_simple_case(
    widget: RegPredActualWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    dataset: Optional[str],
    expected_result: BaseWidgetInfo,
) -> None:
    if dataset is not None:
        widget.dataset = dataset

    analyzer = RegressionPerformanceAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(
        reference_data,
        current_data,
        data_mapping,
        {RegressionPerformanceAnalyzer: analyzer_results},
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
