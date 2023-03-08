#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import (
    ProbClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class ProbClassMetricsMatrixWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.title = title
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

        z = metrics_frame.iloc[:-1, :-3].values
        x = metrics.confusion_matrix.labels
        y = ["precision", "recall", "f1-score"]

        if len(utility_columns.prediction) > 2:
            roc_aucs = metrics.roc_aucs
            z = np.append(z, [roc_aucs], axis=0)
            y.append("roc-auc")

        # change each element of z to type string for annotations
        z_text = [[str(round(y, 3)) for y in x] for x in z]

        # set up figure
        fig = ff.create_annotated_heatmap(
            z, y=y, x=x, annotation_text=z_text, colorscale="bluered", showscale=True
        )
        fig.update_layout(xaxis_title="Class", yaxis_title="Metric")

        metrics_matrix_json = json.loads(fig.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1 if current_data is not None else 2,
            params={
                "data": metrics_matrix_json["data"],
                "layout": metrics_matrix_json["layout"],
            },
        )
