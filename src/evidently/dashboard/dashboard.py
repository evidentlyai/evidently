#!/usr/bin/env python
# coding: utf-8

import base64
import json
import os
import shutil
import uuid
from enum import Enum
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

import dataclasses
import pandas
from dataclasses import asdict

import evidently
from evidently.dashboard.tabs.base_tab import Tab
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import PlotlyGraphInfo
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.pipeline import Pipeline
from evidently.utils import NumpyEncoder


@dataclasses.dataclass()
class TemplateParams:
    dashboard_id: str
    dashboard_info: DashboardInfo
    additional_graphs: Dict
    embed_font: bool = True
    embed_lib: bool = True
    embed_data: bool = True
    font_file: Optional[str] = None
    include_js_files: List[str] = dataclasses.field(default_factory=list)


def _dashboard_info_to_json(dashboard_info: DashboardInfo):
    asdict_result = asdict(dashboard_info)
    for widget in asdict_result["widgets"]:
        widget.pop("additionalGraphs", None)
    return json.dumps(asdict_result, cls=NumpyEncoder)


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

svg {{
  height: intrinsic !important;
}}
</style>
<script>
    var {params.dashboard_id} = {_dashboard_info_to_json(params.dashboard_info)};
    var additional_graphs_{params.dashboard_id} = {json.dumps(params.additional_graphs, cls=NumpyEncoder)};
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
    lib_block = (
        f"""<script>{__load_js()}</script>"""
        if params.embed_lib
        else "<!-- no embedded lib -->"
    )
    data_block = (
        f"""<script>
    var {params.dashboard_id} = {_dashboard_info_to_json(params.dashboard_info)};
    var additional_graphs_{params.dashboard_id} = {json.dumps(params.additional_graphs, cls=NumpyEncoder)};
</script>"""
        if params.embed_data
        else "<!-- no embedded data -->"
    )
    js_files_block = "\n".join(
        [f'<script src="{file}"></script>' for file in params.include_js_files]
    )
    return f"""
<html>
<head>
<meta charset="utf-8">
<style>
/* fallback */
@font-face {{
  font-family: 'Material Icons';
  font-style: normal;
  font-weight: 400;
  src: {f"url(data:font/ttf;base64,{__load_font()}) format('woff2');" if params.embed_font else
    f"url({params.font_file});"}
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
{data_block}
</head>
<body>
<div id="root_{params.dashboard_id}">Loading...</div>
{lib_block}
{js_files_block}
<script>
window.drawDashboard({params.dashboard_id},
    new Map(Object.entries(additional_graphs_{params.dashboard_id})),
    "root_{params.dashboard_id}"
);
</script>
</body>
"""


__BASE_PATH = evidently.__path__[0]  # type: ignore
_STATIC_PATH = os.path.join(__BASE_PATH, "nbextension", "static")


class SaveMode(Enum):
    SINGLE_FILE = "singlefile"
    FOLDER = "folder"
    SYMLINK_FOLDER = "symlink_folder"


SaveModeMap = {v.value: v for v in SaveMode}


def __load_js():
    return open(os.path.join(_STATIC_PATH, "index.js"), encoding="utf-8").read()


def __load_font():
    return base64.b64encode(
        open(os.path.join(_STATIC_PATH, "material-ui-icons.woff2"), "rb").read()
    ).decode()


