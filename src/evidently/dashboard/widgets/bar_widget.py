#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class BarWidget(Widget):
    def analyzers(self):
        return []

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        return BaseWidgetInfo(
            type="big_graph",
            title=self.title,
            size=2,
            params={
                "data": [
                    {
                        "marker": {"color": "#ed0400"},
                        "type": "bar",
                        "x": [1, 2, 3, 4, 5],
                        "y": [2, 5, 3, 1, 2],
                    }
                ],
                "layout": {
                    "xaxis": {"title": {"text": "Features"}},
                    "yaxis": {"showticklabels": True, "title": {"text": "Correlation"}},
                },
            },
            alerts=[],
            insights=[],
            details="",
            alertsPosition="row",
            additionalGraphs=[],
        )
