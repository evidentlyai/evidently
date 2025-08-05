from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union
from typing import get_args

from evidently._pydantic_compat import BaseModel
from evidently.core.base_types import Label
from evidently.legacy.utils.types import ApproxValue
from evidently.pydantic_utils import Fingerprint

if TYPE_CHECKING:
    from .datasets import DescriptorTest
    from .metric_types import BoundTest
    from .metric_types import ByLabelCountSlot
    from .metric_types import MetricTest


class Reference(BaseModel):
    relative: Optional[float] = None
    absolute: Optional[float] = None

    def __hash__(self) -> int:
        return hash(self.relative) + hash(self.absolute)


ThresholdType = Union[float, int, ApproxValue, Reference]
ThresholdValue = Union[float, int, ApproxValue]


def threshold_typecheck_guard(value: Any):
    if isinstance(value, get_args(ThresholdType)):
        raise ValueError("Invalid type for threshold value: {}, but expected {}".format(type(value), ThresholdType))


class GenericTest(BaseModel):
    test_name: str
    metric: Optional["MetricTest"]
    descriptor: Optional["DescriptorTest"]

    def for_metric(self) -> "MetricTest":
        if self.metric is None:
            raise ValueError(f"Test '{self.test_name}' does not have an implementation for metrics")
        return self.metric

    def for_descriptor(self) -> "DescriptorTest":
        if self.descriptor is None:
            raise ValueError(f"Test '{self.test_name}' does not have an implementation for descriptors")
        return self.descriptor

    def bind_single(self, fingerprint: Fingerprint) -> "BoundTest":
        return self.for_metric().bind_single(fingerprint)

    def bind_count(self, fingerprint: Fingerprint, is_count: bool) -> "BoundTest":
        return self.for_metric().bind_count(fingerprint, is_count)

    def bind_by_label(self, fingerprint: Fingerprint, label: Label):
        return self.for_metric().bind_by_label(fingerprint, label)

    def bind_by_label_count(self, fingerprint: Fingerprint, label: Label, slot: "ByLabelCountSlot"):
        return self.for_metric().bind_by_label_count(fingerprint, label, slot)

    def bind_mean_std(self, fingerprint: Fingerprint, is_mean: bool = True):
        return self.for_metric().bind_mean_std(fingerprint, is_mean)
