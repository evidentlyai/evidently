import abc

from dataclasses import dataclass
from numbers import Number
from typing import List
from typing import Optional
from typing import Union


@dataclass
class TestResult:
    # Constants for test result status
    SUCCESS = "SUCCESS"  # the test was passed
    FAIL = "FAIL"  # success pass for the test
    WARNING = "WARNING"  # the test was passed, but we have some issues during the execution
    ERROR = "ERROR"  # cannot calculate the test result, no data
    SKIPPED = "SKIPPED"  # the test was skipped

    name: str
    description: str
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

    def is_passed(self):
        return self.status in [self.SUCCESS, self.WARNING]


class Test:
    """
    all fields in test class with type that is subclass of Metric would be used as dependencies of test.
    """
    name: str

    @abc.abstractmethod
    def check(self):
        raise NotImplementedError()


@dataclass
class TestValueCondition:
    """
    Class for processing a value conditions - should it be less, greater than, equals and so on.

    An object of the class stores specified conditions and can be used for checking a value by them.
    """
    eq: Optional[Number] = None
    gt: Optional[Number] = None
    gte: Optional[Number] = None
    is_in: Optional[List[Union[Number, str, bool]]] = None
    lt: Optional[Number] = None
    lte: Optional[Number] = None
    not_eq: Optional[Number] = None
    not_in: Optional[List[Union[Number, str, bool]]] = None

    def check_value(self, value: Number) -> bool:
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


class BaseCheckValueTest(Test):
    """
    Base class for all tests with checking a value condition
    """
    value: Number

    def __init__(
            self,
            eq: Optional[Number] = None,
            gt: Optional[Number] = None,
            gte: Optional[Number] = None,
            is_in: Optional[List[Union[Number, str, bool]]] = None,
            lt: Optional[Number] = None,
            lte: Optional[Number] = None,
            not_eq: Optional[Number] = None,
            not_in: Optional[List[Union[Number, str, bool]]] = None,
    ):
        self.condition = TestValueCondition(
            eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in
        )

    @abc.abstractmethod
    def calculate_value_for_test(self) -> Number:
        """Method for getting the checking value.

        Define it in a child class"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_description(self, value: Number) -> str:
        """Method for getting a description that we can use.
        The description can use the checked value.

        Define it in a child class"""
        raise NotImplementedError()

    def check(self):
        result = TestResult(name=self.name, description="The test was not launched", status=TestResult.SKIPPED)
        value = self.calculate_value_for_test()
        result.description = self.get_description(value)

        try:
            condition_check_result = self.condition.check_value(value)

            if condition_check_result:
                result.mark_as_success()

            else:
                result.mark_as_fail()

        except ValueError:
            result.mark_as_error("Cannot calculate the condition")

        return result
