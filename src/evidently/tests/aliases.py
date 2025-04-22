from typing import Any
from typing import List
from typing import Optional
from typing import Union
from typing import overload

from evidently.core.datasets import DescriptorTest
from evidently.core.metric_types import MetricTest
from evidently.core.tests import FactoryGenericTest
from evidently.core.tests import GenericTest
from evidently.tests.categorical_tests import IsInMetricTest
from evidently.tests.categorical_tests import NotInMetricTest
from evidently.tests.descriptors import EqualsColumnCondition
from evidently.tests.descriptors import GreaterColumnCondition
from evidently.tests.descriptors import GreaterEqualColumnCondition
from evidently.tests.descriptors import IsInColumnCondition
from evidently.tests.descriptors import IsNotInColumnCondition
from evidently.tests.descriptors import LessColumnCondition
from evidently.tests.descriptors import LessEqualColumnCondition
from evidently.tests.descriptors import NotEqualsColumnCondition
from evidently.tests.numerical_tests import EqualMetricTest
from evidently.tests.numerical_tests import GreaterOrEqualMetricTest
from evidently.tests.numerical_tests import GreaterThanMetricTest
from evidently.tests.numerical_tests import LessOrEqualMetricTest
from evidently.tests.numerical_tests import LessThanMetricTest
from evidently.tests.numerical_tests import NotEqualMetricTest
from evidently.tests.numerical_tests import ThresholdType

AnyTest = Union[GenericTest, MetricTest, DescriptorTest]


@overload
def eq(expected: Any) -> GenericTest: ...


@overload
def eq(expected: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def eq(expected: Any, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def eq(
    expected: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: EqualMetricTest(expected=expected, is_critical=is_critical),
        lambda: DescriptorTest(condition=EqualsColumnCondition(expected=expected), column=column, alias=alias),
    )


@overload
def not_eq(expected: Any) -> GenericTest: ...


@overload
def not_eq(expected: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def not_eq(expected: Any, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def not_eq(
    expected: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: NotEqualMetricTest(expected=expected, is_critical=is_critical),
        lambda: DescriptorTest(condition=NotEqualsColumnCondition(expected=expected), column=column, alias=alias),
    )


@overload
def lt(threshold: ThresholdType) -> GenericTest: ...


@overload
def lt(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def lt(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def lt(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: LessThanMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=LessColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def gt(threshold: ThresholdType) -> GenericTest: ...


@overload
def gt(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def gt(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def gt(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: GreaterThanMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=GreaterColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def gte(threshold: ThresholdType) -> GenericTest: ...


@overload
def gte(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def gte(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def gte(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: GreaterOrEqualMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=GreaterEqualColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def lte(threshold: ThresholdType) -> GenericTest: ...


@overload
def lte(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def lte(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def lte(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: LessOrEqualMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=LessEqualColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def is_in(values: List[Union[int, str]]) -> GenericTest: ...


@overload
def is_in(values: List[Union[int, str]], *, is_critical: bool = True) -> MetricTest: ...


@overload
def is_in(
    values: List[Union[int, str]], *, column: Optional[str] = None, alias: Optional[str] = None
) -> DescriptorTest: ...


def is_in(
    values: List[Union[int, str]],
    *,
    is_critical: bool = True,
    column: Optional[str] = None,
    alias: Optional[str] = None,
) -> AnyTest:
    return FactoryGenericTest(
        lambda: IsInMetricTest(values=values, is_critical=is_critical),
        lambda: DescriptorTest(condition=IsInColumnCondition(values=set(values)), column=column, alias=alias),
    )


@overload
def not_in(values: List[Union[int, str]]) -> GenericTest: ...


@overload
def not_in(values: List[Union[int, str]], *, is_critical: bool = True) -> MetricTest: ...


@overload
def not_in(
    values: List[Union[int, str]], *, column: Optional[str] = None, alias: Optional[str] = None
) -> DescriptorTest: ...


def not_in(
    values: List[Union[int, str]],
    *,
    is_critical: bool = True,
    column: Optional[str] = None,
    alias: Optional[str] = None,
) -> AnyTest:
    return FactoryGenericTest(
        lambda: NotInMetricTest(values=values, is_critical=is_critical),
        lambda: DescriptorTest(condition=IsNotInColumnCondition(values=set(values)), column=column, alias=alias),
    )
