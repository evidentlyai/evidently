import pandas as pd

from evidently.metrics import ColumnValueRangeMetric
from evidently.metrics.base_metric import generate_column_metrics
from evidently.report import Report


def test_metric_generator():
    test_data = pd.DataFrame({"col1": [3, 2, 3], "col2": [4, 5, 6], "col3": [4, 5, 6]})
    report = Report(
        metrics=[
            generate_column_metrics(
                ColumnValueRangeMetric, parameters={"left": 0, "right": 10}
            )
        ]
    )
    report.run(current_data=test_data, reference_data=None)
    assert report.show()

    report = Report(
        metrics=[
            generate_column_metrics(
                metric_class=ColumnValueRangeMetric,
                columns=["col2", "col3"],
                parameters={"left": 0, "right": 10},
            )
        ]
    )
    report.run(current_data=test_data, reference_data=None)
    assert report.show()
