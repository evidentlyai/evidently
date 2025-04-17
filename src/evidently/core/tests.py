from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Callable

if TYPE_CHECKING:
    from .datasets import DescriptorTest
    from .metric_types import MetricTest


class GenericTest:
    @abstractmethod
    def for_metric(self) -> "MetricTest":
        raise NotImplementedError

    @abstractmethod
    def for_descriptor(self) -> "DescriptorTest":
        raise NotImplementedError


class FactoryGenericTest(GenericTest):
    def __init__(self, metric: Callable[[], "MetricTest"], descriptor: Callable[[], "DescriptorTest"]):
        self.metric = metric

        self.descriptor = descriptor

    def for_metric(self) -> "MetricTest":
        return self.metric()

    def for_descriptor(self) -> "DescriptorTest":
        return self.descriptor()
