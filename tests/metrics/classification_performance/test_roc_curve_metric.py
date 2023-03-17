import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import ClassificationRocCurve
from evidently.report import Report


def test_roc_curve_no_exceptions():
    current = pd.DataFrame(
        data=dict(
            target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            a=[0.8, 0.7, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.7],
            b=[0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.4, 0.8],
            c=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.8, 0.9],
        ),
    )
    metric = ClassificationRocCurve()
    report = Report(metrics=[metric])
    report.run(current_data=current, reference_data=None, column_mapping=ColumnMapping(prediction=["a", "b", "c"]))
    metric.get_result()
    report.json()
