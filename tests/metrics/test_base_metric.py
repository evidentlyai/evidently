import pandas as pd

from evidently.features.generated_features import GeneratedFeature
from evidently.metrics import ColumnValueRangeMetric
from evidently.metrics.base_metric import generate_column_metrics, Metric, InputData, TResult, ColumnName, DatasetType, \
    additional_feature
from evidently.report import Report
from evidently.utils.data_preprocessing import DataDefinition


def test_metric_generator():
    test_data = pd.DataFrame({"col1": [3, 2, 3], "col2": [4, 5, 6], "col3": [4, 5, 6]})
    report = Report(metrics=[generate_column_metrics(ColumnValueRangeMetric, parameters={"left": 0, "right": 10})])
    report.run(current_data=test_data, reference_data=None)
    assert report.show()

    report = Report(
        metrics=[
            generate_column_metrics(
                metric_class=ColumnValueRangeMetric, columns=["col2", "col3"], parameters={"left": 0, "right": 10}
            )
        ]
    )
    report.run(current_data=test_data, reference_data=None)
    assert report.show()


class SimpleMetric(Metric[int]):
    column_name: ColumnName

    def __init__(self, column_name: ColumnName):
        self.column_name = column_name

    def calculate(self, data: InputData) -> int:
        return data.get_current_column(self.column_name).sum()


class SimpleGeneratedFeature(GeneratedFeature):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name] * 2)]))


def test_additional_features():
    test_data = pd.DataFrame(dict(col1=[1, 2, 3], col2=[1, 2, 3]))
    metric = SimpleMetric(ColumnName("col1", DatasetType.MAIN, None))
    metric2 = SimpleMetric(additional_feature(SimpleGeneratedFeature("col1"), "col1"))
    report = Report(metrics=[metric, metric2])

    report.run(current_data=test_data, reference_data=None)
    results = metric.get_result()
    assert results == 6
    assert metric2.get_result() == 12

