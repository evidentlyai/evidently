from typing import Dict
from typing import Union

import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import IncludeTags
from evidently.pydantic_utils import FieldPath
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


def test_include_exclude():
    class SomeModel(MetricResult):
        class Config:
            field_tags = {"f1": {IncludeTags.Render}}

        f1: str
        f2: str

    assert SomeModel.fields.list_nested_fields(exclude={IncludeTags.Render, IncludeTags.TypeField}) == ["f2"]

    # assert SomeModel.fields.list_nested_fields(include={IncludeTags.Render}) == ["f1"]

    class SomeNestedModel(MetricResult):
        class Config:
            tags = {IncludeTags.Render}

        f1: str

    class SomeOtherModel(MetricResult):
        f1: str
        f2: SomeNestedModel
        f3: SomeModel

    assert SomeOtherModel.fields.list_nested_fields(exclude={IncludeTags.Render, IncludeTags.TypeField}) == [
        "f1",
        "f3.f2",
    ]
    # assert SomeOtherModel.fields.list_nested_fields(include={IncludeTags.Render}) == ["f2.f1", "f3.f1"]


def test_get_field_tags():
    class SomeModel(MetricResult):
        class Config:
            field_tags = {"f1": {IncludeTags.Render}}

        f1: str
        f2: str

    assert SomeModel.fields.get_field_tags(["type"]) == {IncludeTags.TypeField}
    assert SomeModel.fields.get_field_tags(["f1"]) == {IncludeTags.Render}
    assert SomeModel.fields.get_field_tags(["f2"]) == set()

    class SomeNestedModel(MetricResult):
        class Config:
            tags = {IncludeTags.Render}

        f1: str

    class SomeOtherModel(MetricResult):
        f1: str
        f2: SomeNestedModel
        f3: SomeModel

    assert SomeOtherModel.fields.get_field_tags(["type"]) == {IncludeTags.TypeField}
    assert SomeOtherModel.fields.get_field_tags(["f1"]) == set()
    assert SomeOtherModel.fields.get_field_tags(["f2"]) == {IncludeTags.Render}
    assert SomeOtherModel.fields.get_field_tags(["f2", "f1"]) == {IncludeTags.Render}
    assert SomeOtherModel.fields.get_field_tags(["f3"]) == set()
    assert SomeOtherModel.fields.get_field_tags(["f3", "f1"]) == {IncludeTags.Render}
    assert SomeOtherModel.fields.get_field_tags(["f3", "f2"]) == set()


def test_list_with_tags():
    class SomeModel(MetricResult):
        class Config:
            field_tags = {"f1": {IncludeTags.Render}}

        f1: str
        f2: str

    assert SomeModel.fields.list_nested_fields_with_tags() == [
        ("type", {IncludeTags.TypeField}),
        ("f1", {IncludeTags.Render}),
        ("f2", set()),
    ]

    class SomeNestedModel(MetricResult):
        class Config:
            tags = {IncludeTags.Render}

        f1: str

    class SomeOtherModel(MetricResult):
        f1: str
        f2: SomeNestedModel
        f3: SomeModel

    assert SomeOtherModel.fields.list_nested_fields_with_tags() == [
        ("type", {IncludeTags.TypeField}),
        ("f1", set()),
        ("f2.type", {IncludeTags.Render, IncludeTags.TypeField}),
        ("f2.f1", {IncludeTags.Render}),
        ("f3.type", {IncludeTags.TypeField}),
        ("f3.f1", {IncludeTags.Render}),
        ("f3.f2", set()),
    ]


def test_list_with_tags_with_union():
    class A(MetricResult):
        class Config:
            tags = {IncludeTags.Render}

        f1: str

    class B(MetricResult):
        class Config:
            tags = {IncludeTags.Render}

        f1: str

    fp = FieldPath([], Union[A, B])
    assert not fp.has_instance
    assert fp._cls == A

    class SomeModel(MetricResult):
        f2: Union[A, B]
        f1: str

    assert SomeModel.fields.list_nested_fields_with_tags() == [
        ("type", {IncludeTags.TypeField}),
        ("f2.type", {IncludeTags.Render, IncludeTags.TypeField}),
        ("f2.f1", {IncludeTags.Render}),
        ("f1", set()),
    ]
