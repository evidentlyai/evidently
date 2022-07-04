import dataclasses
import json
import time
import uuid
from collections import Counter
from typing import List
from typing import Optional
from typing import Union
from typing import Iterator

import pandas as pd

import evidently
from evidently import ColumnMapping
from evidently.analyzers.utils import process_columns
from evidently.analyzers.utils import DatasetColumns
from evidently.dashboard.dashboard import TemplateParams, SaveMode, SaveModeMap, save_lib_files, save_data_file
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.utils import NumpyEncoder
from evidently.v2.metrics.base_metric import InputData, Metric
from evidently.v2.renderers.notebook_utils import determine_template
from evidently.v2.suite.base_suite import Suite, find_test_renderer
from evidently.v2.tests.base_test import Test, TestResult


def _discover_dependencies(test: Test) -> Iterator[Union[Metric, Test]]:
    for _, field in test.__dict__.items():
        if issubclass(type(field), (Metric, Test)):
            yield field


class TestSuite:
    _inner_suite: Suite
    _columns_info: DatasetColumns

    def __init__(self, tests: Optional[List[Test]]):
        self._inner_suite = Suite()
        for test in tests:
            for dependency in _discover_dependencies(test):
                if issubclass(type(dependency), Metric):
                    self._inner_suite.add_metrics(dependency)
                if issubclass(type(dependency), Test):
                    self._inner_suite.add_tests(dependency)
        self._inner_suite.add_tests(*tests)

    def __bool__(self):
        return all(test_result.is_passed() for _, test_result in self._inner_suite.context.test_results.items())

    def run(
            self, *, reference_data: Optional[pd.DataFrame], current_data: pd.DataFrame,
            column_mapping: Optional[ColumnMapping] = None
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        self._columns_info = process_columns(current_data, column_mapping)
        self._inner_suite.verify()
        self._inner_suite.run_calculate(InputData(reference_data, current_data, column_mapping))
        self._inner_suite.run_checks()

    def _repr_html_(self):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id,
            dashboard_info=dashboard_info,
            additional_graphs=graphs)
        return self._render(determine_template("inline"), template_params)

    def show(self, mode='auto'):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id,
            dashboard_info=dashboard_info,
            additional_graphs=graphs)
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML
            return HTML(self._render(determine_template(mode), template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def save_html(self, filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        if isinstance(mode, str):
            _mode = SaveModeMap.get(mode)
            if _mode is None:
                raise ValueError(f"Unexpected save mode {mode}. Expected [{','.join(SaveModeMap.keys())}]")
            mode = _mode
        if mode == SaveMode.SINGLE_FILE:
            template_params = TemplateParams(
                dashboard_id=dashboard_id,
                dashboard_info=dashboard_info,
                additional_graphs=graphs,
            )
            with open(filename, 'w', encoding='utf-8') as out_file:
                out_file.write(self._render(determine_template("inline"), template_params))
        else:
            font_file, lib_file = save_lib_files(filename, mode)
            data_file = save_data_file(filename,
                                       mode,
                                       dashboard_id,
                                       dashboard_info,
                                       graphs)
            template_params = TemplateParams(
                dashboard_id=dashboard_id,
                dashboard_info=dashboard_info,
                additional_graphs=graphs,
                embed_lib=False,
                embed_data=False,
                embed_font=False,
                font_file=font_file,
                include_js_files=[lib_file, data_file],
            )
            with open(filename, 'w', encoding='utf-8') as out_file:
                out_file.write(self._render(determine_template("inline"), template_params))

    def as_dict(self) -> dict:
        test_results = []
        counter = Counter(test_result.status for test_result in self._inner_suite.context.test_results.values())

        for test in self._inner_suite.context.test_results:
            renderer = find_test_renderer(type(test), self._inner_suite.context.renderers)
            test_results.append(renderer.render_json(test))

        return {
            "version": evidently.__version__,
            "timestamp": time.time(),
            "tests": test_results,
            "summary": {
                "all_passed": bool(self),
                "total_tests": len(self._inner_suite.context.test_results),
                "success_tests": len(self._inner_suite.context.test_results),
                "failed_tests": len(self._inner_suite.context.test_results),
                "by_status": counter,
            },
            "columns_info": dataclasses.asdict(self._columns_info),
        }

    def json(self) -> str:
        return json.dumps(self.as_dict(), cls=NumpyEncoder)

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as out_file:
            json.dump(self.as_dict(), out_file, cls=NumpyEncoder)

    def _render(self, temple_func, template_params: TemplateParams):
        return temple_func(params=template_params)

    def _build_dashboard_info(self):
        test_results = []
        total_tests = len(self._inner_suite.context.test_results)
        by_status = {}
        for test, test_result in self._inner_suite.context.test_results.items():
            renderer = find_test_renderer(type(test), self._inner_suite.context.renderers)
            by_status[test_result.status] = by_status.get(test_result.status, 0) + 1
            test_results.append(renderer.render_html(test))
        summary_widget = BaseWidgetInfo(
            title="",
            size=2,
            type="counter",
            params={
                "counters": [{
                    "value": f"{total_tests}",
                    "label": "Total Tests"
                }] + [
                    {
                        "value": f"{by_status.get(status, 0)}",
                        "label": f"{status.title()} Tests"
                    } for status in [TestResult.SUCCESS, TestResult.WARNING, TestResult.FAIL, TestResult.ERROR]
                ]
            },

        )
        test_suite_widget = BaseWidgetInfo(
            title="",
            type="test_suite",
            size=2,
            params={
                "tests": [dict(title=test_info.name,
                               description=test_info.description,
                               state=test_info.status.lower(),
                               details=dict(
                                   parts=[dict(id=f"{test_info.name}_{item.id}", title=item.title, type="widget")
                                          for item in test_info.details]
                               )) for test_info in test_results]
            },
            additionalGraphs=[]
        )
        return "evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""), \
               DashboardInfo("Test Suite", widgets=[summary_widget, test_suite_widget]), \
               {f"{info.name}_{item.id}": dataclasses.asdict(item.info)
                for info in test_results for item in info.details}
