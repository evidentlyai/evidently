#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd

import numpy as np

import plotly.figure_factory as ff

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget, RED, GREY


class ProbClassPredDistrWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[ProbClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")
            return None
        if self.dataset == 'current':
            dataset_to_plot = current_data.copy(deep=False) if current_data is not None else None
        else:
            dataset_to_plot = reference_data.copy(deep=False)

        if dataset_to_plot is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires reference dataset but it is None")
            return None
        dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
        dataset_to_plot.dropna(axis=0, how='any', inplace=True)

        # plot distributions
        graphs = []

        for label in results['utility_columns']['prediction']:
            pred_distr = ff.create_distplot(
                [
                    dataset_to_plot[dataset_to_plot[results['utility_columns']['target']] == label][label],
                    dataset_to_plot[dataset_to_plot[results['utility_columns']['target']] != label][label]
                ],
                [str(label), "other"],
                colors=[RED, GREY],
                bin_size=0.05,
                show_curve=False,
                show_rug=True
            )

            pred_distr.update_layout(
                xaxis_title="Probability",
                yaxis_title="Share",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            pred_distr_json = json.loads(pred_distr.to_json())

            graphs.append({
                "id": "tab_" + str(label),
                "title": str(label),
                "graph": {
                    "data": pred_distr_json["data"],
                    "layout": pred_distr_json["layout"],
                }
            })

        return BaseWidgetInfo(
            title=self.title,
            type="tabbed_graph",
            size=1 if current_data is not None else 2,
            params={
                "graphs": graphs
            },
        )
