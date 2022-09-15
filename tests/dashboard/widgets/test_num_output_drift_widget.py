from typing import Optional

import pandas as pd
import pytest
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.dashboard.widgets.num_output_drift_widget import NumOutputDriftWidget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> NumOutputDriftWidget:
    options_provider = OptionsProvider()

    widget = NumOutputDriftWidget("test_widget")
    widget.options_provider = options_provider
    return widget


def test_num_target_drift_widget_analyzer_list(widget: NumOutputDriftWidget) -> None:
    assert widget.analyzers() == [NumTargetDriftAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, kind, expected_result",
    (
        (
            pd.DataFrame({"target": [1, 2, 3, 4, 5, 6, 7]}),
            pd.DataFrame({"target": [1, 2, 3, 1, 5, 6, 7]}),
            ColumnMapping(),
            None,
            BaseWidgetInfo(
                type="big_graph", title="Target Drift: not detected, drift score=0.999961 (K-S p_value)", size=2
            ),
        ),
        (
            pd.DataFrame({"target": [1, 2, 3, 4, 5, 6, 7]}),
            pd.DataFrame({"target": [1, 2, 3, 1, 5, 6, 7]}),
            ColumnMapping(),
            "target",
            BaseWidgetInfo(
                type="big_graph", title="Target Drift: not detected, drift score=0.999961 (K-S p_value)", size=2
            ),
        ),
        (
            pd.DataFrame({"data": [1, 2, 3, 4, 5, 6, 7]}),
            pd.DataFrame({"data": [1, 2, 3, 1, 5, 6, 7]}),
            ColumnMapping(target=None),
            "target",
            None,
        ),
        (
            pd.DataFrame({"prediction": [1, 2, 3, 4, 5, 6, 7]}),
            pd.DataFrame({"prediction": [1, 2, 3, 1, 5, 6, 7]}),
            ColumnMapping(),
            "prediction",
            BaseWidgetInfo(
                type="big_graph", title="Prediction Drift: not detected, drift score=0.999961 (K-S p_value)", size=2
            ),
        ),
        (
            pd.DataFrame({"data": [1, 2, 3, 4, 5, 6, 7]}),
            pd.DataFrame({"data": [1, 2, 3, 1, 5, 6, 7]}),
            ColumnMapping(prediction=None),
            "prediction",
            None,
        ),
    ),
)
def test_num_target_drift_widget_simple_case(
    widget: NumOutputDriftWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    kind: Optional[str],
    expected_result: BaseWidgetInfo,
) -> None:
    if kind is not None:
        widget.kind = kind

    analyzer = NumTargetDriftAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(reference_data, current_data, data_mapping, {NumTargetDriftAnalyzer: analyzer_results})

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
        # incorrect kind
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            None,
            ColumnMapping(),
            "other",
        ),
        # incorrect kind
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            ColumnMapping(),
            "other",
        ),
    ),
)
def test_cat_output_widget_value_error(
    widget: NumOutputDriftWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    kind: Optional[str],
) -> None:
    if kind is not None:
        widget.kind = kind

    analyzer = NumTargetDriftAnalyzer()
    analyzer.options_provider = widget.options_provider

    # replace None current data to reference data for passing analyzers step
    if current_data is None:
        current_data_for_analyzer = reference_data

    else:
        current_data_for_analyzer = current_data

    analyzer_results = analyzer.calculate(reference_data, current_data_for_analyzer, data_mapping)

    with pytest.raises(ValueError):
        widget.calculate(reference_data, current_data, data_mapping, {NumTargetDriftAnalyzer: analyzer_results})
