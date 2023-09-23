import abc
import inspect
from collections import defaultdict
from contextlib import contextmanager
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import ContextManager
from typing import Counter
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar

import pandas as pd
from pydantic import BaseModel

from evidently.base_metric import ColumnName
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition

if TYPE_CHECKING:
    from evidently2.core.suite import Report


class CalculationResult(EvidentlyBaseModel):
    pass


CI = TypeVar("CI")
CR = TypeVar("CR")

DataType = pd.DataFrame

_engines: List[Type["CalculationEngine"]] = []


class CalculationEngine:
    implementations: ClassVar[Dict[Type["_CalculationBase"], Type["CalculationImplementation"]]]

    @classmethod
    def can_use_engine(cls, data) -> bool:
        # todo
        raise NotImplementedError

    def __init_subclass__(cls):
        if cls is not CalculationEngine:
            _engines.append(cls)
            cls.implementations = {}


Calc = TypeVar("Calc", bound="_CalculationBase")


class CalculationImplementation(Generic[Calc]):
    engine: ClassVar[Type[CalculationEngine]]
    calculation_type: ClassVar[Type[Calc]]

    def __init_subclass__(cls):
        if not inspect.isabstract(cls) and hasattr(cls, "calculation_type"):
            cls.engine.implementations[cls.calculation_type] = cls

    @classmethod
    @abc.abstractmethod
    def calculate(cls, calculation: Calc, data):
        raise NotImplementedError


class _CalculationBase(EvidentlyBaseModel):
    @abc.abstractmethod
    def get_result(self):
        raise NotImplementedError

    @property
    def is_no_input_value(self):
        return isinstance(self, InputValue) and self._data is None

    def __repr__(self):
        return f"{self.__class__.__name__}_{str(hash(self))[:2]}"


class Calculation(_CalculationBase, Generic[CI, CR]):
    class Config:
        underscore_attrs_are_private = True

    engine: ClassVar[CalculationEngine]
    input_data: "_CalculationBase"
    _cache: bool = True

    # def __init__(self, input_data: _CalculationBase, **data):
    #     super().__init__(input_data=input_data, **data)

    def _get_implementation(self, data):
        for engine in _engines:
            if engine.can_use_engine(data) and self.__class__ in engine.implementations:
                return engine.implementations[self.__class__]
        raise NotImplementedError(
            f"No engine found for {self.__class__.__name__} for data of type {data.__class__.__name__}"
        )

    def calculate(self, data: CI) -> CR:
        return self._get_implementation(data).calculate(self, data)

    def get_result(self):
        with Context.current() as ctx:
            if self not in ctx.results:
                result = self.calculate(self.input_data.get_result())
                if self._cache:
                    ctx.results[self] = result
                # else:
                #     print("no cache")
                return result
            return ctx.results[self]

    # todo
    @property
    def empty(self):
        from evidently2.calculations.basic import IsEmpty

        return IsEmpty(input_data=self)

    def disable_cache(self):
        self._cache = False


class _Input(_CalculationBase):
    pass


class InputValue(_Input):
    class Config:
        underscore_attrs_are_private = True

    id: str
    _data: Any

    def bind(self, data):
        self._data = data
        return self

    def get_result(self):
        if self._data is None:
            # todo: temp
            with Context.current() as ctx:
                if self in ctx.results:
                    return ctx.results[self]
            raise NoInputError()
        return self._data


class Constant(_Input):
    value: Any

    def __init__(self, value: Any, **data):
        super().__init__(value=value, **data)

    def get_result(self):
        return self.value


def create_calculation_from_callable(func: callable):
    class CallableCalculation(Calculation):
        instance: Any = None

        def calculate(self, data: CI) -> CR:
            if self.instance is not None:
                return func(self.instance, data)
            return func(data)

    return CallableCalculation


class NoInputError(Exception):
    pass


class InputData:
    def __init__(self, current_data, reference_data, data_definition: DataDefinition):
        self._current_data = current_data
        self._reference_data = reference_data
        self.data_definition = data_definition

    @property
    def reference_data(self) -> _CalculationBase:
        return InputValue(id="reference").bind(self._reference_data)

    @property
    def current_data(self) -> _CalculationBase:
        return InputValue(id="current").bind(self._current_data)

    def get_current_column(self, column_name: ColumnName) -> "InputColumnData":
        return InputColumnData(input_data=self.current_data, column=column_name.name)

    def get_reference_column(self, column_name: ColumnName) -> "InputColumnData":
        return InputColumnData(input_data=self.reference_data, column=column_name.name)


