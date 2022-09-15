import pandas as pd

from evidently.dashboard.widgets.expandable_list_widget import \
    ExpandableListWidget
from evidently.pipeline.column_mapping import ColumnMapping


def test_expandable_list__widget_simple_case() -> None:
    reference_data = pd.DataFrame(
        {
            "test": [1, 2, 3, 1],
        }
    )

    # the widget does not use analyzers results, skip analyzers calculation

    widget = ExpandableListWidget("test_widget")
    assert widget.analyzers() == []
    result = widget.calculate(reference_data, None, ColumnMapping(), {})
    assert result is not None
    assert result.title == ""
    assert result.params is None
