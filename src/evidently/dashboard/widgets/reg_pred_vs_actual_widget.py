#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import (
    RegressionPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class RegPredActualWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [RegressionPerformanceAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        color_options = self.options_provider.get(ColorOptions)
        results = RegressionPerformanceAnalyzer.get_results(analyzers_results)

        target_name = results.columns.utility_columns.target
        prediction_name = results.columns.utility_columns.prediction

        if target_name is None or prediction_name is None:
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires 'target' and 'prediction' columns"
                )

            return None

        if self.dataset == "current":
            dataset_to_plot = (
                current_data.copy(deep=False) if current_data is not None else None
            )

        else:
            dataset_to_plot = reference_data.copy(deep=False)

        if dataset_to_plot is None:
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires reference dataset but it is None"
                )

            return None

        dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
        dataset_to_plot.dropna(
            axis=0, how="any", inplace=True, subset=[target_name, prediction_name]
        )

        # plot output correlations
        pred_actual = go.Figure()

        pred_actual.add_trace(
            go.Scatter(
                x=dataset_to_plot[target_name],
                y=dataset_to_plot[prediction_name],
                mode="markers",
                name=self.dataset.title(),
                marker=dict(color=color_options.primary_color, showscale=False),
            )
        )

        pred_actual.update_layout(
            xaxis_title="Actual value",
            yaxis_title="Predicted value",
            xaxis=dict(showticklabels=True),
            yaxis=dict(showticklabels=True),
        )

        pred_actual_json = json.loads(pred_actual.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": pred_actual_json["data"],
                "layout": pred_actual_json["layout"],
            },
        )
