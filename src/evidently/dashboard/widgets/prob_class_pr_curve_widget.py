#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import (
    ProbClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class ProbClassPRCurveWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        color_options = self.options_provider.get(ColorOptions)
        results = ProbClassificationPerformanceAnalyzer.get_results(analyzers_results)
        utility_columns = results.columns.utility_columns

        if utility_columns.target is None or utility_columns.prediction is None:
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires 'target' and 'prediction' columns"
                )

            return None

        if self.dataset == "reference":
            metrics = results.reference_metrics

            if metrics is None:
                raise ValueError(
                    f"Widget [{self.title}] required 'reference' results from"
                    f" {ProbClassificationPerformanceAnalyzer.__name__} but no data found"
                )

        elif self.dataset == "current":
            metrics = results.current_metrics

        else:
            raise ValueError(
                f"Widget [{self.title}] required 'current' or 'reference' dataset value"
            )

        if metrics is None:
            return None

        # plot PR-curve
        if len(utility_columns.prediction) <= 2:
            if metrics.pr_curve is None:
                raise ValueError(f"Widget [{self.title}] got no pr_curve value")

            pr_curve = metrics.pr_curve
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=pr_curve["rcl"],
                    y=pr_curve["pr"],
                    mode="lines",
                    name="PR",
                    marker=dict(
                        size=6,
                        color=color_options.primary_color,
                    ),
                )
            )

            fig.update_layout(
                yaxis_title="Precision", xaxis_title="Recall", showlegend=True
            )

            fig_json = json.loads(fig.to_json())

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="big_graph",
                size=1 if current_data is not None else 2,
                params={"data": fig_json["data"], "layout": fig_json["layout"]},
            )
        else:
            if metrics.pr_curve is None:
                raise ValueError(f"Widget [{self.title}] got no pr_curve value")

            if not isinstance(metrics.pr_curve, dict):
                raise ValueError(
                    f"Widget [{self.title}] got incorrect type for pr_curve value"
                )

            graphs = []

            for label in utility_columns.prediction:
                pr_curve = metrics.pr_curve[label]
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=pr_curve["pr"],
                        y=pr_curve["rcl"],
                        mode="lines",
                        name="PR",
                        marker=dict(
                            size=6,
                            color=color_options.primary_color,
                        ),
                    )
                )

                fig.update_layout(
                    yaxis_title="Precision", xaxis_title="Recall", showlegend=True
                )

                fig_json = json.loads(fig.to_json())

                graphs.append(
                    {
                        "id": "tab_" + str(label),
                        "title": str(label),
                        "graph": {
                            "data": fig_json["data"],
                            "layout": fig_json["layout"],
                        },
                    }
                )

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="tabbed_graph",
                size=1 if current_data is not None else 2,
                params={"graphs": graphs},
            )
        return widget_info
