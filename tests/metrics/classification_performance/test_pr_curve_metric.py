import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import ClassificationPRCurve
from evidently.metrics.base_metric import InputData


def test_roc_curve_no_exceptions():
    current = pd.DataFrame(
        data=dict(
            target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            a=[0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
            b=[0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
            c=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
        ),
    )
    m2 = ClassificationPRCurve()
    result = m2.calculate(
        data=InputData(
            reference_data=None,
            current_data=current,
            column_mapping=ColumnMapping(prediction=["a", "b", "c"]),
        )
    )
