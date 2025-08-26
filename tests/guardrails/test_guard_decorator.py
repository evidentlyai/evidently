from typing import Callable

import pytest

from evidently.guardrails import GuardException
from evidently.guardrails import PythonFunction
from evidently.guardrails import guard


def stub_guard_factory(result: bool) -> Callable[[str], bool]:
    def stub_guard(data: str) -> bool:
        return result

    return stub_guard


@guard(PythonFunction(stub_guard_factory(True)))
def success_operation(input: str) -> str:
    return input


@guard(
    [
        PythonFunction(stub_guard_factory(True)),
    ]
)
def success_operation_multiple_guards(input: str) -> str:
    return input


@pytest.mark.parametrize(
    "func,args",
    [
        (success_operation, ["test"]),
        (success_operation_multiple_guards, ["test"]),
    ],
)
def test_guard_decorator_success(func, args):
    assert func(*args) == args[0]


@guard(PythonFunction(stub_guard_factory(False)))
def failed_operation(input: str) -> str:
    return input


@guard(
    [
        PythonFunction(stub_guard_factory(False)),
        PythonFunction(stub_guard_factory(False)),
    ]
)
def failed_operation_multiple_guards(input: str) -> str:
    return input


@pytest.mark.parametrize(
    "func,args",
    [
        (failed_operation, ["test"]),
        (failed_operation_multiple_guards, ["test"]),
    ],
)
def test_guard_decorator_failed(func, args):
    with pytest.raises(GuardException):
        func(*args)
