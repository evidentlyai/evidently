import json
from typing import Optional

import pandas as pd
import pytest

from evidently.legacy.metrics import ColumnValuePlot
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, data_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValuePlot(column_name="col"),
            {},
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValuePlot(column_name="col"),
            {},
        ),
    ),
)
def test_column_value_plot_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: ColumnValuePlot,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    assert report.show()
    result_json = report.json()
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "ColumnValuePlot"
    assert result["metrics"][0]["result"] == expected_json


@pytest.mark.parametrize(
    "current_data, reference_data, data_mapping, metric, expected_error",
    (
        # no reference dataset
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            None,
            ColumnValuePlot(column_name="feature"),
            "Reference data should be present",
        ),
        # no column in current dataset
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValuePlot(column_name="col"),
            "Column 'col' should present in the current dataset",
        ),
        # no column in reference dataset
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            ColumnValuePlot(column_name="col"),
            "Column 'col' should present in the reference dataset",
        ),
    ),
)
def test_column_value_plot_errors(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    data_mapping: Optional[ColumnMapping],
    metric: ColumnValuePlot,
    expected_error: str,
) -> None:
    report = Report(metrics=[metric])

    with pytest.raises(ValueError, match=expected_error):
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
        report.json()
