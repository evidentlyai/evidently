from dataclasses import dataclass

from evidently.suites.base_suite import BaseSuit
from evidently.suites.metrics.source_metadata_metrics import DatasetMetadataMetric


@dataclass
class DataQualitySuite(BaseSuit):
    metrics = [
        DatasetMetadataMetric
    ]
    tests = [
        TestNumberOfRows(reference_gt=0)
    ]
