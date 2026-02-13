from abc import ABC
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Set
from typing import Union

import pytest
from pydantic import TypeAdapter
from pydantic import ValidationError

from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.core import IncludeTags
from evidently.legacy.core import get_all_fields_tags
from evidently.pydantic_utils import ALLOWED_TYPE_PREFIXES
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import FieldPath
from evidently.pydantic_utils import PolymorphicModel


class MockMetricResultField(MetricResult):
    __alias_required__: ClassVar[bool] = False

    nested_field: str


class ExtendedMockMetricResultField(MockMetricResultField):
    __alias_required__: ClassVar[bool] = False

    additional_field: str


class MockMetricResult(MetricResult):
    __alias_required__: ClassVar[bool] = False

    field1: MockMetricResultField
    field2: int


def _metric_with_result(result: MetricResult):
    class MockMetric(Metric):
        __alias_required__: ClassVar[bool] = False

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
    __alias_required__: ClassVar[bool] = False

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
        __alias_required__: ClassVar[bool] = False

    with pytest.raises(ValueError):
        TypeAdapter(SomeModel).validate_python({"type": "external.Class"})


def test_type_alias():
    class SomeModel(PolymorphicModel):
        __type_alias__: ClassVar[Optional[str]] = "somemodel"
        __alias_required__: ClassVar[bool] = False

    class SomeModelSubclass(SomeModel):
        pass

    class SomeOtherSubclass(SomeModel):
        __type_alias__: ClassVar[Optional[str]] = "othersubclass"

    obj = TypeAdapter(SomeModel).validate_python({"type": "somemodel"})
    assert obj.__class__ == SomeModel

    obj = TypeAdapter(SomeModel).validate_python({"type": SomeModelSubclass.__get_type__()})
    assert obj.__class__ == SomeModelSubclass

    obj = TypeAdapter(SomeModel).validate_python({"type": "othersubclass"})
    assert obj.__class__ == SomeOtherSubclass


def test_include_exclude():
    class SomeModel(MetricResult):
        __field_tags__: ClassVar[Dict[str, Set[IncludeTags]]] = {"f1": {IncludeTags.Render}}
        __alias_required__: ClassVar[bool] = False

        f1: str
        f2: str

    assert SomeModel.fields.list_nested_fields(exclude={IncludeTags.Render, IncludeTags.TypeField}) == ["f2"]

    # assert SomeModel.fields.list_nested_fields(include={IncludeTags.Render}) == ["f1"]

    class SomeNestedModel(MetricResult):
        __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
        __alias_required__: ClassVar[bool] = False

        f1: str

    class SomeOtherModel(MetricResult):
        __alias_required__: ClassVar[bool] = False

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
        __field_tags__: ClassVar[Dict[str, Set[IncludeTags]]] = {"f1": {IncludeTags.Render}}
        __alias_required__: ClassVar[bool] = False

        f1: str
        f2: str

    assert SomeModel.fields.get_field_tags(["type"]) == {IncludeTags.TypeField}
    assert SomeModel.fields.get_field_tags(["f1"]) == {IncludeTags.Render}
    assert SomeModel.fields.get_field_tags(["f2"]) == set()

    class SomeNestedModel(MetricResult):
        __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
        __alias_required__: ClassVar[bool] = False

        f1: str

    class SomeOtherModel(MetricResult):
        __alias_required__: ClassVar[bool] = False

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
        __field_tags__: ClassVar[Dict[str, Set[IncludeTags]]] = {"f1": {IncludeTags.Render}}
        __alias_required__: ClassVar[bool] = False

        f1: str
        f2: str

    assert SomeModel.fields.list_nested_fields_with_tags() == [
        ("type", {IncludeTags.TypeField}),
        ("f1", {IncludeTags.Render}),
        ("f2", set()),
    ]

    class SomeNestedModel(MetricResult):
        __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
        __alias_required__: ClassVar[bool] = False

        f1: str

    class SomeOtherModel(MetricResult):
        __alias_required__: ClassVar[bool] = False

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
        __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
        __alias_required__: ClassVar[bool] = False

        f1: str

    class B(MetricResult):
        __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
        __alias_required__: ClassVar[bool] = False

        f1: str

    fp = FieldPath([], Union[A, B])
    assert not fp.has_instance
    assert fp._cls == A

    class SomeModel(MetricResult):
        __alias_required__: ClassVar[bool] = False

        f2: Union[A, B]
        f1: str

    assert list(sorted(SomeModel.fields.list_nested_fields_with_tags())) == [
        ("f1", set()),
        ("f2.f1", {IncludeTags.Render}),
        ("f2.type", {IncludeTags.Render, IncludeTags.TypeField}),
        ("type", {IncludeTags.TypeField}),
    ]


