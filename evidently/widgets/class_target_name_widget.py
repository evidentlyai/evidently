#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget
from evidently.analyzers.utils import process_columns


class ClassTargetNameWidget(Widget):
    def analyzers(self):
        return []

    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping, analyzers_results):
        columns = process_columns(reference_data, column_mapping)

        if columns.utility_columns.target is not None and columns.utility_columns.prediction is not None:

            self.wi = BaseWidgetInfo(
                title=self.title,
                type="counter",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=2,
                params={
                    "counters": [
                      {
                        "value": "",
                        "label": "Classification Model Performance Report. Target:'" + columns.utility_columns.target +"'"
                      }
                    ]
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None
