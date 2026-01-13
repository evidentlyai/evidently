"""Pre-configured metric collections for common evaluation scenarios.

Presets combine multiple related `Metric` objects into convenient templates
for specific evaluation tasks. They provide a quick way to run comprehensive
evaluations without manually selecting individual metrics.

Available presets:
- `DataSummaryPreset`: Overview statistics for all columns
- `DataDriftPreset`: Detect distribution shifts across columns
- `ClassificationPreset`: Comprehensive classification quality metrics
- `RegressionPreset`: Comprehensive regression quality metrics
- `TextEvals`: Summarize text descriptor results
- `RecsysPreset`: Ranking and recommendation metrics

**Documentation**: See [All Presets](https://docs.evidentlyai.com/metrics/all_presets) for a complete reference.

Example:
```python
from evidently import Report
from evidently.presets import DataSummaryPreset

report = Report([DataSummaryPreset()])
snapshot = report.run(dataset, None)
```
"""

from .classification import ClassificationDummyQuality
from .classification import ClassificationPreset
from .classification import ClassificationQuality
from .classification import ClassificationQualityByLabel
from .dataset_stats import DatasetStats
from .dataset_stats import DataSummaryPreset
from .dataset_stats import TextEvals
from .dataset_stats import ValueStats
from .drift import DataDriftPreset
from .recsys import RecsysPreset
from .regression import RegressionDummyQuality
from .regression import RegressionPreset
from .regression import RegressionQuality

__all__ = [
    "ClassificationDummyQuality",
    "ClassificationPreset",
    "ClassificationQuality",
    "ClassificationQualityByLabel",
    "ValueStats",
    "TextEvals",
    "DatasetStats",
    "DataSummaryPreset",
    "RegressionDummyQuality",
    "RegressionQuality",
    "RegressionPreset",
    "DataDriftPreset",
    "RecsysPreset",
]