class Dashboard(Pipeline):
    name: str
    stages: Sequence[Tab]

    def __init__(self, tabs: Sequence[Tab], options: Optional[List[object]] = None):
        super().__init__(tabs, options if options is not None else [])

    def calculate(
        self,
        reference_data: pandas.DataFrame,
        current_data: Optional[pandas.DataFrame] = None,
        column_mapping: Optional[ColumnMapping] = None,
    ):
        column_mapping = column_mapping or ColumnMapping()
        self.execute(reference_data, current_data, column_mapping)

    def __dashboard_data(self) -> Tuple[str, DashboardInfo, Dict]:
        dashboard_id = "evidently_dashboard_" + str(uuid.uuid4()).replace("-", "")
        tab_widgets = [t.info() for t in self.stages]
        dashboard_info = DashboardInfo(
            dashboard_id,
            [item for tab in tab_widgets for item in tab if item is not None],
        )
        additional_graphs = {}
        for widget in [item for tab in tab_widgets for item in tab]:
            if widget is None:
                continue
            for graph in widget.get_additional_graphs():
                if isinstance(graph, AdditionalGraphInfo):
                    additional_graphs[graph.id] = graph.params
                elif isinstance(graph, (BaseWidgetInfo, PlotlyGraphInfo)):
                    additional_graphs[graph.id] = graph
        return dashboard_id, dashboard_info, additional_graphs

    def __render(
        self,
        dashboard_id,
        dashboard_info,
        additional_graphs,
        template: Callable[[TemplateParams], str],
    ):
        return template(TemplateParams(dashboard_id, dashboard_info, additional_graphs))

    def __no_lib_render(
        self,
        dashboard_id,
        dashboard_info,
        additional_graphs,
        font_file: str,
        include_js_files: List[str],
        template: Callable[[TemplateParams], str],
    ):
        return template(
            TemplateParams(
                dashboard_id,
                dashboard_info,
                additional_graphs,
                embed_lib=False,
                embed_data=False,
                embed_font=False,
                font_file=font_file,
                include_js_files=include_js_files,
            )
        )

    def _json(self):
        dashboard_id = "evidently_dashboard_" + str(uuid.uuid4()).replace("-", "")
        tab_widgets = [t.info() for t in self.stages]
        dashboard_info = DashboardInfo(
            dashboard_id,
            [item for tab in tab_widgets for item in tab if item is not None],
        )
        return json.dumps(asdict(dashboard_info), cls=NumpyEncoder)

    def _save_to_json(self, filename):
        parent_dir = os.path.dirname(filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as out_file:
            out_file.write(self._json())

    def show(self, mode="auto"):
        dashboard_id, dashboard_info, additional_graphs = self.__dashboard_data()
        # pylint: disable=import-outside-toplevel
        render_mode = mode
        try:
            from IPython import get_ipython
            from IPython.display import HTML

            if mode == "auto":
                if type(get_ipython()).__module__.startswith("google.colab"):
                    render_mode = "inline"
                else:
                    render_mode = "nbextension"
            if render_mode == "inline":
                return HTML(
                    self.__render(
                        dashboard_id,
                        dashboard_info,
                        additional_graphs,
                        file_html_template,
                    )
                )
            if render_mode == "nbextension":
                return HTML(
                    self.__render(
                        dashboard_id, dashboard_info, additional_graphs, inline_template
                    )
                )
            raise ValueError(f"Unexpected value {mode}/{render_mode} for mode")
        except ImportError as err:
            raise Exception(
                "Cannot import HTML from IPython.display, no way to show html"
            ) from err

    def html(self):
        dashboard_id, dashboard_info, additional_graphs = self.__dashboard_data()
        return self.__render(
            dashboard_id, dashboard_info, additional_graphs, file_html_template
        )

    def save(self, filename: str, mode: SaveMode = SaveMode.SINGLE_FILE):
        if isinstance(mode, str):
            _mode = SaveModeMap.get(mode)
            if _mode is None:
                raise ValueError(
                    f"Unexpected save mode {mode}. Expected [{','.join(SaveModeMap.keys())}]"
                )
            mode = _mode
        if mode == SaveMode.SINGLE_FILE:
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self.html())
        if mode in [SaveMode.FOLDER, SaveMode.SYMLINK_FOLDER]:
            font_file, lib_file = save_lib_files(filename, mode)
            dashboard_id, dashboard_info, additional_graphs = self.__dashboard_data()
            data_file = save_data_file(
                filename, mode, dashboard_id, dashboard_info, additional_graphs
            )
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(
                    self.__no_lib_render(
                        dashboard_id,
                        dashboard_info,
                        additional_graphs,
                        font_file,
                        [data_file, lib_file],
                        file_html_template,
                    )
                )


def save_lib_files(filename: str, mode: SaveMode):
    if mode == SaveMode.SINGLE_FILE:
        return None, None
    parent_dir = os.path.dirname(filename)
    if not os.path.exists(os.path.join(parent_dir, "js")):
        os.makedirs(os.path.join(parent_dir, "js"), exist_ok=True)
    font_file = os.path.join(parent_dir, "js", "material-ui-icons.woff2")
    lib_file = os.path.join(parent_dir, "js", f"evidently.{evidently.__version__}.js")

    if mode == SaveMode.SYMLINK_FOLDER:
        if os.path.exists(font_file):
            os.remove(font_file)
        os.symlink(os.path.join(_STATIC_PATH, "material-ui-icons.woff2"), font_file)
        if os.path.exists(lib_file):
            os.remove(lib_file)
        os.symlink(os.path.join(_STATIC_PATH, "index.js"), lib_file)
    else:
        shutil.copy(os.path.join(_STATIC_PATH, "material-ui-icons.woff2"), font_file)
        shutil.copy(os.path.join(_STATIC_PATH, "index.js"), lib_file)
    return font_file, lib_file


def save_data_file(
    filename: str,
    mode: SaveMode,
    dashboard_id,
    dashboard_info: DashboardInfo,
    additional_graphs: Dict,
):
    if mode == SaveMode.SINGLE_FILE:
        return None
    parent_dir = os.path.dirname(filename)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    base_name = os.path.basename(filename)
    data_file = os.path.join(parent_dir, "js", f"{base_name}.data.js")
    with open(data_file, "w", encoding="utf-8") as out_file:
        out_file.write(
            f"""
    var {dashboard_id} = {_dashboard_info_to_json(dashboard_info)};
    var additional_graphs_{dashboard_id} = {json.dumps(additional_graphs, cls=NumpyEncoder)};"""
        )
    return data_file
