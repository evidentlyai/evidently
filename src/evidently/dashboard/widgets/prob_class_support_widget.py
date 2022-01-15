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


class ProbClassSupportWidget(Widget):
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
        # plot support bar
        metrics_matrix = results['metrics'][self.dataset]['metrics_matrix']
        metrics_frame = pd.DataFrame(metrics_matrix)

        fig = go.Figure()

        fig.add_trace(go.Bar(x=metrics_frame.columns.tolist()[:-3],
                             y=metrics_frame.iloc[-1:, :-3].values[0], marker_color=RED, name='Support'))

        fig.update_layout(
            xaxis_title="Class",
            yaxis_title="Number of Objects",
        )

        support_bar_json = json.loads(fig.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1 if current_data is not None else 2,
            params={
                "data": support_bar_json['data'],
                "layout": support_bar_json['layout']
            },
        )
