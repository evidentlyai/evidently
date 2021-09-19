#!/usr/bin/env python
# coding: utf-8

import dataclasses
import json
import os
import uuid
import base64
from dataclasses import asdict
import typing
from typing import List, Dict, Type

import pandas

import evidently
from evidently.analyzers.base_analyzer import Analyzer
from evidently.model.dashboard import DashboardInfo
from evidently.pipeline.pipeline import Pipeline
from evidently.tabs.base_tab import Tab
from evidently.utils import NumpyEncoder


@dataclasses.dataclass()
class TemplateParams:
    dashboard_id: str
    dashboard_info: DashboardInfo
    additional_graphs: Dict


def __dashboard_info_to_json(dashboard_info: DashboardInfo):
    return json.dumps(asdict(dashboard_info), cls=NumpyEncoder)


def inline_template(params: TemplateParams):
    return f"""
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"/>
<style>
.reset-this-parent {{
  all: initial;
}}
.reset-this-parent h5 {{
  all: initial;
  font: initial;
}}
</style>
<script>
    var {params.dashboard_id} = {__dashboard_info_to_json(params.dashboard_info)};
    var additional_graphs_{params.dashboard_id} = {json.dumps(params.additional_graphs)};
</script>
<script>
$(document).ready(function () {{
    requirejs(["evidently"], function(ev) {{
        drawDashboard({params.dashboard_id},
        new Map(Object.entries(additional_graphs_{params.dashboard_id})),
        "root_{params.dashboard_id}");
    }},
    function(err) {{
        $("#root_{params.dashboard_id}").innerHTML = "Failed to load";
    }})
}});
</script>
<div class="reset-this-parent" id="root_{params.dashboard_id}">Loading...</div>

"""


def file_html_template(params: TemplateParams):
    return f"""
<html>
<head>
<style>
/* fallback */
@font-face {{
  font-family: 'Material Icons';
  font-style: normal;
  font-weight: 400;
  src: url(data:font/ttf;base64,{__load_font()}) format('woff2');
}}

.material-icons {{
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}}
</style>
<script>
    var {params.dashboard_id} = {__dashboard_info_to_json(params.dashboard_info)};
    var additional_graphs_{params.dashboard_id} = {json.dumps(params.additional_graphs)};
</script>
</head>
<body>
<div id="root_{params.dashboard_id}">Loading...</div>
<script>{__load_js()}</script>
<script>
window.drawDashboard({params.dashboard_id},
    new Map(Object.entries(additional_graphs_{params.dashboard_id})),
    "root_{params.dashboard_id}"
);
</script>
</body>
"""


__BASE_PATH = evidently.__path__[0]
__STATIC_PATH = os.path.join(__BASE_PATH, "nbextension", "static")


def __load_js():
    return open(os.path.join(__STATIC_PATH, "index.js"), encoding='utf-8').read()


def __load_font():
    return base64.b64encode(
        open(os.path.join(__STATIC_PATH, "material-ui-icons.woff2"), 'rb').read()).decode()


class Dashboard(Pipeline):
    name: str
    _analyzers: List[Type[Analyzer]]

    def __init__(self, tabs: List[Type[Tab]]):
        super().__init__()
        self.tabs_data = [t() for t in tabs]
        self._analyzers = list({analyzer for tab in self.tabs_data for analyzer in tab.analyzers()})

    def get_analyzers(self):
        return self._analyzers

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: dict = None):
        self.execute(reference_data, current_data, column_mapping)
        for tab in self.tabs_data:
            tab.calculate(reference_data, current_data, column_mapping, self.analyzers_results)

    def __render(self, template: typing.Callable[[TemplateParams], str]):
        dashboard_id = "evidently_dashboard_" + str(uuid.uuid4()).replace("-", "")
        tab_widgets = [t.info() for t in self.tabs_data]

        dashboard_info = DashboardInfo(dashboard_id, [item for tab in tab_widgets for item in tab if item is not None])
        additional_graphs = {}
        for widget in [item for tab in tab_widgets for item in tab]:
            if widget is None:
                continue
            for graph in widget.additionalGraphs:
                additional_graphs[graph.id] = graph.params
        return template(TemplateParams(dashboard_id, dashboard_info, additional_graphs))

    def _json(self):
        dashboard_id = "evidently_dashboard_" + str(uuid.uuid4()).replace("-", "")
        tab_widgets = [t.info() for t in self.tabs_data]
        dashboard_info = DashboardInfo(dashboard_id, [item for tab in tab_widgets for item in tab if item is not None])
        return json.dumps(asdict(dashboard_info), cls=NumpyEncoder)

    def _save_to_json(self, filename):
        parent_dir = os.path.dirname(filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as out_file:
            out_file.write(self._json())

    def show(self):
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML
            return HTML(self.__render(inline_template))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def html(self):
        return self.__render(file_html_template)

    def save(self, filename):
        parent_dir = os.path.dirname(filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as out_file:
            out_file.write(self.html())
