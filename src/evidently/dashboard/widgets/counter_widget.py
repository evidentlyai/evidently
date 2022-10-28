#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class CounterWidget(Widget):
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
            type="counter",
            title=self.title,
            size=1,
            params={
                "counters": [
                    {"value": "7 out of 12 features", "label": "Data Drift Detected"}
                ]
            },
        )
