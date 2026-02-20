import glob
import os
from enum import Enum
from importlib import import_module
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Set
from typing import Type

import pytest
from pydantic import BaseModel
from pydantic import Field
from pydantic import TypeAdapter

import evidently
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.tests.base_test import EnumValueMixin
from tests.conftest import pydantic_v2_not_supported


@pytest.fixture
def all_metric_results():
    path = os.path.dirname(evidently.__file__)

    metric_result_field_classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = "evidently." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not MetricResult and issubclass(value, MetricResult):
                metric_result_field_classes.add(value)
    return metric_result_field_classes


def test_metric_result_fields_config(all_metric_results: Set[Type[MetricResult]]):
    errors = []
    for cls in all_metric_results:
        field_names = set(cls.model_fields)
        for config_field in (
            "pd_name_mapping",
            "dict_include_fields",
            "dict_exclude_fields",
            "pd_include_fields",
            "pd_exclude_fields",
        ):
            field_value = getattr(cls, f"__{config_field}__", None)
            if field_value is None:
                continue
            for field_name in field_value:
                if field_name not in field_names:
                    errors.append((cls, config_field, field_name))

    assert len(errors) == 0, f"Wrong config for field classes: {errors}"


class SimpleField(MetricResult):
    __alias_required__: ClassVar[bool] = False

    f1: str


class ExcludeModel(MetricResult):
    __dict_exclude_fields__: ClassVar[set] = {"simple"}
    __alias_required__: ClassVar[bool] = False

    simple: SimpleField


@pytest.mark.parametrize("obj, expected", [(ExcludeModel(simple=SimpleField(f1="a")), {})])
def test_default_json(obj: MetricResult, expected):
    assert obj.get_dict() == expected


class FieldExclude(MetricResult):
    __dict_exclude_fields__: ClassVar[set] = {"f2"}
    __alias_required__: ClassVar[bool] = False

    f1: str
    f2: List[int]


class FieldInclude(MetricResult):
    __dict_include_fields__: ClassVar[set] = {"f1"}
    __alias_required__: ClassVar[bool] = False

    f1: str
    f2: List[int]


class DictExclude(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __alias_required__: ClassVar[bool] = False

    f1: List[int]
    f2: List[int]


class NestedExclude(MetricResult):
    __alias_required__: ClassVar[bool] = False

    f: str
    nested: DictExclude


class Model(MetricResult):
    __alias_required__: ClassVar[bool] = False

    no: NestedExclude = Field(..., include={"nested": {"f1"}})
    fe: FieldExclude
    feo: FieldExclude = Field(include={"f1", "f2"})
    fi: FieldInclude
    de: DictExclude
    deo: DictExclude = Field(..., include=True)
    n: NestedExclude


@pytest.fixture
def model():
    data = []

    fe = FieldExclude(f1="a", f2=data)
    fi = FieldInclude(f1="a", f2=data)
    de = DictExclude(f1=data, f2=data)
    n = NestedExclude(f="a", nested=de)
    m = Model(fe=fe, fi=fi, feo=fe, de=de, deo=de, n=n, no=n)
    return m


@pytest.mark.parametrize(
    "include,exclude,expected",
    [
        # skip - pydantic v2 does not support Field(include=...)
        # (
        #     None,
        #     None,
        #     {
        #         "fe": {"f1": "a"},
        #         "feo": {"f1": "a", "f2": []},
        #         "fi": {"f1": "a"},
        #         "deo": {"f1": [], "f2": []},
        #         "n": {"f": "a"},
        #         "no": {"nested": {"f1": []}},
        #     },
        # ),
        ({"n": {"f"}}, None, {"n": {"f": "a"}}),
        (None, {"n", "no", "deo", "feo"}, {"fe": {"f1": "a"}, "fi": {"f1": "a"}}),
    ],
)
def test_include_exclude(model: Model, include, exclude, expected):
    assert model.get_dict(include=include, exclude=exclude) == expected


class DictModel(MetricResult):
    __alias_required__: ClassVar[bool] = False

    de: Dict[str, DictExclude]
    deo: Dict[str, DictExclude] = Field(..., include=True)
    # fe: Dict[str, FieldExclude]
    # feo: Dict[str, FieldExclude] = Field(include={"f1", "f2"})


@pytest.fixture()
def dict_model():
    data = []

    # fe = FieldExclude(f1="a", f2=data)
    # fi = FieldInclude(f1="a", f2=data)
    de = {"a": DictExclude(f1=data, f2=data)}
    # n = NestedExclude(f="a", nested=de)
    return DictModel(de=de, deo=de)


@pydantic_v2_not_supported("pydantic v2 does not support Field(include=...)")
@pytest.mark.parametrize(
    "include,exclude,expected",
    [
        (
            None,
            None,
            {
                "deo": {"a": {"f1": [], "f2": []}},
            },
        ),
    ],
)
def test_include_exclude_dict(dict_model: DictModel, include, exclude, expected):
    assert dict_model.get_dict(include=include, exclude=exclude) == expected


def test_polymorphic():
    class Parent(MetricResult):
        __alias_required__: ClassVar[bool] = False

    class A(Parent):
        __dict_include_fields__: ClassVar[set] = {"f1"}
        __alias_required__: ClassVar[bool] = False

        f1: str
        f2: str

    class B(Parent):
        __dict_exclude_fields__: ClassVar[set] = {"b"}
        __alias_required__: ClassVar[bool] = False

        a: str
        b: str

    class PModel(MetricResult):
        __alias_required__: ClassVar[bool] = False

        vals: Dict[str, Parent]

    p_model = PModel(vals={"a": A(f1="a", f2="b"), "b": B(a="a", b="b")})
    assert p_model.get_dict() == {"vals": {"a": {"f1": "a"}, "b": {"a": "a"}}}


def test_model_enum():
    class MyEnum(Enum):
        A = "a"
        B = "b"

    class Container(EnumValueMixin, BaseModel):
        value: MyEnum

    obj = Container(value=MyEnum.A)
    assert obj.value == MyEnum.A
    d = obj.model_dump()
    assert d == {"value": "a"}
    obj2 = TypeAdapter(Container).validate_python(d)
    assert obj2.value == MyEnum.A
    assert obj2 == obj


def test_skip_type():
    class A(MetricResult):
        __alias_required__: ClassVar[bool] = False
        field: str

    res = A(field="aaa").get_dict()
    assert "type" not in res


def test_model_list():
    class SimpleField(MetricResult):
        __alias_required__: ClassVar[bool] = False

        field: str
        field2: str

    class Container(MetricResult):
        __alias_required__: ClassVar[bool] = False

        field: List[SimpleField]

    obj = Container(field=[SimpleField(field="a", field2="b")])
    assert obj.get_dict() == {"field": [{"field": "a", "field2": "b"}]}
