import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics import ColumnRegExpMetric
from evidently.legacy.metrics.data_integrity.column_regexp_metric import DataIntegrityValueByRegexpMetricResult
from evidently.legacy.metrics.data_integrity.column_regexp_metric import DataIntegrityValueByRegexpStat
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, column_name, reg_exp, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "category_feature": ["3", "a", "b5", "a", np.nan],
                    "target": [1, 2, 1, 2, 1],
                    "prediction": [1, 1, 1, 2, 2],
                }
            ),
            None,
            "category_feature",
            r".*\d+.*",
            DataIntegrityValueByRegexpMetricResult(
                column_name="category_feature",
                reg_exp=r".*\d+.*",
                top=10,
                current=DataIntegrityValueByRegexpStat(
                    number_of_matched=2,
                    number_of_not_matched=2,
                    number_of_rows=5,
                    table_of_matched={"3": 1, "b5": 1},
                    table_of_not_matched={"a": 2},
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "feature": ["a", "a", "c"],
                }
            ),
            "feature",
            r"^\s+.*",
            DataIntegrityValueByRegexpMetricResult(
                column_name="feature",
                reg_exp=r"^\s+.*",
                top=10,
                current=DataIntegrityValueByRegexpStat(
                    number_of_matched=2,
                    number_of_not_matched=1,
                    number_of_rows=5,
                    table_of_matched={" a": 1, "\tb": 1},
                    table_of_not_matched={"a": 1},
                ),
                reference=DataIntegrityValueByRegexpStat(
                    number_of_matched=0,
                    number_of_not_matched=3,
                    number_of_rows=3,
                    table_of_matched={},
                    table_of_not_matched={"a": 2, "c": 1},
                ),
            ),
        ),
    ),
)
def test_column_regexp_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    reg_exp: str,
    expected_result: DataIntegrityValueByRegexpMetricResult,
) -> None:
    metric = ColumnRegExpMetric(column_name=column_name, reg_exp=reg_exp)
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    result = metric.get_result()
    assert result == expected_result


@pytest.mark.parametrize(
    "current_data, reference_data, metric",
    (
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnRegExpMetric(column_name="test", reg_exp=r".*\d+.*"),
        ),
        (
            pd.DataFrame(
                {
                    "feature": [" a", "a", "\tb", np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "test": ["a", "a", "c"],
                }
            ),
            ColumnRegExpMetric(column_name="feature", reg_exp=r".*\d+.*"),
        ),
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnRegExpMetric(column_name="col", reg_exp=""),
        ),
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnRegExpMetric(column_name="col", reg_exp=r"\d*", top=0),
        ),
    ),
)
def test_column_regexp_metric_value_error(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnRegExpMetric
) -> None:
    with pytest.raises(ValueError):
        report = Report(metrics=[metric])
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
        metric.get_result()


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_json",
    (
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 1, 2, 1],
                }
            ),
            None,
            ColumnRegExpMetric(column_name="col", reg_exp=r".*\d+.*"),
            {
                "column_name": "col",
                "current": {
                    "number_of_matched": 5,
                    "number_of_not_matched": 0,
                    "number_of_rows": 5,
                    "table_of_matched": {"1": 3, "2": 2},
                    "table_of_not_matched": {},
                },
                "reference": None,
                "reg_exp": ".*\\d+.*",
                "top": 10,
            },
        ),
        (
            pd.DataFrame(
                {
                    "feature": [np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "feature": ["a", "a", "c"],
                }
            ),
            ColumnRegExpMetric(column_name="feature", reg_exp=r".*a+.*"),
            {
                "column_name": "feature",
                "current": {
                    "number_of_matched": 0,
                    "number_of_not_matched": 0,
                    "number_of_rows": 2,
                    "table_of_matched": {},
                    "table_of_not_matched": {},
                },
                "reference": {
                    "number_of_matched": 2,
                    "number_of_not_matched": 1,
                    "number_of_rows": 3,
                    "table_of_matched": {"a": 2},
                    "table_of_not_matched": {"c": 1},
                },
                "reg_exp": ".*a+.*",
                "top": 10,
            },
        ),
        (
            pd.DataFrame(
                {
                    "col": [1, 2, 3, 4, 5, "a", "b", "c", 1, 1234567890, "a", "a", "d", "e", "f"],
                }
            ),
            None,
            ColumnRegExpMetric(column_name="col", reg_exp=r"\d", top=3),
            {
                "column_name": "col",
                "current": {
                    "number_of_matched": 7,
                    "number_of_not_matched": 8,
                    "number_of_rows": 15,
                    "table_of_matched": {"1": 2, "2": 1, "3": 1},
                    "table_of_not_matched": {"a": 3, "b": 1, "c": 1},
                },
                "reference": None,
                "reg_exp": "\\d",
                "top": 3,
            },
        ),
    ),
)
def test_column_regexp_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnRegExpMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    result = json.loads(json_result)
    assert result["metrics"][0]["metric"] == "ColumnRegExpMetric"
    assert result["metrics"][0]["result"] == expected_json
