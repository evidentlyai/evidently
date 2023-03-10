#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd
from plotly import graph_objs as go

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import Insight


class ExpandableListWidget(Widget):
    def analyzers(self):
        return []

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3, 4, 5], y=[0.1, 0.2, 0.3, 0.4, 0.5]))

        fig_dict = fig.to_dict()

        return BaseWidgetInfo(
            title="",
            size=2,
            type="list",
            widgets=[
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "Header",
                        "description": "optional description",
                        "metricsValuesHeaders": ["reference", "current"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6]},
                            {"label": "average", "values": [0.3, 0.6]},
                            {"label": "something", "values": [0.3, 0.6]},
                            {"label": "some string", "values": ["absc", "gar"]},
                        ],
                        "graph": {
                            "data": fig_dict["data"],
                            "layout": fig_dict["layout"],
                        },
                        "details": {
                            "parts": [
                                {"title": "First Tab", "id": "first_tab"},
                                {"title": "Second Tab", "id": "second_tab"},
                            ],
                            "insights": [],
                        },
                    },
                    additionalGraphs=[
                        AdditionalGraphInfo(
                            "first_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                        AdditionalGraphInfo(
                            "second_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                    ],
                ),
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "Without Graph",
                        "description": "optional description",
                        "metricsValuesHeaders": ["reference", "current"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6]},
                            {"label": "average", "values": [0.3, 0.6]},
                            {"label": "something", "values": [0.3, 0.6]},
                            {"label": "some string", "values": ["absc", "gar"]},
                        ],
                        "details": {
                            "parts": [
                                {"title": "First Tab", "id": "first_tab"},
                                {"title": "Second Tab", "id": "second_tab"},
                            ],
                            "insights": [],
                        },
                    },
                    additionalGraphs=[
                        AdditionalGraphInfo(
                            "first_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                        AdditionalGraphInfo(
                            "second_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                    ],
                ),
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "Without details",
                        "description": "optional description",
                        "metricsValuesHeaders": ["reference", "current"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6]},
                            {"label": "average", "values": [0.3, 0.6]},
                            {"label": "something", "values": [0.3, 0.6]},
                            {"label": "some string", "values": ["absc", "gar"]},
                        ],
                        "graph": {
                            "data": fig_dict["data"],
                            "layout": fig_dict["layout"],
                        },
                    },
                ),
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "Without graph and details",
                        "description": "optional description",
                        "metricsValuesHeaders": ["reference", "current"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6]},
                            {"label": "average", "values": [0.3, 0.6]},
                            {"label": "something", "values": [0.3, 0.6]},
                            {"label": "some string", "values": ["absc", "gar"]},
                        ],
                    },
                ),
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "Header",
                        "description": "optional description",
                        "metricsValuesHeaders": ["reference", "current"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6]},
                            {"label": "average", "values": [0.3, 0.6]},
                            {"label": "something", "values": [0.3, 0.6]},
                            {"label": "some string", "values": ["absc", "gar"]},
                        ],
                        "graph": {
                            "data": fig_dict["data"],
                            "layout": fig_dict["layout"],
                        },
                        "details": {
                            "parts": [
                                {"title": "First Tab", "id": "first_tab"},
                                {"title": "Second Tab", "id": "second_tab"},
                            ],
                            "insights": [],
                        },
                    },
                    additionalGraphs=[
                        AdditionalGraphInfo(
                            "first_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                        AdditionalGraphInfo(
                            "second_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                    ],
                ),
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "More values",
                        "description": "optional description",
                        "metricsValuesHeaders": ["first", "second", "third"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6, 0.9]},
                            {"label": "average", "values": [0.3, 0.6, 0.7]},
                            {"label": "something", "values": [0.3, 0.6, 0.9]},
                            {"label": "some string", "values": ["absc", "gar", "par"]},
                        ],
                        "graph": {
                            "data": fig_dict["data"],
                            "layout": fig_dict["layout"],
                        },
                        "details": {
                            "parts": [
                                {"title": "First Tab", "id": "first_tab"},
                                {"title": "Second Tab", "id": "second_tab"},
                            ],
                        },
                    },
                    additionalGraphs=[
                        AdditionalGraphInfo(
                            "first_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                        AdditionalGraphInfo(
                            "second_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                    ],
                ),
                BaseWidgetInfo(
                    type="rich_data",
                    title="",
                    size=2,
                    params={
                        "header": "With insight",
                        "description": "optional description",
                        "metricsValuesHeaders": ["reference", "current"],
                        "metrics": [
                            {"label": "f1", "values": [0.3, 0.6]},
                            {"label": "average", "values": [0.3, 0.6]},
                            {"label": "something", "values": [0.3, 0.6]},
                            {"label": "some string", "values": ["absc", "gar"]},
                        ],
                        "graph": {
                            "data": fig_dict["data"],
                            "layout": fig_dict["layout"],
                        },
                        "details": {
                            "parts": [
                                {"title": "First Tab", "id": "first_tab"},
                                {"title": "Second Tab", "id": "second_tab"},
                            ],
                            "insights": [
                                Insight(
                                    "Some notification",
                                    "warning",
                                    "additional text for insight",
                                )
                            ],
                        },
                    },
                    additionalGraphs=[
                        AdditionalGraphInfo(
                            "first_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                        AdditionalGraphInfo(
                            "second_tab",
                            {
                                "data": fig_dict["data"],
                                "layout": fig_dict["layout"],
                            },
                        ),
                    ],
                ),
            ],
            pageSize=2,
        )
