from typing import ClassVar
from typing import Dict
from typing import Optional

import pandas as pd
import pytest

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.base_metric import DatasetType
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.metrics import ColumnValueRangeMetric
from evidently.legacy.metrics.base_metric import generate_column_metrics
from evidently.legacy.options.base import Options
from evidently.legacy.options.option import Option
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.pydantic_utils import FingerprintPart
from evidently.pydantic_utils import get_value_fingerprint


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
    class Config:
        alias_required = False

    column_name: ColumnName

    def __init__(self, column_name: ColumnName):
        self.column_name = column_name
        super().__init__()

    def calculate(self, data: InputData) -> int:
        return data.get_current_column(self.column_name).sum()


class SimpleMetric2(Metric[int]):
    class Config:
        alias_required = False

    column_name: ColumnName

    def __init__(self, column_name: ColumnName):
        self.column_name = column_name
        super().__init__()

    def calculate(self, data: InputData) -> int:
        return data.get_current_column(self.column_name).sum() + 1


class SimpleMetricWithFeatures(Metric[int]):
    class Config:
        alias_required = False

    column_name: str
    _feature: Optional[GeneratedFeature]

    def __init__(self, column_name: str):
        self.column_name = column_name
        self._feature = None
        super().__init__()

    def calculate(self, data: InputData) -> int:
        if data.data_definition.get_column(self.column_name).column_type == ColumnType.Categorical:
            return data.get_current_column(self._feature.as_column()).sum()
        return data.get_current_column(self.column_name).sum()

    def required_features(self, data_definition: DataDefinition):
        column_type = data_definition.get_column(self.column_name).column_type
        self._feature = LengthFeature(self.column_name)
        if column_type == ColumnType.Categorical:
            return [self._feature]
        return []


class MetricWithAllTextFeatures(Metric[Dict[str, int]]):
    class Config:
        alias_required = False

    _features: Dict[str, "LengthFeature"]

    def calculate(self, data: InputData):
        return {k: data.get_current_column(v.as_column()).sum() for k, v in self._features.items()}

    def required_features(self, data_definition: DataDefinition):
        self._features = {
            column.column_name: LengthFeature(column.column_name)
            for column in data_definition.get_columns(ColumnType.Text, features_only=True)
        }
        return list(self._features.values())


class SimpleGeneratedFeature(GeneratedFeature):
    class Config:
        alias_required = False

    __feature_type__: ClassVar = ColumnType.Numerical
    column_name: str

    def __init__(self, column_name: str, display_name: str = ""):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name] * 2)]))

    def _as_column(self) -> ColumnName:
        return self._create_column(subcolumn=self.column_name, default_display_name="SGF: {self.column_name}")


class LengthFeature(GeneratedFeature):
    class Config:
        alias_required = False

    __feature_type__: ClassVar = ColumnType.Numerical
    column_name: str
    max_length: Optional[int] = None

    def __init__(self, column_name: str, max_length: Optional[int] = None):
        self.column_name = column_name
        self.max_length = max_length
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(len))]))

    def _as_column(self) -> ColumnName:
        return self._create_column(self.column_name, default_display_name=f"Length of {self.column_name}")


@pytest.mark.parametrize(
    "metric,result",
    [
        (SimpleMetric(ColumnName("col1", "col1", DatasetType.MAIN, None)), 6),
        (SimpleMetric(SimpleGeneratedFeature("col1").as_column()), 12),
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
                SimpleMetric(SimpleGeneratedFeature("col1", "d1").as_column()),
                SimpleMetric2(SimpleGeneratedFeature("col1", "d2").as_column()),
            ],
            (12, 13),
        ),
    ],
)
def test_additional_features_multi_metrics(metrics, result):
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


def test_options_fingerprint_not_specified():
    class MyOption(Option):
        field: str

    class MockMetric(Metric[MetricResult]):
        class Config:
            alias_required = False

        def calculate(self, data: InputData):
            return MetricResult()

    m1 = MockMetric(options=[MyOption(field="a")])
    m2 = MockMetric(options=[MyOption(field="b")])

    assert m1.get_fingerprint() == m2.get_fingerprint()


def test_options_fingerprint_specified_type():
    class MyOption(Option):
        field: str

    class UsesMyOptionMixin:
        options: Options

        def get_options_fingerprint(self) -> FingerprintPart:
            return get_value_fingerprint(self.options.get(MyOption).field)

    class MockMetricWithOption(UsesMyOptionMixin, Metric[MetricResult]):
        class Config:
            alias_required = False

        def calculate(self, data: InputData):
            return MetricResult()

    m3 = MockMetricWithOption(options=[MyOption(field="a")])
    m4 = MockMetricWithOption(options=[MyOption(field="b")])

    assert m3.get_fingerprint() != m4.get_fingerprint()
