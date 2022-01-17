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


class ProbClassRocCurveWidget(Widget):
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
        # plot roc-curve
        if len(results['utility_columns']['prediction']) <= 2:

            roc_curve = results['metrics'][self.dataset]['roc_curve']
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=roc_curve['fpr'],
                y=roc_curve['tpr'],
                mode='lines',
                name='ROC',
                marker=dict(
                    size=6,
                    color=RED,
                )
            ))

            fig.update_layout(
                yaxis_title="True Positive Rate",
                xaxis_title="False Positive Rate",
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
                additionalGraphs=[],
            )

        else:
            # plot roc-curve
            graphs = []

            for label in results['utility_columns']['prediction']:
                roc_curve = results['metrics'][self.dataset]['roc_curve'][label]
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=roc_curve['fpr'],
                    y=roc_curve['tpr'],
                    mode='lines',
                    name='ROC',
                    marker=dict(
                        size=6,
                        color=RED,
                    )
                ))

                fig.update_layout(
                    yaxis_title="True Positive Rate",
                    xaxis_title="False Positive Rate",
                    showlegend=True
                )

                fig_json = json.loads(fig.to_json())

                graphs.append({
                    "id": f"tab_{label}",
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
