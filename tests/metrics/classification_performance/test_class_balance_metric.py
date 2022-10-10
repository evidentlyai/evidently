import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.class_balance_metric import ClassificationClassBalance


@pytest.mark.parametrize(
    "reference, current, expected_reference, expected_current",
    [
        (
            None,
            pd.DataFrame(data=dict(target=["a", "a", "a", "b", "b", "b", "c", "c", "c"])),
            None,
            dict(a=3, b=3, c=3),
        ),
        (
            pd.DataFrame(data=dict(target=["a", "a", "b", "b", "b", "c", "c", "c", "c"])),
            pd.DataFrame(data=dict(target=["a", "a", "a", "b", "b", "b", "c", "c", "c"])),
            dict(a=2, b=3, c=4),
            dict(a=3, b=3, c=3),
        ),
    ],
)
def test_class_balance_metric(reference, current, expected_reference, expected_current):
    metric = ClassificationClassBalance()
    results = metric.calculate(
        data=InputData(
            reference_data=reference,
            current_data=current,
            column_mapping=ColumnMapping(),
        )
    )
    assert results.reference_label_count == expected_reference
    assert results.current_label_count == expected_current
