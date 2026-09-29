import pandas as pd
from evidently.metrics.average_precision_metric import ClassificationAveragePrecision
from evidently.legacy.report import Report


def test_average_precision_metric_success():
    current = pd.DataFrame({
        "target": [1, 0, 1, 1, 0, 1],
        "prediction": [0.9, 0.2, 0.8, 0.4, 0.1, 0.7]
    })

    report = Report(metrics=[ClassificationAveragePrecision()])
    report.run(current_data=current, reference_data=None)
    result = report.as_dict()

    metric_res = result["metrics"][0]["result"]
    assert metric_res["current_value"] is not None
    assert 0.0 <= metric_res["current_value"] <= 1.0