import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.features.generated_features import GeneratedFeature
from evidently.metrics import ColumnValueRangeMetric
from evidently.metrics.base_metric import ColumnName
from evidently.metrics.base_metric import DatasetType
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.base_metric import additional_feature
from evidently.metrics.base_metric import generate_column_metrics
from evidently.report import Report
from evidently.utils.data_preprocessing import ColumnType
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


class SimpleMetricWithFeatures(Metric[int]):
    column_name: str

    def __init__(self, column_name: str):
        self.column_name = column_name
        self.feature = LengthFeature(self.column_name)

    def calculate(self, data: InputData) -> int:
        if data.data_definition.get_column(self.column_name).column_type == ColumnType.Categorical:
            return data.get_current_column(self.feature.feature_name()).sum()
        return data.get_current_column(self.column_name).sum()

    def required_features(self, data_definition: DataDefinition):
        column_type = data_definition.get_column(self.column_name).column_type
        if column_type == ColumnType.Categorical:
            return [self.feature]
        return []


class SimpleGeneratedFeature(GeneratedFeature):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name] * 2)]))

    def feature_name(self) -> ColumnName:
        return ColumnName(self.column_name, DatasetType.ADDITIONAL, self)


class LengthFeature(GeneratedFeature):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(len))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name)


@pytest.mark.parametrize(
    "metric,result",
    [
        (SimpleMetric(ColumnName("col1", DatasetType.MAIN, None)), 6),
        (SimpleMetric(additional_feature(SimpleGeneratedFeature("col1"), "col1")), 12),
        (SimpleMetricWithFeatures("col1"), 6),
        (SimpleMetricWithFeatures("col2"), 9),
    ],
)
def test_additional_features(metric, result):
    test_data = pd.DataFrame(dict(col1=[1.0, 2.0, 3.0], col2=["11", "111", "1111"]))
    report = Report(metrics=[metric])

    report.run(
        current_data=test_data,
        reference_data=None,
        column_mapping=ColumnMapping(
            numerical_features=["col1"],
            categorical_features=["col2"],
        ),
    )
    assert metric.get_result() == result
