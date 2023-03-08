#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.figure_factory as ff

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import (
    ClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class ClassConfMatrixWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ClassificationPerformanceAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        results = ClassificationPerformanceAnalyzer.get_results(analyzers_results)

        if (
            results.columns.utility_columns.target is None
            or results.columns.utility_columns.prediction is None
        ):
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] required 'target' or 'prediction' column to be set"
                )
            return None

        if self.dataset == "current":
            result_metrics = results.current_metrics

        elif self.dataset == "reference":
            result_metrics = results.reference_metrics

        else:
            raise ValueError(
                f"Widget [{self.title}] required '{self.dataset}' results from"
                f" {ClassificationPerformanceAnalyzer.__name__} but no data found"
            )

        if result_metrics is None:
            return None

        # plot confusion matrix
        conf_matrix = result_metrics.confusion_matrix.values
        labels = result_metrics.confusion_matrix.labels
        z = [[int(y) for y in x] for x in conf_matrix]

        # change each element of z to type string for annotations
        z_text = [[str(y) for y in x] for x in z]

        fig = ff.create_annotated_heatmap(
            z,
            x=labels,
            y=labels,
            annotation_text=z_text,
            colorscale="bluered",
            showscale=True,
        )

        fig.update_layout(xaxis_title="Predicted value", yaxis_title="Actual value")

        conf_matrix_json = json.loads(fig.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1 if current_data is not None else 2,
            params={
                "data": conf_matrix_json["data"],
                "layout": conf_matrix_json["layout"],
            },
            additionalGraphs=[],
        )
