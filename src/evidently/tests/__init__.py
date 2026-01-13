"""Test conditions for validating metric results.

Tests add pass/fail conditions to metrics. They check if metric values meet
specific criteria and return test status (pass, fail, warning, error).

Use test condition functions to create tests:
- Comparison: `gt()`, `lt()`, `gte()`, `lte()`, `eq()`, `not_eq()`
- Membership: `is_in()`, `not_in()`
- Reference-based: `Reference()` for relative comparisons

Tests can be added to metrics when creating a `Report`, or automatically
generated when using presets with `include_tests=True`.

**Documentation**: See [Tests Guide](https://docs.evidentlyai.com/docs/library/tests) for detailed usage.

Example:
```python
from evidently import Report
from evidently.metrics import MeanValue
from evidently.tests import gt

report = Report([
    MeanValue(column="age").add_test(gt(25))
])
snapshot = report.run(dataset, None)
```
"""

from evidently.core.tests import Reference

from .aliases import eq
from .aliases import gt
from .aliases import gte
from .aliases import is_in
from .aliases import lt
from .aliases import lte
from .aliases import not_eq
from .aliases import not_in

__all__ = [
    "eq",
    "not_eq",
    "gt",
    "gte",
    "is_in",
    "not_in",
    "lt",
    "lte",
    "Reference",
]
