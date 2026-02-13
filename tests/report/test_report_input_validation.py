import pandas as pd
import pytest

from evidently import Report
from evidently.metrics import ColumnSummaryMetric


def test_report_run_fails_on_empty_current_data():
    report = Report(metrics=[ColumnSummaryMetric(column_name="x")])

    empty_df = pd.DataFrame()

    with pytest.raises(ValueError):
        report.run(current_data=empty_df)
