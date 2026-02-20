import abc
import glob
import json
import os
from importlib import import_module
from inspect import isabstract
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin

from pydantic import BaseModel
from pydantic import model_validator

import evidently
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.report import Report
from evidently.legacy.utils.types import ApproxValue
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import get_field_inner_type
from tests.conftest import smart_assert_equal


class TestOutcome:
    @abc.abstractmethod
    def check(self, report: Report):
        raise NotImplementedError


class Error(TestOutcome):
    def __init__(self, exception_type: Type[Exception], match: str = None):
        self.exception_type = exception_type
        self.match = match

    def check(self, report: Report):
        pass


class AssertResultFields(TestOutcome):
    def __init__(self, values: Dict[str, Any]):
        # todo: nested keys
        self.values = values

    def check(self, report: Report):
        result_json = report.json()
        result = json.loads(result_json)["metrics"][0]["result"]

        for key, value in self.values.items():
            assert result[key] == value


class AssertExpectedResult(TestOutcome):
    def __init__(self, result: MetricResult, metric: Optional[Metric] = None):
        self.metric = metric
        self.result = result

    def check(self, report: Report):
        if self.metric is None:
            metrics = list(report._inner_suite.context.metric_results.keys())
            if len(metrics) != 1:
                raise ValueError(
                    f"Metric is not specified for AssertExpectedResult and context does not contain exactly 1 metric: {metrics}"
                )
            metric = metrics[0]
        else:
            metric = self.metric
        result = report._inner_suite.context.metric_results[metric]
        smart_assert_equal(result, self.result)


class CustomAssert(TestOutcome):
    def __init__(self, custom_check: Callable[[Report], None]):
        self.custom_check = custom_check

    def check(self, report: Report):
        self.custom_check(report)


class NoopOutcome(TestOutcome):
    def check(self, report: Report):
        pass


def find_all_subclasses(
    base: Type,
    base_module: str = "evidently",
    path: str = os.path.dirname(evidently.__file__),
    include_abstract: bool = False,
):
    classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = f"{base_module}." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not base and issubclass(value, base):
                if not isabstract(value) or include_abstract:
                    classes.add(value)

    return classes


T = TypeVar("T", bound=BaseModel)


def make_approx_type(original_cls: Type[T], ignore_not_set: bool = False) -> Type[T]:
    optional = False
    if get_origin(original_cls) is Optional:
        original_cls = get_args(original_cls)[0]
        optional = True

    class ApproxFields(original_cls):
        __alias_required__: ClassVar[bool] = False
        if isinstance(original_cls, type) and issubclass(original_cls, PolymorphicModel):
            __type_alias__: ClassVar[str] = original_cls.__get_type__()

        __ignore_not_set__ = ignore_not_set
        __annotations__ = {
            k: Union[ApproxValue, f.annotation]
            if not isinstance(get_field_inner_type(f), type) or not issubclass(get_field_inner_type(f), BaseModel)
            else make_approx_type(get_field_inner_type(f))
            for k, f in original_cls.__fields__.items()
        }
        locals().update({k: f.default for k, f in original_cls.__fields__.items()})

        def __eq__(self, other):
            if ignore_not_set:
                d = {k: v for k, v in self.dict().items() if v is not None}
                d2 = {k: v for k, v in other.dict().items() if k in d}
                return d == d2
            return super().__eq__(other)

        @model_validator(mode="before")
        def allow_parent(cls, value):
            if isinstance(value, original_cls):
                value = value.model_dump()
            return value

    if issubclass(original_cls, PolymorphicModel):
        ApproxFields.__fields__["type"].default = original_cls.__fields__["type"].default

    ApproxFields.__name__ = f"Approx{original_cls.__name__}"
    return ApproxFields if not optional else Optional[ApproxFields]
