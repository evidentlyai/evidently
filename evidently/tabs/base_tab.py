#!/usr/bin/env python
# coding: utf-8
from typing import List, Dict, Type, Optional, Tuple

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.stage import PipelineStage
from evidently.widgets.widget import Widget


VerboseLevel = int


class Verbose:
    ALWAYS = -1
    SHORT = 0
    FULL = 1


class Tab(PipelineStage):
    widgets: List[Tuple[Widget, VerboseLevel]]
    _widgets: List[Widget]

    def __init__(self,
                 verbose_level: VerboseLevel = None,
                 include_widgets: List[str] = None):
        super().__init__()
        if verbose_level is None:
            verbose_level = Verbose.FULL
        self._widgets = []
        self.details_level = verbose_level
        for widget in self.widgets:
            if include_widgets is not None and widget[0].title not in include_widgets:
                continue
            if include_widgets is None and widget[1] > verbose_level:
                continue
            self._widgets.append(widget[0])
            for analyzer in widget[0].analyzers():
                self.add_analyzer(analyzer)

    def calculate(self, reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: ColumnMapping,
                  analyzers_results: Dict[Type[Analyzer], object]):
        for widget in self._widgets:
            widget.options_provider = self.options_provider
            widget.calculate(reference_data, current_data, column_mapping, analyzers_results)

    def info(self) -> List[Optional[BaseWidgetInfo]]:
        return [w.get_info() for w in self._widgets]

    @classmethod
    def list_widgets(cls):
        return [widget[0].title for widget in cls.widgets]
