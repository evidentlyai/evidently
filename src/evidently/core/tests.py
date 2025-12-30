from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
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
    """Reference value for threshold comparisons.

    Used in tests to compare metric values against reference data. Can specify
    either a relative change (percentage) or absolute difference, or both.
    """

    relative: Optional[float] = None
    """Optional relative change threshold (percentage as decimal, e.g., 0.1 for 10%)."""
    absolute: Optional[float] = None
    """Optional absolute difference threshold."""

    def __hash__(self) -> int:
        return hash(self.relative) + hash(self.absolute)


ThresholdType = Union[float, int, ApproxValue, Reference]
"""Type alias for threshold values: numeric, approximate, or reference-based."""
ThresholdValue = Union[float, int, ApproxValue]
"""Type alias for threshold values: numeric or approximate."""


def threshold_typecheck_guard(value: Any):
    """Validate that a value is a valid threshold type.

    Args:
    * `value`: Value to validate.

    Raises:
    * `ValueError`: If value is not a valid threshold type.
    """
    if isinstance(value, get_args(ThresholdType)):
        raise ValueError("Invalid type for threshold value: {}, but expected {}".format(type(value), ThresholdType))


class GenericTest(BaseModel):
    """Unified test interface for both metrics and descriptors.

    `GenericTest` provides a single interface for tests that can work with both
    metric results and descriptor values. It contains both metric and descriptor
    test implementations and automatically selects the appropriate one.
    """

    test_name: str
    """Name of the test (e.g., "gt", "lt", "between")."""
    metric: Optional["MetricTest"]
    """Optional `MetricTest` implementation for metric results."""
    descriptor: Optional["DescriptorTest"]
    """Optional `DescriptorTest` implementation for descriptor values."""

    def for_metric(self) -> "MetricTest":
        """Get the metric test implementation.

        Returns:
        * `MetricTest` for this test.

        Raises:
        * `ValueError`: If metric test is not available.
        """
        if self.metric is None:
            raise ValueError(f"Test '{self.test_name}' does not have an implementation for metrics")
        return self.metric

    def for_descriptor(self) -> "DescriptorTest":
        """Get the descriptor test implementation.

        Returns:
        * `DescriptorTest` for this test.

        Raises:
        * `ValueError`: If descriptor test is not available.
        """
        if self.descriptor is None:
            raise ValueError(f"Test '{self.test_name}' does not have an implementation for descriptors")
        return self.descriptor

    def bind_single(self, fingerprint: Fingerprint) -> "BoundTest":
        """Bind this test to a single-value metric.

        Args:
        * `fingerprint`: Metric fingerprint to bind to.

        Returns:
        * `BoundTest` bound to the metric.
        """
        return self.for_metric().bind_single(fingerprint)

    def bind_count(self, fingerprint: Fingerprint, is_count: bool) -> "BoundTest":
        """Bind this test to a count metric.

        Args:
        * `fingerprint`: Metric fingerprint to bind to.
        * `is_count`: If `True`, test the count value; if `False`, test the share value.

        Returns:
        * `BoundTest` bound to the metric.
        """
        return self.for_metric().bind_count(fingerprint, is_count)

    def bind_by_label(self, fingerprint: Fingerprint, label: Label):
        """Bind this test to a by-label metric for a specific label.

        Args:
        * `fingerprint`: Metric fingerprint to bind to.
        * `label`: Label to test.

        Returns:
        * `BoundTest` bound to the metric and label.
        """
        return self.for_metric().bind_by_label(fingerprint, label)

    def bind_by_label_count(self, fingerprint: Fingerprint, label: Label, slot: "ByLabelCountSlot"):
        """Bind this test to a by-label-count metric.

        Args:
        * `fingerprint`: Metric fingerprint to bind to.
        * `label`: Label to test.
        * `slot`: Whether to test "count" or "share".

        Returns:
        * `BoundTest` bound to the metric, label, and slot.
        """
        return self.for_metric().bind_by_label_count(fingerprint, label, slot)

    def bind_mean_std(self, fingerprint: Fingerprint, is_mean: bool = True):
        """Bind this test to a mean-std metric.

        Args:
        * `fingerprint`: Metric fingerprint to bind to.
        * `is_mean`: If `True`, test the mean value; if `False`, test the std value.

        Returns:
        * `BoundTest` bound to the metric.
        """
        return self.for_metric().bind_mean_std(fingerprint, is_mean)

    def bind_dataframe(self, fingerprint: Fingerprint, column: str, label_filters: Optional[Dict[str, str]] = None):
        """Bind this test to a dataframe metric column.

        Args:
        * `fingerprint`: Metric fingerprint to bind to.
        * `column`: Column name in the dataframe to test.
        * `label_filters`: Optional filters to select specific rows by label values.

        Returns:
        * `BoundTest` bound to the metric, column, and filters.
        """
        return self.for_metric().bind_dataframe(fingerprint, column, label_filters)
