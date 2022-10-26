import json

import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_integrity.column_summary_metric import CategoricalCharacteristics
from evidently.metrics.data_integrity.column_summary_metric import ColumnSummary
from evidently.metrics.data_integrity.column_summary_metric import DataQualityPlot
from evidently.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, metric, expected_result",
    (
        (
            pd.DataFrame({"target": [1, "ff", 3], "prediction": ["a", "b", "c"]}),
            None,
            ColumnMapping(),
            ColumnSummaryMetric(column_name="target"),
            ColumnSummary(
                column_name="target",
                column_type="cat",
                reference_characteristics=None,
                current_characteristics=CategoricalCharacteristics(
                    number_of_rows=3,
                    count=3,
                    unique=3,
                    unique_percentage=3,
                    most_common=3,
                    most_common_percentage=3,
                    missing=3,
                    missing_percentage=3,
                    new_in_current_values_count=None,
                    unused_in_current_values_count=None,
                ),
                plot_data=DataQualityPlot(
                    bins_for_hist={},
                    data_in_time=None,
                    data_by_target=None,
                    counts_of_values=None,
                ),
            ),
        ),
    ),
)
def test_column_summary_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    metric: ColumnSummaryMetric,
    expected_result: ColumnSummary,
) -> None:
    result = metric.calculate(
        data=InputData(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    )
    assert result is not None
    # assert result == expected_result


@pytest.mark.parametrize(
    "current_data, reference_data, metric, error_message",
    (
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnSummaryMetric(column_name="col2"),
            "Column 'col2' not found in current dataset.",
        ),
        (
            pd.DataFrame(
                {
                    "col2": [1, 2, 1, 2, 1],
                }
            ),
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            ColumnSummaryMetric(column_name="col2"),
            "Column 'col2' not found in reference dataset.",
        ),
    ),
)
def test_column_summary_metric_value_error(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnSummaryMetric, error_message: str
) -> None:
    with pytest.raises(ValueError) as error:
        metric.calculate(
            data=InputData(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
        )

    assert error.value.args[0] == error_message


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"test1": ["a", "a", "c", "d", "e", "f", "g", "h", "i", "j"]}),
            None,
            ColumnMapping(),
            ColumnSummaryMetric(column_name="test1"),
            {
                "column_name": "test1",
                "column_type": "cat",
                "current_characteristics": {
                    "count": 10,
                    "missing": 0,
                    "missing_percentage": 0.0,
                    "most_common": "a",
                    "most_common_percentage": 20.0,
                    "new_in_current_values_count": None,
                    "number_of_rows": 10,
                    "unique": 9,
                    "unique_percentage": 90.0,
                    "unused_in_current_values_count": None,
                },
                "reference_characteristics": None,
            },
        ),
        (
            pd.DataFrame({"test1": ["a", "a", "a"]}),
            pd.DataFrame({"test1": ["c", "c", "e", "f", "g", "h", "i", "j"]}),
            ColumnMapping(),
            ColumnSummaryMetric(column_name="test1"),
            {
                "column_name": "test1",
                "column_type": "cat",
                "current_characteristics": {
                    "count": 3,
                    "missing": 0,
                    "missing_percentage": 0.0,
                    "most_common": "a",
                    "most_common_percentage": 100.0,
                    "new_in_current_values_count": 1,
                    "number_of_rows": 3,
                    "unique": 1,
                    "unique_percentage": 33.33,
                    "unused_in_current_values_count": 7,
                },
                "reference_characteristics": {
                    "count": 8,
                    "missing": 0,
                    "missing_percentage": 0.0,
                    "most_common": "c",
                    "most_common_percentage": 25.0,
                    "new_in_current_values_count": None,
                    "number_of_rows": 8,
                    "unique": 7,
                    "unique_percentage": 87.5,
                    "unused_in_current_values_count": None,
                },
            },
        ),
        (
            pd.DataFrame({"test1": [1, 2, 3], "test2": [1, 2, 3], "test3": [1, 1, 1]}),
            pd.DataFrame({"test1": [1, 2, 3], "test2": ["a", "a", "a"], "test3": [1, 1, 1]}),
            ColumnMapping(),
            ColumnSummaryMetric(column_name="test1"),
            {
                "column_name": "test1",
                "column_type": "num",
                "current_characteristics": {
                    "count": 3,
                    "infinite_count": 0,
                    "infinite_percentage": 0.0,
                    "max": 3,
                    "mean": 2.0,
                    "min": 1,
                    "missing": 0,
                    "missing_percentage": 0.0,
                    "most_common": 3,
                    "most_common_percentage": 33.33,
                    "number_of_rows": 3,
                    "p25": 1.5,
                    "p50": 2.0,
                    "p75": 2.5,
                    "std": 1.0,
                    "unique": 3,
                    "unique_percentage": 100.0,
                },
                "reference_characteristics": {
                    "count": 3,
                    "infinite_count": 0,
                    "infinite_percentage": 0.0,
                    "max": 3,
                    "mean": 2.0,
                    "min": 1,
                    "missing": 0,
                    "missing_percentage": 0.0,
                    "most_common": 3,
                    "most_common_percentage": 33.33,
                    "number_of_rows": 3,
                    "p25": 1.5,
                    "p50": 2.0,
                    "p75": 2.5,
                    "std": 1.0,
                    "unique": 3,
                    "unique_percentage": 100.0,
                },
            },
        ),
    ),
)
def test_column_summary_metric_with_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    metric: ColumnSummaryMetric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnSummaryMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnSummaryMetric"] == expected_json
