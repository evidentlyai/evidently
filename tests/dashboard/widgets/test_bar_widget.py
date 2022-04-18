import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.widgets.bar_widget import BarWidget


def test_bar_widget_simple_case() -> None:
    reference_data = pd.DataFrame(
        {
            "test": [1, 2, 3, 1],
        }
    )

    # BarWidget do not use analyzers results, skip analyzers calculation

    widget = BarWidget("test_bar_widget")
    assert widget.analyzers() == []
    result = widget.calculate(reference_data, None, ColumnMapping(), {})
    assert result is not None
    assert result.title == "test_bar_widget"
    assert result.params is not None
