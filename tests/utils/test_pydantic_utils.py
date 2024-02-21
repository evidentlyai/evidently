from typing import Dict

import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.pydantic_utils import PolymorphicModel


class MockMetricResultField(MetricResult):
    nested_field: str


class ExtendedMockMetricResultField(MockMetricResultField):
    additional_field: str


class MockMetricResult(MetricResult):
    field1: MockMetricResultField
    field2: int


def _metric_with_result(result: MetricResult):
    class MockMetric(Metric):
        def get_result(self):
            return result

        def calculate(self, data):
            pass

    return MockMetric()


def test_field_path():
    assert MockMetricResult.fields.list_fields() == ["type", "field1", "field2"]
    assert MockMetricResult.fields.field1.list_fields() == ["type", "nested_field"]
    assert MockMetricResult.fields.list_nested_fields() == ["type", "field1.type", "field1.nested_field", "field2"]

    with pytest.raises(AttributeError):
        _ = MockMetricResult.fields.field3

    metric_result = MockMetricResult(field1=MockMetricResultField(nested_field="1"), field2=1)
    metric = _metric_with_result(metric_result)

    assert metric.fields.list_fields() == ["type", "field1", "field2"]
    assert metric.fields.field1.list_fields() == ["type", "nested_field"]
    assert metric.fields.list_nested_fields() == ["type", "field1.type", "field1.nested_field", "field2"]

    metric_result = MockMetricResult(
        field1=ExtendedMockMetricResultField(nested_field="1", additional_field="2"), field2=1
    )
    metric = _metric_with_result(metric_result)

    assert metric.fields.list_fields() == ["type", "field1", "field2"]
    assert metric.fields.field1.list_fields() == ["type", "nested_field", "additional_field"]
    assert metric.fields.list_nested_fields() == [
        "type",
        "field1.type",
        "field1.nested_field",
        "field1.additional_field",
        "field2",
    ]


class MockMetricResultWithDict(MetricResult):
    d: Dict[str, MockMetricResultField]


def test_field_path_with_dict():
    assert MockMetricResultWithDict.fields.list_fields() == ["type", "d"]
    assert MockMetricResultWithDict.fields.list_nested_fields() == ["type", "d.*.type", "d.*.nested_field"]
    assert MockMetricResultWithDict.fields.d.lol.list_fields() == ["type", "nested_field"]
    assert str(MockMetricResultWithDict.fields.d.lol.nested_field) == "d.lol.nested_field"

    metric_result = MockMetricResultWithDict(d={"a": MockMetricResultField(nested_field="1")})
    metric = _metric_with_result(metric_result)

    assert metric.fields.list_fields() == ["type", "d"]
    assert metric.fields.list_nested_fields() == ["type", "d.a.type", "d.a.nested_field"]
    assert metric.fields.d.a.list_fields() == ["type", "nested_field"]
    assert metric.fields.d.list_fields() == ["a"]

    metric_result = MockMetricResultWithDict(
        d={
            "a": MockMetricResultField(nested_field="1"),
            "b": ExtendedMockMetricResultField(nested_field="1", additional_field="2"),
        }
    )
    metric = _metric_with_result(metric_result)

    assert metric.fields.list_fields() == ["type", "d"]
    assert metric.fields.list_nested_fields() == [
        "type",
        "d.a.type",
        "d.a.nested_field",
        "d.b.type",
        "d.b.nested_field",
        "d.b.additional_field",
    ]
    assert metric.fields.d.a.list_fields() == ["type", "nested_field"]
    assert metric.fields.d.list_fields() == ["a", "b"]


def test_not_allowed_prefix():
    class SomeModel(PolymorphicModel):
        pass

    with pytest.raises(ValueError):
        parse_obj_as(SomeModel, {"type": "external.Class"})


def test_type_alias():
    class SomeModel(PolymorphicModel):
        class Config:
            type_alias = "somemodel"

    class SomeModelSubclass(SomeModel):
        pass

    class SomeOtherSubclass(SomeModel):
        class Config:
            type_alias = "othersubclass"

    obj = parse_obj_as(SomeModel, {"type": "somemodel"})
    assert obj.__class__ == SomeModel

    obj = parse_obj_as(SomeModel, {"type": SomeModelSubclass.__get_type__()})
    assert obj.__class__ == SomeModelSubclass

    obj = parse_obj_as(SomeModel, {"type": "othersubclass"})
    assert obj.__class__ == SomeOtherSubclass
