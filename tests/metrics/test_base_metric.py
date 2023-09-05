from typing import Dict
from typing import Optional

import pandas as pd
import pytest

from evidently.base_metric import ColumnName
from evidently.base_metric import DatasetType
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import additional_feature
from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.metrics import ColumnValueRangeMetric
from evidently.metrics.base_metric import generate_column_metrics
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.utils.data_preprocessing import DataDefinition


def test_metric_generator():
    test_data = pd.DataFrame({"col1": [3, 2, 3], "col2": [4, 5, 6], "col3": [4, 5, 6]})
    report = Report(metrics=[generate_column_metrics(ColumnValueRangeMetric, parameters={"left": 0, "right": 10})])
    report.run(
        current_data=test_data,
        reference_data=None,
        column_mapping=ColumnMapping(numerical_features=["col1", "col2", "col3"]),
    )
    assert report.show()

    report = Report(
        metrics=[
            generate_column_metrics(
                metric_class=ColumnValueRangeMetric, columns=["col2", "col3"], parameters={"left": 0, "right": 10}
            )
        ]
    )
    report.run(
        current_data=test_data,
        reference_data=None,
        column_mapping=ColumnMapping(numerical_features=["col1", "col2", "col3"]),
    )
    assert report.show()


class SimpleMetric(Metric[int]):
    column_name: ColumnName

    def __init__(self, column_name: ColumnName):
        self.column_name = column_name
        super().__init__()

    def calculate(self, data: InputData) -> int:
        return data.get_current_column(self.column_name).sum()


class SimpleMetric2(Metric[int]):
    column_name: ColumnName

    def __init__(self, column_name: ColumnName):
        self.column_name = column_name
        super().__init__()

    def calculate(self, data: InputData) -> int:
        return data.get_current_column(self.column_name).sum() + 1


class SimpleMetricWithFeatures(Metric[int]):
    column_name: str
    _feature: Optional[GeneratedFeature]

    def __init__(self, column_name: str):
        self.column_name = column_name
        self._feature = None
        super().__init__()

    def calculate(self, data: InputData) -> int:
        if data.data_definition.get_column(self.column_name).column_type == ColumnType.Categorical:
            return data.get_current_column(self._feature.feature_name()).sum()
        return data.get_current_column(self.column_name).sum()

    def required_features(self, data_definition: DataDefinition):
        column_type = data_definition.get_column(self.column_name).column_type
        self._feature = LengthFeature(self.column_name)
        if column_type == ColumnType.Categorical:
            return [self._feature]
        return []


class MetricWithAllTextFeatures(Metric[Dict[str, int]]):
    _features: Dict[str, "LengthFeature"]

    def calculate(self, data: InputData):
        return {k: data.get_current_column(v.feature_name()).sum() for k, v in self._features.items()}

    def required_features(self, data_definition: DataDefinition):
        self._features = {
            column.column_name: LengthFeature(column.column_name)
            for column in data_definition.get_columns("text_features")
        }
        return list(self._features.values())


class SimpleGeneratedFeature(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str, display_name: str = ""):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name] * 2)]))

    def feature_name(self) -> ColumnName:
        return additional_feature(
            self,
            self.column_name,
            self.display_name if self.display_name else "SGF: {self.column_name}",
        )


class LengthFeature(GeneratedFeature):
    column_name: str
    max_length: Optional[int] = None

    def __init__(self, column_name: str, max_length: Optional[int] = None):
        self.column_name = column_name
        self.max_length = max_length
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(len))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name, f"Length of {self.column_name}")


@pytest.mark.parametrize(
    "metric,result",
    [
        (SimpleMetric(ColumnName("col1", "col1", DatasetType.MAIN, None)), 6),
        (SimpleMetric(SimpleGeneratedFeature("col1").feature_name()), 12),
        (SimpleMetricWithFeatures("col1"), 6),
        (SimpleMetricWithFeatures("col2"), 9),
        (MetricWithAllTextFeatures(), {"col3": 9, "col4": 12}),
    ],
)
def test_additional_features(metric, result):
    test_data = pd.DataFrame(
        dict(
            col1=[1.0, 2.0, 3.0],
            col2=["11", "111", "1111"],
            col3=["11", "111", "1111"],
            col4=["111", "1111", "11111"],
        )
    )
    report = Report(metrics=[metric])

    report.run(
        current_data=test_data,
        reference_data=None,
        column_mapping=ColumnMapping(
            numerical_features=["col1"],
            categorical_features=["col2"],
            text_features=["col3", "col4"],
        ),
    )
    report._inner_suite.raise_for_error()
    assert metric.get_result() == result


@pytest.mark.parametrize(
    "metrics,result",
    [
        (
            [
                SimpleMetric(SimpleGeneratedFeature("col1", "d1").feature_name()),
                SimpleMetric2(SimpleGeneratedFeature("col1", "d2").feature_name()),
            ],
            (12, 13),
        ),
    ],
)
def test_additional_features(metrics, result):
    test_data = pd.DataFrame(
        dict(
            col1=[1.0, 2.0, 3.0],
            col2=["11", "111", "1111"],
            col3=["11", "111", "1111"],
            col4=["111", "1111", "11111"],
        )
    )
    report = Report(metrics=metrics)

    report.run(
        current_data=test_data,
        reference_data=None,
        column_mapping=ColumnMapping(
            numerical_features=["col1"],
            categorical_features=["col2"],
            text_features=["col3", "col4"],
        ),
    )
    report._inner_suite.raise_for_error()
    assert metrics[0].get_result() == result[0]
    assert metrics[1].get_result() == result[1]
