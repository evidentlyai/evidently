from evidently.metrics.data_integrity.column_missing_values_metric import ColumnMissingValuesMetric
from evidently.metrics.data_integrity.column_regexp_metric import ColumnRegExpMetric
from evidently.metrics.data_integrity.column_summary_metric import ColumnSummaryMetric
from evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetric
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def column_missing_values_metric():
    return TestMetric(
        "column_missing_values_metric", ColumnMissingValuesMetric(column_name="education"), dataset_names=["adult"]
    )


@metric
def column_summary_metric():
    return TestMetric("column_summary_metric", ColumnSummaryMetric(column_name="age"), dataset_names=["adult"])


@metric
def dataset_summary_metric():
    return TestMetric("dataset_summary_metric", DatasetSummaryMetric())


@metric
def column_reg_exp_metric():
    return TestMetric(
        "column_reg_exp_metric",
        ColumnRegExpMetric(column_name="relationship", reg_exp=r".*child.*"),
        dataset_names=["adult"],
    )


@metric
def dataset_missing_values_metric():
    return TestMetric("dataset_missing_values_metric", DatasetMissingValuesMetric())
