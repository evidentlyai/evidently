#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd

import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer

from evidently.model.widget import BaseWidgetInfo
from evidently.dashboard.widgets.widget import Widget, RED


class ProbClassPRCurveWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[ProbClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")
            return None
        if self.dataset not in results['metrics'].keys():
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] required 'reference' results from"
                                 f" {ProbClassificationPerformanceAnalyzer.__name__} but no data found")
            return None

        widget_info = None
        # plot PR-curve
        if len(results['utility_columns']['prediction']) <= 2:

            pr_curve = results['metrics'][self.dataset]['pr_curve']

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=pr_curve['pr'],
                y=pr_curve['rcl'],
                mode='lines',
                name='PR',
                marker=dict(
                    size=6,
                    color=RED,
                )
            ))

            fig.update_layout(
                yaxis_title="Precision",
                xaxis_title="Recall",
                showlegend=True
            )

            fig_json = json.loads(fig.to_json())

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="big_graph",
                size=1 if current_data is not None else 2,
                params={
                    "data": fig_json['data'],
                    "layout": fig_json['layout']
                },
            )
        else:

            graphs = []

            for label in results['utility_columns']['prediction']:
                pr_curve = results['metrics'][self.dataset]['pr_curve'][label]

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=pr_curve['pr'],
                    y=pr_curve['rcl'],
                    mode='lines',
                    name='PR',
                    marker=dict(
                        size=6,
                        color=RED,
                    )
                ))

                fig.update_layout(
                    yaxis_title="Precision",
                    xaxis_title="Recall",
                    showlegend=True
                )

                fig_json = json.loads(fig.to_json())

                graphs.append({
                    "id": "tab_" + str(label),
                    "title": str(label),
                    "graph": {
                        "data": fig_json["data"],
                        "layout": fig_json["layout"],
                    }
                })

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="tabbed_graph",
                size=1 if current_data is not None else 2,
                params={
                    "graphs": graphs
                },
            )
        return widget_info
