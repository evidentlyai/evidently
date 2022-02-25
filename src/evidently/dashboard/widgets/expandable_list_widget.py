#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd
from plotly import graph_objs as go

from evidently import ColumnMapping
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget


class ExpandableListWidget(Widget):
    def analyzers(self):
        return []

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3, 4, 5], y=[0.1, 0.2, 0.3, 0.4, 0.5]))

        fig_dict = fig.to_dict()

        wi = BaseWidgetInfo(
            type="expandable_list",
            title="",
            size=2,
            params={
                "header": "Feature",
                "description": "number",
                "metricsValuesHeaders": ["reference", "current"],
                "metrics": [
                    {"label": "f1", "values": [0.3, 0.6]},
                    {"label": "average", "values": [0.3, 0.6]},
                    {"label": "something", "values": [0.3, 0.6]},
                    {"label": "some string", "values": ["absc", "gar"]},
                ],
                "graph": {
                    "data": fig_dict['data'],
                    "layout": fig_dict['layout']
                },
                "details": {
                    "parts": [{
                        "title": "First Tab",
                        "id": "first_tab"
                    }, {
                        "title": "Second Tab",
                        "id": "second_tab"
                    }],
                    "insights": []
                }
            },
            additionalGraphs=[
                AdditionalGraphInfo("first_tab", {
                    "data": fig_dict['data'],
                    "layout": fig_dict['layout'],
                }),
                AdditionalGraphInfo("second_tab", {
                    "data": fig_dict['data'],
                    "layout": fig_dict['layout'],
                })
            ]
        )
        return BaseWidgetInfo(
            title="",
            size=2,
            type="group",
            widgets=[wi, wi]
        )
