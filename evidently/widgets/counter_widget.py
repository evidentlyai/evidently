#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas

from evidently import ColumnMapping
from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget


class CounterWidget(Widget):
    def analyzers(self):
        return []

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        return BaseWidgetInfo(
            type="counter",
            title=self.title,
            size=2,
            params={
                "counters": [
                    {
                        "value": "7 out of 12 features",
                        "label": "Data Drift Detected"
                    }
                ]
            },
        )
