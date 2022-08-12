from typing import Optional

import pandas as pd

import pytest

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.widgets.cat_output_drift_widget import CatOutputDriftWidget


@pytest.fixture
def widget() -> CatOutputDriftWidget:
    options_provider = OptionsProvider()

    widget = CatOutputDriftWidget("test_cat_output_drift_widget")
    widget.options_provider = options_provider
    return widget


def test_cat_output_widget_analyzer_list(widget: CatOutputDriftWidget) -> None:
    assert widget.analyzers() == [CatTargetDriftAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, kind, expected_result",
    (
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 1]}),
            ColumnMapping(),
            None,
            BaseWidgetInfo(
                type="big_graph", title="Target Drift: not detected, drift score=0.572407 (chi-square p_value)", size=2
            ),
        ),
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 1]}),
            ColumnMapping(),
            "target",
            BaseWidgetInfo(
                type="big_graph", title="Target Drift: not detected, drift score=0.572407 (chi-square p_value)", size=2
            ),
        ),
        (
            pd.DataFrame({"data": [1, 2, 3, 4]}),
            pd.DataFrame({"data": [1, 2, 3, 1]}),
            ColumnMapping(target=None),
            "target",
            None,
        ),
        (
            pd.DataFrame({"prediction": [1, 2, 3, 4]}),
            pd.DataFrame({"prediction": [1, 2, 3, 1]}),
            ColumnMapping(),
            "prediction",
            BaseWidgetInfo(
                type="big_graph",
                title="Prediction Drift: not detected, drift score=0.572407 (chi-square p_value)",
                size=2,
            ),
        ),
        (
            pd.DataFrame({"data": [1, 2, 3, 4]}),
            pd.DataFrame({"data": [1, 2, 3, 1]}),
            ColumnMapping(prediction=None),
            "prediction",
            None,
        ),
    ),
)
def test_cat_output_widget(
    widget: CatOutputDriftWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    kind: Optional[str],
    expected_result: BaseWidgetInfo,
) -> None:
    if kind is not None:
        widget.kind = kind

    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(reference_data, current_data, data_mapping, {CatTargetDriftAnalyzer: analyzer_results})

    if expected_result is not None:
        # we have some widget for visualization
        assert result.type == expected_result.type
        assert result.title == expected_result.title
        assert result.size == expected_result.size
        assert result.params is not None

    else:
        # no widget data, show nothing
        assert result is None


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, kind",
    (
        # no current data
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            None,
            ColumnMapping(),
            None,
        ),
        # incorrect kind
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 1]}),
            ColumnMapping(),
            "some_value",
        ),
    ),
)
def test_cat_output_widget_value_error(
    widget: CatOutputDriftWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    kind: Optional[str],
) -> None:
    if kind is not None:
        widget.kind = kind

    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = widget.options_provider

    # replace None current data to reference data for passing analyzers step
    if current_data is None:
        current_data_for_analyzer = reference_data

    else:
        current_data_for_analyzer = current_data

    analyzer_results = analyzer.calculate(reference_data, current_data_for_analyzer, data_mapping)

    with pytest.raises(ValueError):
        widget.calculate(reference_data, current_data, data_mapping, {CatTargetDriftAnalyzer: analyzer_results})
