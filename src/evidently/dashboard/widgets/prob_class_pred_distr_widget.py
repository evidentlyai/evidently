#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

from evidently import ColumnMapping
from evidently.analyzers.prob_distribution_analyzer import ProbDistributionAnalyzer
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class ProbClassPredDistrWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbDistributionAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        color_options = self.options_provider.get(ColorOptions)
        results = ProbDistributionAnalyzer.get_results(analyzers_results)
        utility_columns = results.columns.utility_columns

        if (
            isinstance(utility_columns.prediction, str)
            or utility_columns.prediction is None
        ):
            return None

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

        # plot distributions
        graphs = []

        for label in utility_columns.prediction:
            pred_distr = ff.create_distplot(
                [
                    dataset_to_plot[dataset_to_plot[utility_columns.target] == label][
                        label
                    ],
                    dataset_to_plot[dataset_to_plot[utility_columns.target] != label][
                        label
                    ],
                ],
                [str(label), "other"],
                colors=[color_options.primary_color, color_options.secondary_color],
                bin_size=0.05,
                show_curve=False,
                show_rug=True,
            )

            pred_distr.update_layout(
                xaxis_title="Probability",
                yaxis_title="Share",
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )

            pred_distr_json = json.loads(pred_distr.to_json())

            graphs.append(
                {
                    "id": "tab_" + str(label),
                    "title": str(label),
                    "graph": {
                        "data": pred_distr_json["data"],
                        "layout": pred_distr_json["layout"],
                    },
                }
            )

        return BaseWidgetInfo(
            title=self.title,
            type="tabbed_graph",
            size=1 if current_data is not None else 2,
            params={"graphs": graphs},
        )
