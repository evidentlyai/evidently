import json

import pandas as pd
import pytest

from evidently.metrics.data_integrity.rouge_summary_metric import ROUGESummaryMetric
from evidently.metrics.data_integrity.rouge_summary_metric import ROUGESummaryMetricResult
from evidently.report.report import Report
from tests.conftest import smart_assert_equal


@pytest.mark.parametrize(
    "current_df, reference_df, metric, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "summary": ["hello there", "general kenobi"],
                }
            ),
            pd.DataFrame({"summary": ["hello there", "no de"]}),
            ROUGESummaryMetric(column_name="summary", rouge_n=1),
            ROUGESummaryMetricResult(rouge_type="ROUGE-1", score={"per_row_scores": [1.0, 0.0], "summary_score": 0.5}),
        ),
    ),
)
def test_rouge_summary_metric_success(
    current_df: pd.DataFrame,
    reference_df: pd.DataFrame,
    metric,
    expected_result: ROUGESummaryMetricResult,
) -> None:
    report = Report(metrics=[metric])

    report.run(current_data=current_df, reference_data=reference_df)

    smart_assert_equal(metric.get_result(), expected_result)


@pytest.mark.parametrize(
    "current_df, reference_df, metric, expected_json",
    (
        (
            pd.DataFrame(
                {
                    "summary": ["hello there", "general kenobi"],
                }
            ),
            pd.DataFrame({"summary": ["hello there", "no de"]}),
            ROUGESummaryMetric(column_name="summary", rouge_n=1),
            {"rouge_type": "ROUGE-1", "score": {"per_row_scores": [1.0, 0.0], "summary_score": 0.5}},
        ),
    ),
)
def test_rouge_summary_metric_with_report(
    current_df: pd.DataFrame,
    reference_df: pd.DataFrame,
    metric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])

    report.run(current_data=current_df, reference_data=reference_df)

    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    result = json.loads(json_result)
    assert result["metrics"][0]["result"] == expected_json
