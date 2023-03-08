#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import (
    ProbClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class ProbClassPredictionCloudWidget(Widget):
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

        # plot clouds
        graphs = []

        for label in utility_columns.prediction:
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=np.random.random(
                        dataset_to_plot[
                            dataset_to_plot[utility_columns.target] == label
                        ].shape[0]
                    ),
                    y=dataset_to_plot[dataset_to_plot[utility_columns.target] == label][
                        label
                    ],
                    mode="markers",
                    name=str(label),
                    marker=dict(size=6, color=color_options.primary_color),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=np.random.random(
                        dataset_to_plot[
                            dataset_to_plot[utility_columns.target] != label
                        ].shape[0]
                    ),
                    y=dataset_to_plot[dataset_to_plot[utility_columns.target] != label][
                        label
                    ],
                    mode="markers",
                    name="other",
                    marker=dict(size=6, color=color_options.secondary_color),
                )
            )

            fig.update_layout(
                yaxis_title="Probability",
                xaxis=dict(range=(-2, 3), showticklabels=False),
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

        return BaseWidgetInfo(
            title=self.title,
            type="tabbed_graph",
            details="",
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=1 if current_data is not None else 2,
            params={"graphs": graphs},
            additionalGraphs=[],
        )
