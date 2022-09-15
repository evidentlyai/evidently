import pandas as pd
from evidently.dashboard.widgets.text_widget import TextWidget
from evidently.pipeline.column_mapping import ColumnMapping


def test_text_widget_simple_case() -> None:
    reference_data = pd.DataFrame(
        {
            "test": [1, 2, 3, 1],
        }
    )

    # the widget does not use analyzers results, skip analyzers calculation

    widget = TextWidget("test_widget")
    assert widget.analyzers() == []
    result = widget.calculate(reference_data, None, ColumnMapping(), {})
    assert result is not None
    assert result.title == "Some title"
    assert result.params is not None
