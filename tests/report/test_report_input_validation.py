import pandas as pd
import pytest

from evidently import Report


def test_report_run_fails_on_empty_current_data():
    report = Report(metrics=[])

    empty_df = pd.DataFrame()

    with pytest.raises(ValueError):
        report.run(current_data=empty_df)
