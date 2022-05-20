import json
from dataclasses import dataclass
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

import pandas as pd

from evidently.suites.metrics.base_metrics import BaseCalculation
from evidently.suites.metrics.base_metrics import BaseTest
from evidently.suites.metrics.base_metrics import OneSourceDatasetMetric


@dataclass
class BaseSuit:
    _calculated_metrics = Dict[str, BaseCalculation]
    _calculated_tests = List[BaseTest]
    metrics: ClassVar[List[Type[BaseCalculation]]]
    tests: Optional[List[BaseTest]] = None

    def add_tests(self, *args):
        if self.tests is None:
            self.tests = []

        self.tests.extend(args)

    def calculate(self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame] = None):
        self._calculated_metrics = {}

        for metric_class in self.metrics:
            metric = metric_class()

            if issubclass(metric_class, OneSourceDatasetMetric):
                metric.dataset = reference_data

            metric.result = metric.calculate()
            self._calculated_metrics[metric.name] = metric

        self._calculated_tests = []

        for test in self.tests:
            if test.required_analyzer:
                test.calculated_analyzer = self._calculated_metrics[test.required_analyzer.name]

            test.result = test.calculate()
            self._calculated_tests.append(test)

    def make_json_report(self, verbose: bool = False):
        result = {}

        if self._calculated_metrics:
            result["metrics"] = {}

            for metric in self._calculated_metrics.values():
                result["metrics"][metric.name] = metric.get_result_as_dict(verbose=verbose)

        if self._calculated_tests:
            result["tests"] = {}

            for test in self._calculated_tests:
                result["tests"][test.id] = test.get_result_as_dict(verbose=verbose)

        return json.dumps(result)