class InputColumnData(Calculation):
    input_data: _CalculationBase
    column: str


def get_all_calculations(obj: BaseModel, *, _result=None) -> Dict[Calculation, Set[Calculation]]:
    _result = _result if _result is not None else defaultdict(set)
    is_calculation = isinstance(obj, Calculation)
    for field_name, field in obj.__fields__.items():
        field_type = field.type_
        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            # todo: lists, dicts etc
            field_value = getattr(obj, field_name)
            get_all_calculations(field_value, _result=_result)
            if is_calculation and issubclass(field_type, _CalculationBase) and not issubclass(field_type, _Input):
                _result[obj].add(field_value)
    return _result


def get_calculation_uses(obj: BaseModel) -> Counter[Calculation]:
    from collections import Counter

    result = Counter()
    for _, deps in get_all_calculations(obj).items():
        result.update(deps)
    return result


def partial_calculations(obj: BaseModel) -> Tuple[Set[Calculation], Set[Calculation]]:
    all_calc = get_all_calculations(obj)

    inversed = defaultdict(set)
    for calc, deps in all_calc.items():
        for d in deps:
            inversed[d].add(calc)

    skipping = {c for c in inversed if c.is_no_input_value}
    cur = set(skipping)
    while cur:
        cur = {parent for c in cur for parent in inversed[c]}
        skipping.update(cur)

    return skipping, {dep for c in skipping for dep in all_calc.get(c, []) if dep not in skipping}


class NoContextError(Exception):
    pass


class Context:
    _instance: Optional["Context"] = None

    def __init__(self):
        self.results: Dict[_CalculationBase, Any] = {}

    @classmethod
    @contextmanager
    def new(cls) -> ContextManager["Context"]:
        _prev = Context._instance
        Context._instance = Context()
        try:
            yield Context._instance
        finally:
            Context._instance = _prev

    @classmethod
    @contextmanager
    def current(cls) -> ContextManager["Context"]:
        if Context._instance is None:
            raise NoContextError("No current context")
        yield Context._instance

    @classmethod
    @contextmanager
    def use(cls, ctx: "Context") -> ContextManager["Context"]:
        _prev = Context._instance
        try:
            Context._instance = ctx
            yield ctx
        finally:
            Context._instance = _prev

    def add_profile_cache(self, profile: "ProfileCalculations"):
        for calc, res in zip(profile.calculations, profile.results):
            self.results[calc] = res

    def get_profile_cache(self, calculations: List[Calculation]):
        with Context.use(self):
            return ProfileCalculations(calculations=calculations, results=[c.get_result() for c in calculations])

    # def get_profile_for(self, obj: BaseModel):


class ProfileCalculations(BaseModel):
    calculations: List[_CalculationBase]
    results: List[Any]

    def merge(self, other: "ProfileCalculations"):
        calc_set = set(self.calculations)
        add_calc = []
        add_res = []
        for calc, res in zip(other.calculations, other.results):
            if calc in calc_set:
                continue
            add_calc.append(calc)
            add_res.append(res)
        return ProfileCalculations(calculations=self.calculations + add_calc, results=self.results + add_res)


class Profile(BaseModel):
    cache: ProfileCalculations
    metrics: List["BaseMetric"]
    metric_calculations: List["MetricResultCalculation"]

    # todo: move from here
    def run(self, current_data: DataType) -> "Report":
        from evidently2.core.suite import Report

        report = Report(metrics=self.metrics)
        report._ctx.add_profile_cache(self.cache)
        report._ctx.results[InputValue(id="current")] = current_data
        with Context.use(report._ctx):
            for metric, calculation in zip(self.metrics, self.metric_calculations):
                report._metric_results[metric] = calculation.get_result()
        return report


# todo

from evidently2.core.metric import BaseMetric
from evidently2.core.metric import MetricResultCalculation

Profile.update_forward_refs()
