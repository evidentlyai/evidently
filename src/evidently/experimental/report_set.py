import datetime
import os
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from pydantic import ValidationError

from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.report import Report
from evidently.suite.base_suite import Display


def load_metric_report_set(
    path: str,
    date_from: Optional[datetime.datetime] = None,
    date_to: Optional[datetime.datetime] = None,
    metrics: Optional[List[Metric]] = None,
) -> Dict[Metric, Dict[datetime.datetime, MetricResult]]:
    reports = load_report_set(path, Report, date_from, date_to)
    result: Dict[Metric, Dict[datetime.datetime, MetricResult]] = defaultdict(dict)
    if metrics is None:
        for timestamp, report in reports.items():
            for metric in report._first_level_metrics:
                result[metric][timestamp] = metric.get_result()
        return result
    for metric in metrics:
        for timestamp, report in reports.items():
            if metric in report._first_level_metrics:
                metric.set_context(report._inner_suite.context)
                result[metric][timestamp] = metric.get_result()
    return result


T = TypeVar("T", bound=Display)


def load_report_set(
    path: str,
    cls: Type[T],
    date_from: Optional[datetime.datetime] = None,
    date_to: Optional[datetime.datetime] = None,
    skip_errors: bool = False,
) -> Dict[datetime.datetime, T]:
    result = {}
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        try:
            suite = cls._load(filepath)
        except ValidationError:
            if skip_errors:
                continue
            raise
        if date_from is not None and suite.timestamp < date_from:
            continue
        if date_to is not None and suite.timestamp > date_to:
            continue
        result[suite.timestamp] = suite
    return result
