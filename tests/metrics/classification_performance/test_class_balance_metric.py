import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import ClassificationClassBalance
from evidently.report import Report


@pytest.mark.parametrize(
    "reference, current, expected_plot_data",
    [
        (
            None,
            pd.DataFrame(
                {
                    "target": ["a", "a", "a", "a", "a", "b", "c", "c", "c"],
                    "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                }
            ),
            {"current": pd.DataFrame({"x": ["a", "c", "b"], "count": [5, 3, 1]})},
        ),
        (
            pd.DataFrame(
                {
                    "target": ["a", "a", "b", "b", "b", "c", "c", "c", "c"],
                    "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                }
            ),
            pd.DataFrame(
                {
                    "target": ["a", "a", "a", "a", "a", "b", "c", "c", "c"],
                    "prediction": ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                }
            ),
            {
                "current": pd.DataFrame({"x": ["a", "c", "b"], "count": [5, 3, 1]}),
                "reference": pd.DataFrame({"x": ["c", "b", "a"], "count": [4, 3, 2]}),
            },
        ),
    ],
)
def test_class_balance_metric(reference, current, expected_plot_data):
    metric = ClassificationClassBalance()
    report = Report(metrics=[metric])
    report.run(current_data=current, reference_data=reference, column_mapping=ColumnMapping())
    results = metric.get_result()

    pd.testing.assert_frame_equal(results.plot_data["current"], expected_plot_data["current"])
    if "reference" in expected_plot_data.keys():
        pd.testing.assert_frame_equal(results.plot_data["reference"], expected_plot_data["reference"])
