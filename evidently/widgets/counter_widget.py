#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Optional

import pandas

from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget


class CounterWidget(Widget):
    wi: Optional[BaseWidgetInfo]

    def __init__(self, title: str):
        super().__init__()
        self.wi = None
        self.title = title

    def calculate(self, reference_data: pandas.DataFrame, production_data: pandas.DataFrame, _: Dict):
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

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("no widget info provided")
