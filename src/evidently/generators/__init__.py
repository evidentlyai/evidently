"""Metric generators for creating multiple metrics programmatically.

Generators help create multiple related metrics efficiently, such as generating
the same metric for multiple columns or creating metric combinations.

Example:
```python
from evidently.metrics import MeanValue
from evidently.generators import ColumnMetricGenerator

# Generate MeanValue for all numerical columns
metrics = ColumnMetricGenerator(MeanValue, columns=["age", "salary", "score"])
```
"""

from .column import ColumnMetricGenerator

__all__ = ["ColumnMetricGenerator"]
