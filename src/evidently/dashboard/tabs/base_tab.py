#!/usr/bin/env python
# coding: utf-8
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.stage import PipelineStage

VerboseLevel = int


class Verbose:
    ALWAYS = -1
    SHORT = 0
    FULL = 1


class Tab(PipelineStage):
    widgets: List[Tuple[Widget, VerboseLevel]]
    _widgets: List[Widget]
    _widget_results: List[Optional[BaseWidgetInfo]]

    def __init__(
        self,
        verbose_level: VerboseLevel = None,
        include_widgets: List[Union[str, Widget]] = None,
    ):
        super().__init__()
        if verbose_level is None:
            verbose_level = Verbose.FULL
        self._widgets = []
        self._widget_results = []
        self.details_level = verbose_level
        predefined_widgets = {widget[0].title: widget[0] for widget in self.widgets}

        if include_widgets is not None:
            for widget in include_widgets:
                if isinstance(widget, str):
                    self._widgets.append(predefined_widgets[widget])
                elif isinstance(widget, Widget):
                    self._widgets.append(widget)
                else:
                    raise ValueError(f"Unexpected value: {widget}")
        else:
            for _widget in self.widgets:
                if _widget[1] > verbose_level:
                    continue
                self._widgets.append(_widget[0])
        for _widget_instance in self._widgets:
            for analyzer in _widget_instance.analyzers():
                self.add_analyzer(analyzer)

    def calculate(
        self,
        reference_data: pandas.DataFrame,
        current_data: pandas.DataFrame,
        column_mapping: ColumnMapping,
        analyzers_results: Dict[Type[Analyzer], object],
    ):
        self._widget_results.clear()
        for widget in self._widgets:
            widget.options_provider = self.options_provider
            self._widget_results.append(
                widget.calculate(
                    reference_data, current_data, column_mapping, analyzers_results
                )
            )

    def info(self) -> List[Optional[BaseWidgetInfo]]:
        return self._widget_results

    @classmethod
    def list_widgets(cls):
        return [widget[0].title for widget in cls.widgets]
