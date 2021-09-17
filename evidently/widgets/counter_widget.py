#!/usr/bin/env python
# coding: utf-8

from typing import Dict

import pandas

from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget


class CounterWidget(Widget):
    def analyzers(self):
        return []

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: Dict,
                  analyzers_results):
        self.wi = BaseWidgetInfo(
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
            alerts=[],
            insights=[],
            details="",
            alertsPosition="row",
            alertStats=AlertStats(),
            additionalGraphs=[],
        )
