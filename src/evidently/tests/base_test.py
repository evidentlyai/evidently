import abc
from abc import ABC

import dataclasses
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from evidently.analyzers.utils import DatasetColumns
from evidently.tests.utils import ApproxValue
from evidently.tests.utils import Numeric


@dataclasses.dataclass
class GroupData:
    id: str
    title: str
    description: str
    sort_index: int = 0
    severity: Optional[str] = None


@dataclasses.dataclass
class GroupTypeData:
    id: str
    title: str
    # possible values with description, if empty will use simple view (no severity, description and sorting).
    values: List[GroupData] = dataclasses.field(default_factory=list)

    def add_value(self, data: GroupData):
        self.values.append(data)


class GroupingTypes:
    ByFeature = GroupTypeData("by_feature", "By feature", [GroupData(
        "no group",
        "Dataset-level tests",
        "Some tests cannot be grouped by feature",
    )])
    ByClass = GroupTypeData("by_class", "By class", [])
    TestGroup = GroupTypeData("test_group", "By test group", [GroupData(
        "no group",
        "Ungrouped",
        "Some tests don’t belong to any group under the selected condition",
    )])
    TestType = GroupTypeData("test_type", "By test type", [])


DEFAULT_GROUP = [
    GroupingTypes.ByFeature,
    GroupingTypes.TestGroup,
    GroupingTypes.TestType,
    GroupingTypes.ByClass
]


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
    # grouping parameters
    groups: Dict[str, str] = dataclasses.field(default_factory=dict)

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
    def check(self) -> TestResult:
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

    def has_condition(self) -> bool:
        """
        Checks if we have a condition in the object and returns True in this case.

        If we have no conditions - returns False.
        """
        return any(
            value is not None
            for value in (self.eq, self.gt, self.gte, self.is_in, self.lt, self.lte, self.not_in, self.not_eq)
        )

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

    def groups(self) -> Dict[str, str]:
        return {}

    def check(self):
        result = TestResult(name=self.name, description="The test was not launched", status=TestResult.SKIPPED)
        value = self.calculate_value_for_test()
        self.value = value
        result.description = self.get_description(value)

        try:
            if value is None:
                result.mark_as_error()

            else:
                condition = self.get_condition()

                if condition is None:
                    raise ValueError

                condition_check_result = condition.check_value(value)

                if condition_check_result:
                    result.mark_as_success()

                else:
                    result.mark_as_fail()

        except ValueError:
            result.mark_as_error("Cannot calculate the condition")

        result.groups.update(self.groups())
        return result


TTest = TypeVar("TTest")


class BaseTestGenerator(Generic[TTest]):
    """Base class for tests generator creation

    To create a new generator:
        - inherit a class from the base class
        - implement `generate_tests` method and return a list of test objects from it

    Test Suite will call the method and add generated tests to its list instead of the generator object.

    You can use `columns_info` parameter in `generate_tests` for getting data structure meta info like columns list.

    For example:
        if you want to create a test generator for 50, 90, 99 quantiles tests
        for all numeric columns with default condition, by reference quantiles

    class TestQuantiles(BaseTestGenerator):
        def generate_tests(self, columns_info: DatasetColumns) -> List[TestValueQuantile]:
            return [
                TestValueQuantile(column_name=name, quantile=quantile)
                for quantile in (0.5, 0.9, 0.99)
                for name in columns_info.num_feature_names
            ]

    Do not forget set correct test type for `generate_tests` return value
    """
    @abc.abstractmethod
    def generate_tests(self, columns_info: DatasetColumns) -> List[TTest]:
        raise NotImplementedError()


def generate_column_tests(
    test_class: Type[Test],
    columns: Optional[Union[str, list]] = None,
    parameters: Optional[Dict] = None,
) -> BaseTestGenerator:
    """Create a test generator for a columns list with a test class.

    Test class is specified with `test_class` parameter.
    If the test have no "column_name" parameter - TypeError will be raised.

    Columns list can be defined with parameter `columns`.
    If it is a list - just use it as a list of the columns.
    If `columns` is a string, it can be one of values:
    - "all" - make tests for all columns, including target/prediction columns
    - "num" - for numeric features
    - "cat" - for category features
    - "features" - for all features, not target/prediction columns.
    None value is the same as "all".
    If `columns` is string and it is not one of the values, ValueError will be raised.

    `parameters` is used for specifying other parameters for each test, it is the same for all generated tests.
    """
    if parameters is None:
        parameters_for_test: Dict = {}

    else:
        parameters_for_test = parameters

    class TestColumnsGenerator(BaseTestGenerator):
        def generate_tests(self, columns_info: DatasetColumns) -> List[Test]:
            nonlocal parameters_for_test
            result = []

            if isinstance(columns, list):
                columns_for_tests = columns

            elif columns == "all" or columns is None:
                columns_for_tests = columns_info.get_all_columns_list()

            elif columns == "cat":
                columns_for_tests = columns_info.cat_feature_names

            elif columns == "num":
                columns_for_tests = columns_info.num_feature_names

            elif columns == "features":
                columns_for_tests = columns_info.get_all_features_list(include_datetime_feature=True)

            else:
                raise ValueError("Incorrect parameter 'columns' for test generator")

            for column_name in columns_for_tests:
                parameters_for_test["column_name"] = column_name
                # ignore possible parameters incompatibility
                # we cannot guarantee that a test class has column_name parameter
                # if it has not, type error will ve raised
                try:
                    result.append(test_class(**parameters_for_test))  # type: ignore

                except TypeError as error:
                    raise TypeError(f"Cannot generate test {test_class.__name__}. Error: {error}")

            return result

    return TestColumnsGenerator()
