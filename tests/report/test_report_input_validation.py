import pytest

from evidently.report import Report


def test_report_invalid_metrics_type():
    """
    Report should raise an error when metrics is not a list.
    """
    with pytest.raises(Exception):
        Report(metrics="not_a_list")
