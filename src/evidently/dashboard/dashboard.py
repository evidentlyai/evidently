#!/usr/bin/env python
# coding: utf-8

import json
import os
import uuid
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

import pandas
from dataclasses import asdict

from evidently.dashboard.tabs.base_tab import Tab
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import PlotlyGraphInfo
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.pipeline import Pipeline
from evidently.utils import NumpyEncoder
from evidently.utils.dashboard import SaveMode
from evidently.utils.dashboard import SaveModeMap
from evidently.utils.dashboard import TemplateParams
from evidently.utils.dashboard import file_html_template
from evidently.utils.dashboard import inline_template
from evidently.utils.dashboard import save_data_file
from evidently.utils.dashboard import save_lib_files


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
        dashboard_info = DashboardInfo(dashboard_id, [item for tab in tab_widgets for item in tab if item is not None])
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

    def __render(self, dashboard_id, dashboard_info, additional_graphs, template: Callable[[TemplateParams], str]):
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
        dashboard_info = DashboardInfo(dashboard_id, [item for tab in tab_widgets for item in tab if item is not None])
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
                return HTML(self.__render(dashboard_id, dashboard_info, additional_graphs, file_html_template))
            if render_mode == "nbextension":
                return HTML(self.__render(dashboard_id, dashboard_info, additional_graphs, inline_template))
            raise ValueError(f"Unexpected value {mode}/{render_mode} for mode")
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def html(self):
        dashboard_id, dashboard_info, additional_graphs = self.__dashboard_data()
        return self.__render(dashboard_id, dashboard_info, additional_graphs, file_html_template)

    def save(self, filename: str, mode: SaveMode = SaveMode.SINGLE_FILE):
        if isinstance(mode, str):
            _mode = SaveModeMap.get(mode)
            if _mode is None:
                raise ValueError(f"Unexpected save mode {mode}. Expected [{','.join(SaveModeMap.keys())}]")
            mode = _mode
        if mode == SaveMode.SINGLE_FILE:
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self.html())
        if mode in [SaveMode.FOLDER, SaveMode.SYMLINK_FOLDER]:
            font_file, lib_file = save_lib_files(filename, mode)
            dashboard_id, dashboard_info, additional_graphs = self.__dashboard_data()
            data_file = save_data_file(filename, mode, dashboard_id, dashboard_info, additional_graphs)
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
