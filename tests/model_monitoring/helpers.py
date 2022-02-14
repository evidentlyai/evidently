"""Common methods for monitoring testing"""

from collections import defaultdict
from typing import Any
from typing import Dict
from typing import Generator
from typing import List

from evidently.model_monitoring.monitoring import MetricsType


def collect_metrics_results(metrics: Generator[MetricsType, None, None]) -> Dict[str, List[Dict[str, Any]]]:
    """Represent monitoring results as a dict with all collected metrics. Group by a metric name.

    Returns a dict like:
    {
        "monitor_type_prefix_1:metric_1": [
            {'labels': {'dataset': 'reference', 'metric': 'accuracy'}, 'value': 0.5},
            {'labels': {'dataset': 'reference', 'metric': 'accuracy'}, 'value': 0.5},
            ...
        ],
        "monitor_type_prefix_2:metric_1": [
            {'labels': {'class_name': 'label_a', 'dataset': 'reference', 'type': 'target'}, 'value': 3},
        ...
    }

    Where in a list element:
        - labels: a dict with a label name as a key and a label value as a value of the label
        - value: the metric value
    """
    result = defaultdict(list)

    for metric, value, labels in metrics:
        result[metric.name].append(
            {
                "value": value,
                "labels": labels,
            }
        )
    return result
