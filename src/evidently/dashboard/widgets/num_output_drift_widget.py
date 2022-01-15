#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.figure_factory as ff

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.dashboard.widgets.widget import Widget, GREY, RED


class NumOutputDriftWidget(Widget):
    def __init__(self, title: str, kind: str = 'target'):
        super().__init__(title)
        self.kind = kind  # target or prediction

    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[NumTargetDriftAnalyzer]

        if current_data is None:
            raise ValueError("current_data should be present")

        if results['utility_columns'][self.kind] is None:
            return None
        # calculate output drift
        output_p_value = results['metrics'][self.kind + '_drift']
        output_sim_test = "detected" if output_p_value < 0.05 else "not detected"

        # plot output distributions
        output_distr = ff.create_distplot(
            [reference_data[results['utility_columns'][self.kind]],
             current_data[results['utility_columns'][self.kind]]],
            ["Reference", "Current"],
            colors=[GREY, RED],
            show_rug=True)

        output_distr.update_layout(
            xaxis_title="Value",
            yaxis_title="Share",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        output_drift_json = json.loads(output_distr.to_json())

        return BaseWidgetInfo(
            title=self.kind.title() + " drift: ".title() + output_sim_test + ", p_value=" + str(
                round(output_p_value, 6)),
            type="big_graph",
            details="",
            alertStats=AlertStats(),
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=2,
            params={
                "data": output_drift_json['data'],
                "layout": output_drift_json['layout']
            },
            additionalGraphs=[],
        )
