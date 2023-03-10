from typing import Optional

import pandas as pd
import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo


class TestSuiteWidget(Widget):
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
            type="test_suite",
            size=2,
            params={
                "tests": [
                    {
                        "title": "Test Case #1",
                        "description": "Some long description of test case",
                        "state": "success",
                    },
                    {
                        "title": "Test Case #2",
                        "description": "Some long description of test case",
                        "state": "warning",
                    },
                    {
                        "title": "Test Case #3",
                        "description": "Some long description of test case",
                        "state": "fail",
                        "details": {
                            "parts": [
                                {
                                    "title": "Graph",
                                    "id": "test_case_3",
                                },
                                {
                                    "title": "Graph 2",
                                    "id": "test_case_3_2",
                                },
                            ]
                        },
                    },
                ]
            },
            additionalGraphs=[
                AdditionalGraphInfo(
                    "test_case_3",
                    {
                        "data": fig_dict["data"],
                        "layout": fig_dict["layout"],
                    },
                ),
                AdditionalGraphInfo(
                    "test_case_3_2",
                    {
                        "data": fig_dict["data"],
                        "layout": fig_dict["layout"],
                    },
                ),
            ],
        )

    def analyzers(self):
        return []
