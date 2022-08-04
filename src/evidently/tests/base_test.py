import abc
from abc import ABC

import dataclasses
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
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
    ByFeature = GroupTypeData("by_feature", "By feature", [])
    ByClass = GroupTypeData("by_class", "By class", [])
    TestGroup = GroupTypeData("test_group", "By test group", [])
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


class TestColumn:
    """Base test class for a test that checks one column"""
    column_name: str

    def __init__(self, column_name: str):
        self.column_name = column_name


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


def _generate_tests_for_columns_list_from_method(
    test_class: Type[TestColumn],
    list_columns_method: Callable,
    for_all_parameters: Optional[Dict] = None,
    per_column_parameters: Optional[Dict] = None,
) -> BaseTestGenerator:

    class TestForOneColumn(BaseTestGenerator):
        def generate_tests(self, columns_info: DatasetColumns) -> List[TestColumn]:
            result = []

            for column_name in list_columns_method(columns_info):
                if per_column_parameters is not None and column_name in per_column_parameters:
                    actual_parameters = per_column_parameters[column_name]

                else:
                    actual_parameters = for_all_parameters or {}

                actual_parameters["column_name"] = column_name
                result.append(test_class(**actual_parameters))

            return result

    return TestForOneColumn()


def generate_tests_for_columns(
        test_class: Type[TestColumn],
        columns: List[str],
        for_all_parameters: Optional[Dict] = None,
        per_column_parameters: Optional[Dict] = None,
) -> BaseTestGenerator:
    """Generate tests for specified columns"""
    def list_columns(_: DatasetColumns) -> List[str]:
        return columns

    return _generate_tests_for_columns_list_from_method(
        test_class=test_class,
        list_columns_method=list_columns,
        for_all_parameters=for_all_parameters,
        per_column_parameters=per_column_parameters,
    )


def generate_tests_for_all_columns(
        test_class: Type[TestColumn],
        for_all_parameters: Optional[Dict] = None,
        per_column_parameters: Optional[Dict] = None,
) -> BaseTestGenerator:
    """Generate tests for all columns"""
    def list_all_columns(columns_info: DatasetColumns) -> List[str]:
        return columns_info.get_all_columns_list()

    return _generate_tests_for_columns_list_from_method(
        test_class=test_class,
        list_columns_method=list_all_columns,
        for_all_parameters=for_all_parameters,
        per_column_parameters=per_column_parameters,
    )


def generate_tests_for_num_features(
        test_class: Type[TestColumn],
        for_all_parameters: Optional[Dict] = None,
        per_column_parameters: Optional[Dict] = None
) -> BaseTestGenerator:
    """Generate tests for numeric features"""
    def list_num_features_columns(columns_info: DatasetColumns) -> List[str]:
        return columns_info.num_feature_names

    return _generate_tests_for_columns_list_from_method(
        test_class=test_class,
        list_columns_method=list_num_features_columns,
        for_all_parameters=for_all_parameters,
        per_column_parameters=per_column_parameters,
    )


def generate_tests_for_cat_features(
    test_class: Type[TestColumn],
    for_all_parameters: Optional[Dict] = None,
    per_column_parameters: Optional[Dict] = None
) -> BaseTestGenerator:
    """Generate tests for category features"""
    def list_cat_features_columns(columns_info: DatasetColumns) -> List[str]:
        return columns_info.cat_feature_names

    return _generate_tests_for_columns_list_from_method(
        test_class=test_class,
        list_columns_method=list_cat_features_columns,
        for_all_parameters=for_all_parameters,
        per_column_parameters=per_column_parameters,
    )


def generate_tests_for_datetime_features(
    test_class: Type[TestColumn],
    for_all_parameters: Optional[Dict] = None,
    per_column_parameters: Optional[Dict] = None
) -> BaseTestGenerator:
    """Generate tests for datetime features"""
    def list_numeric_features_columns(columns_info: DatasetColumns) -> List[str]:
        return columns_info.datetime_feature_names

    return _generate_tests_for_columns_list_from_method(
        test_class=test_class,
        list_columns_method=list_numeric_features_columns,
        for_all_parameters=for_all_parameters,
        per_column_parameters=per_column_parameters,
    )
