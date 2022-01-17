#!/usr/bin/env python
# coding: utf-8

import dataclasses
import json
import os
import uuid
import base64
from dataclasses import asdict
from typing import List, Callable, Dict, Optional, Sequence

import pandas

import evidently
from evidently.model.dashboard import DashboardInfo
from evidently.pipeline.pipeline import Pipeline
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.tabs.base_tab import Tab
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
function domReady(fn) {{
  // If we're early to the party
  document.addEventListener("DOMContentLoaded", fn);
  // If late; I mean on time.
  if (document.readyState === "interactive" || document.readyState === "complete" ) {{
    fn();
  }}
}}

domReady(function () {{
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


__BASE_PATH = evidently.__path__[0]  # type: ignore
__STATIC_PATH = os.path.join(__BASE_PATH, "nbextension", "static")


def __load_js():
    return open(os.path.join(__STATIC_PATH, "index.js"), encoding='utf-8').read()


def __load_font():
    return base64.b64encode(
        open(os.path.join(__STATIC_PATH, "material-ui-icons.woff2"), 'rb').read()).decode()


class Dashboard(Pipeline):
    name: str
    stages: Sequence[Tab]

    def __init__(self, tabs: Sequence[Tab], options: Optional[List[object]] = None):
        super().__init__(tabs, options if options is not None else [])

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: Optional[pandas.DataFrame],
                  column_mapping: Optional[ColumnMapping] = None):
        column_mapping = column_mapping or ColumnMapping()
        self.execute(reference_data, current_data, column_mapping)

    def __render(self, template: Callable[[TemplateParams], str]):
        dashboard_id = "evidently_dashboard_" + str(uuid.uuid4()).replace("-", "")
        tab_widgets = [t.info() for t in self.stages]

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
        tab_widgets = [t.info() for t in self.stages]
        dashboard_info = DashboardInfo(dashboard_id, [item for tab in tab_widgets for item in tab if item is not None])
        return json.dumps(asdict(dashboard_info), cls=NumpyEncoder)

    def _save_to_json(self, filename):
        parent_dir = os.path.dirname(filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as out_file:
            out_file.write(self._json())

    def show(self, mode='auto'):
        # pylint: disable=import-outside-toplevel
        render_mode = mode
        try:
            from IPython.display import HTML
            from IPython import get_ipython
            if mode == 'auto':
                if type(get_ipython()).__module__.startswith("google.colab"):
                    render_mode = 'inline'
                else:
                    render_mode = 'nbextension'
            if render_mode == 'inline':
                return HTML(self.__render(file_html_template))
            if render_mode == 'nbextension':
                return HTML(self.__render(inline_template))
            raise ValueError(f"Unexpected value {mode}/{render_mode} for mode")
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
