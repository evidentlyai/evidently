import pandas as pd
import pytest

from evidently.dashboard.widgets.class_target_name_widget import ClassTargetNameWidget
from evidently.pipeline.column_mapping import ColumnMapping


def test_class_target_name_widget_simple_case() -> None:
    reference_data = pd.DataFrame(
        {
            "target": [1, 2, 3, 1],
            "prediction": [2, 2, 3, 1],
        }
    )

    # the widget does not use analyzers results, skip analyzers calculation

    widget = ClassTargetNameWidget("test_widget")
    assert widget.analyzers() == []
    result = widget.calculate(reference_data, None, ColumnMapping(), {})
    assert result is not None
    assert result.title == "test_widget"
    assert result.params is not None


@pytest.mark.parametrize(
    "reference_data, column_mapping",
    (
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 1],
                    "prediction": [2, 2, 3, 1],
                }
            ),
            ColumnMapping(target=None),
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 1],
                    "prediction": [2, 2, 3, 1],
                }
            ),
            ColumnMapping(prediction=None),
        ),
    ),
)
def test_class_target_name_widget_value_error(
    reference_data: pd.DataFrame, column_mapping: ColumnMapping
) -> None:
    widget = ClassTargetNameWidget("test_widget")
    with pytest.raises(ValueError):
        widget.calculate(reference_data, None, column_mapping, {})
