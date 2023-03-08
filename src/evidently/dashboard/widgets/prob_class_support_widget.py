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


class ProbClassSupportWidget(Widget):
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

        # plot support bar
        metrics_matrix = metrics.metrics_matrix
        metrics_frame = pd.DataFrame(metrics_matrix)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=metrics_frame.columns.tolist()[:-3],
                y=metrics_frame.iloc[-1:, :-3].values[0],
                marker_color=color_options.primary_color,
                name="Support",
            )
        )

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
                "data": support_bar_json["data"],
                "layout": support_bar_json["layout"],
            },
        )
