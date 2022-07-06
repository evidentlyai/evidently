import abc
from abc import ABC

from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from evidently.tests.utils import ApproxValue
from evidently.tests.utils import Numeric


@dataclass
class TestResult:
    # Constants for test result status
    SUCCESS = "SUCCESS"  # the test was passed
    FAIL = "FAIL"  # success pass for the test
    WARNING = "WARNING"  # the test was passed, but we have some issues during the execution
    ERROR = "ERROR"  # cannot calculate the test result, no data
    SKIPPED = "SKIPPED"  # the test was skipped

    # short name/title from the test class
    name: str
    # what was checked, what threshold (current value 13 is not ok with condition less than 5)
    description: str
    # status of the test result
    status: str

    def set_status(self, status: str, description: Optional[str] = None) -> None:
        self.status = status

        if description is not None:
            self.description = description

    def mark_as_fail(self, description: Optional[str] = None):
        self.set_status(self.FAIL, description=description)

    def mark_as_error(self, description: Optional[str] = None):
        self.set_status(self.ERROR, description=description)

    def mark_as_success(self, description: Optional[str] = None):
        self.set_status(self.SUCCESS, description=description)

    def mark_as_warning(self, description: Optional[str] = None):
        self.set_status(self.WARNING, description=description)

    def is_passed(self):
        return self.status in [self.SUCCESS, self.WARNING]


class Test:
    """
    all fields in test class with type that is subclass of Metric would be used as dependencies of test.
    """

    name: str
    group: str
    context = None

    @abc.abstractmethod
    def check(self):
        raise NotImplementedError()

    def set_context(self, context):
        self.context = context

    def get_result(self):
        if self.context is None:
            raise ValueError("No context is set")
        result = self.context.test_results.get(self, None)
        if result is None:
            raise ValueError(f"No result found for metric {self} of type {type(self).__name__}")
        return result


@dataclass
class TestValueCondition:
    """
    Class for processing a value conditions - should it be less, greater than, equals and so on.

    An object of the class stores specified conditions and can be used for checking a value by them.
    """

    eq: Optional[Numeric] = None
    gt: Optional[Numeric] = None
    gte: Optional[Numeric] = None
    is_in: Optional[List[Union[Numeric, str, bool]]] = None
    lt: Optional[Numeric] = None
    lte: Optional[Numeric] = None
    not_eq: Optional[Numeric] = None
    not_in: Optional[List[Union[Numeric, str, bool]]] = None

    def is_set(self) -> bool:
        return any([self.eq, self.gt, self.gte, self.is_in, self.lt, self.lte, self.not_in, self.not_eq])

    def check_value(self, value: Numeric) -> bool:
        result = True

        if self.eq is not None and result:
            result = value == self.eq

        if self.gt is not None and result:
            result = value > self.gt

        if self.gte is not None and result:
            result = value >= self.gte

        if self.is_in is not None and result:
            result = value in self.is_in

        if self.lt is not None and result:
            result = value < self.lt

        if self.lte is not None and result:
            result = value <= self.lte

        if self.not_eq is not None and result:
            result = value != self.not_eq

        if self.not_in is not None and result:
            result = value not in self.not_in

        return result

    def __str__(self) -> str:
        conditions = []
        operations = ["eq", "gt", "gte", "lt", "lte", "not_eq", "is_in", "not_in"]

        for op in operations:
            value = getattr(self, op)

            if value is None:
                continue

            if isinstance(value, (float, ApproxValue)):
                conditions.append(f"{op}={value:.3g}")

            else:
                conditions.append(f"{op}={value}")

        return f"{' and '.join(conditions)}"

    def as_dict(self) -> dict:
        result = {}
        operations = ["eq", "gt", "gte", "lt", "lte", "not_eq", "is_in", "not_in"]

        for op in operations:
            value = getattr(self, op)

            if value is not None:
                result[op] = value

        return result


class BaseConditionsTest(Test, ABC):
    """
    Base class for all tests with a condition
    """

    condition: TestValueCondition

    def __init__(
        self,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        self.condition = TestValueCondition(
            eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in
        )


class BaseCheckValueTest(BaseConditionsTest):
    """
    Base class for all tests with checking a value condition
    """

    value: Numeric

    @abc.abstractmethod
    def calculate_value_for_test(self) -> Optional[Any]:
        """Method for getting the checking value.

        Define it in a child class"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_description(self, value: Numeric) -> str:
        """Method for getting a description that we can use.
        The description can use the checked value.

        Define it in a child class"""
        raise NotImplementedError()

    def get_condition(self) -> TestValueCondition:
        return self.condition

    def check(self):
        result = TestResult(name=self.name, description="The test was not launched", status=TestResult.SKIPPED)
        value = self.calculate_value_for_test()
        self.value = value
        result.description = self.get_description(value)

        try:
            if value is None:
                result.mark_as_error()

            else:
                condition_check_result = self.get_condition().check_value(value)

                if condition_check_result:
                    result.mark_as_success()

                else:
                    result.mark_as_fail()

        except ValueError:
            result.mark_as_error("Cannot calculate the condition")

        return result
