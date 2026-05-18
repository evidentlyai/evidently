import pandas as pd

from evidently import Report
from evidently.metrics import GroupBy
from evidently.metrics.column_statistics import ValueDrift, ValueDriftCalculation


def _make_datasets():
    current = pd.DataFrame({"col1": [float(i) for i in range(30)], "group": (["a", "b"] * 15)})
    reference = pd.DataFrame({"col1": [float(i) + 0.5 for i in range(30)], "group": (["a", "b"] * 15)})
    return current, reference


def test_group_by_value_drift_widget_title_includes_group_context():
    """Widget counter label must include 'group by' info when wrapped in GroupBy."""
    current, reference = _make_datasets()

    captured_titles = []
    original_render = ValueDriftCalculation._render

    def capturing_render(self, result, options, color_options, title=None):
        captured_titles.append(title)
        return original_render(self, result, options, color_options, title=title)

    ValueDriftCalculation._render = capturing_render
    try:
        report = Report([GroupBy(ValueDrift(column="col1"), "group")])
        report.run(current_data=current, reference_data=reference)
    finally:
        ValueDriftCalculation._render = original_render

    assert len(captured_titles) == 2
    for title in captured_titles:
        assert "group by 'group'" in title, f"Expected 'group by' in title, got: {title!r}"
        assert "for label:" in title, f"Expected 'for label:' in title, got: {title!r}"


def test_standalone_value_drift_widget_title():
    """Standalone ValueDrift widget label uses the metric display_name."""
    current = pd.DataFrame({"col1": [float(i) for i in range(30)]})
    reference = pd.DataFrame({"col1": [float(i) + 0.5 for i in range(30)]})

    captured_titles = []
    original_render = ValueDriftCalculation._render

    def capturing_render(self, result, options, color_options, title=None):
        captured_titles.append(title)
        return original_render(self, result, options, color_options, title=title)

    ValueDriftCalculation._render = capturing_render
    try:
        report = Report([ValueDrift(column="col1")])
        report.run(current_data=current, reference_data=reference)
    finally:
        ValueDriftCalculation._render = original_render

    assert len(captured_titles) == 1
    assert "col1" in captured_titles[0]
    assert "group by" not in captured_titles[0]
