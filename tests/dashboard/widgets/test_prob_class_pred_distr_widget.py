from typing import Optional

import pandas as pd
import pytest

from evidently.dashboard.widgets.prob_class_pred_distr_widget import (
    ProbClassPredDistrWidget,
)
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> ProbClassPredDistrWidget:
    options_provider = OptionsProvider()

    widget = ProbClassPredDistrWidget("test_widget")
    widget.options_provider = options_provider
    return widget


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, dataset, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "target": [
                        "label_a",
                        "label_a",
                        "label_a",
                        "label_b",
                        "label_b",
                        "label_b",
                    ],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                }
            ),
            None,
            ColumnMapping(
                target="target",
                prediction=["label_a", "label_b"],
            ),
            None,
            BaseWidgetInfo(type="tabbed_graph", title="test_widget", size=2),
        ),
        (
            pd.DataFrame(
                {
                    "target": [
                        "label_a",
                        "label_a",
                        "label_a",
                        "label_b",
                        "label_b",
                        "label_b",
                    ],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                }
            ),
            pd.DataFrame(
                {
                    "target": [
                        "label_a",
                        "label_a",
                        "label_a",
                        "label_b",
                        "label_b",
                        "label_b",
                    ],
                    "label_a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                    "label_b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
                }
            ),
            ColumnMapping(
                target="target",
                prediction=["label_a", "label_b"],
            ),
            "current",
            BaseWidgetInfo(type="tabbed_graph", title="test_widget", size=1),
        ),
    ),
)
def test_prob_class_pred_distr_widget_simple_case(
    widget: ProbClassPredDistrWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    dataset: Optional[str],
    expected_result: BaseWidgetInfo,
) -> None:
    if dataset is not None:
        widget.dataset = dataset

    analyzers = {}
    for analyzer_type in widget.analyzers():
        analyzer = analyzer_type()
        analyzer.options_provider = widget.options_provider
        analyzer_results = analyzer.calculate(
            reference_data, current_data, data_mapping
        )
        analyzers[analyzer_type] = analyzer_results
    result = widget.calculate(reference_data, current_data, data_mapping, analyzers)

    assert result.type == expected_result.type
    assert result.title == expected_result.title
    assert result.size == expected_result.size
    assert result.params is not None
