import uuid
from typing import List, Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.dashboard import TemplateParams
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics.base_metric import InputData, Metric
from evidently.v2.renderers.notebook_utils import determine_template
from evidently.v2.suite.base_suite import Suite, find_test_renderer
from evidently.v2.tests.base_test import Test


class TestSuite:
    _inner_suite: Suite

    def __init__(self, tests: Optional[List[Test]]):
        self._inner_suite = Suite()
        for test in tests:
            for dependency in test.dependencies():
                if issubclass(type(dependency), Metric):
                    self._inner_suite.add_metrics(dependency)
                if issubclass(type(dependency), Test):
                    self._inner_suite.add_tests(dependency)
        self._inner_suite.add_tests(*tests)

    def run(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping: ColumnMapping):
        self._inner_suite.verify()
        self._inner_suite.run_calculate(InputData(reference_data, current_data, column_mapping))
        self._inner_suite.run_checks()

    def _repr_html_(self):
        return self._render(determine_template("inline"))

    def show(self, mode='auto'):
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML
            return HTML(self._render(determine_template(mode)))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def _render(self, temple_func):
        test_results = []
        for _, test_result in self._inner_suite.context.test_results.items():
            renderer = find_test_renderer(test_result, self._inner_suite.context.renderers)
            test_results.append(renderer.render(test_result))
        test_suite_widget = BaseWidgetInfo(
            title="",
            type="test_suite",
            size=2,
            params={
                "tests": [dict(title=test_info.name,
                               description=test_info.description,
                               state=test_info.status.lower(),
                               details=dict(
                                   parts=[dict(id=item.id, title=item.title) for item in test_info.details]
                               )) for test_info in test_results]
            },
            additionalGraphs=[item.info for info in test_results for item in info.details]
        )
        return temple_func(params=TemplateParams(
            dashboard_id="evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""),
            dashboard_info=DashboardInfo("Test Suite", widgets=[test_suite_widget]),
            additional_graphs={}))