def test_get_field_tags_no_overwrite():
    class A(MetricResult):
        __field_tags__: ClassVar[Dict[str, Set[IncludeTags]]] = {"f": {IncludeTags.Current}}
        __alias_required__: ClassVar[bool] = False

        f: str

    class B(A):
        __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Reference}

    class C(MetricResult):
        __field_tags__: ClassVar[Dict[str, Set[IncludeTags]]] = {"f": {IncludeTags.Reference}}
        __alias_required__: ClassVar[bool] = False

        f: A

    assert A.fields.get_field_tags("f") == {IncludeTags.Current}
    assert B.fields.get_field_tags("f") == {IncludeTags.Current, IncludeTags.Reference}
    assert C.fields.get_field_tags(["f", "f"]) == {IncludeTags.Current, IncludeTags.Reference}
    B.fields.list_nested_fields_with_tags()
    C.fields.list_nested_fields_with_tags()
    get_all_fields_tags(B)
    get_all_fields_tags(C)
    assert A.fields.get_field_tags("f") == {IncludeTags.Current}


def test_fingerprint_add_new_default_field():
    class A(EvidentlyBaseModel):
        __alias_required__: ClassVar[bool] = False

        field1: str

    f1 = A(field1="123").get_fingerprint()

    class A(EvidentlyBaseModel):
        __alias_required__: ClassVar[bool] = False

        field1: str
        field2: str = "321"

    f2 = A(field1="123").get_fingerprint()

    assert f2 == f1
    assert A(field1="123", field2="123").get_fingerprint() != f1


def test_fingerprint_reorder_fields():
    class A(EvidentlyBaseModel):
        __alias_required__: ClassVar[bool] = False

        field1: str
        field2: str

    f1 = A(field1="123", field2="321").get_fingerprint()

    class A(EvidentlyBaseModel):
        __alias_required__: ClassVar[bool] = False

        field2: str
        field1: str

    f2 = A(field1="123", field2="321").get_fingerprint()

    assert f2 == f1
    assert A(field1="123", field2="123").get_fingerprint() != f1


def test_fingerprint_default_collision():
    class A(EvidentlyBaseModel):
        __alias_required__: ClassVar[bool] = False

        field1: Optional[str] = None
        field2: Optional[str] = None

    assert A(field1="a").get_fingerprint() != A(field2="a").get_fingerprint()


def test_wrong_classpath():
    class WrongClassPath(EvidentlyBaseModel):
        __alias_required__: ClassVar[bool] = False

        f: str

    ALLOWED_TYPE_PREFIXES.append("tests.")
    a = WrongClassPath(f="asd")
    assert TypeAdapter(WrongClassPath).validate_python(a.model_dump()) == a
    d = a.model_dump()
    d["type"] += "_"
    with pytest.raises(ValidationError):
        TypeAdapter(WrongClassPath).validate_python(d)


def test_alias_requied():
    class RequiredAlias(PolymorphicModel, ABC):
        __alias_required__: ClassVar[bool] = True

    with pytest.raises(ValueError):

        class NoAlias(RequiredAlias):
            pass

    class Alias(RequiredAlias):
        __type_alias__: ClassVar[Optional[str]] = "alias"
