import abc

from dataclasses import dataclass


@dataclass
class TestResult:
    name: str
    description: str
    status: str


class Test:
    """
    all fields in test class with type that is subclass of Metric would be used as dependencies of test.
    """
    @abc.abstractmethod
    def check(self):
        raise NotImplementedError()
