#!/usr/bin/env python
# coding: utf-8
import json
from typing import Optional

import pandas as pd

import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.dashboard.widgets.widget import Widget, RED, GREY


class CatOutputDriftWidget(Widget):
    def __init__(self, title: str, kind: str = 'target'):
        super().__init__(title)
        # check kind values and make private
        self.kind = kind  # target or prediction

    def analyzers(self):
        return [CatTargetDriftAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        results = CatTargetDriftAnalyzer.get_results(analyzers_results)

        if current_data is None:
            raise ValueError("current_data should be present")

        if self.kind == 'target':
            if results.columns.utility_columns.target is None:
                result_metrics = None

            else:
                result_metrics = results.target_metrics

        elif self.kind == 'prediction':
            if results.columns.utility_columns.prediction is None:
                result_metrics = None

            else:
                result_metrics = results.prediction_metrics

        else:
            raise ValueError('kind should be "target" or "prediction" value')

        if not result_metrics:
            return None

        output_name = result_metrics.column_name
        output_p_value = result_metrics.drift
        output_sim_test = "detected" if output_p_value < 0.05 else "not detected"
        # plot output distributions
        fig = go.Figure()

        fig.add_trace(go.Histogram(x=reference_data[output_name],
                                   marker_color=GREY, opacity=0.6, nbinsx=10, name='Reference', histnorm='probability'))

        fig.add_trace(go.Histogram(x=current_data[output_name],
                                   marker_color=RED, opacity=0.6, nbinsx=10, name='Current', histnorm='probability'))

        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis_title=output_name.title(),
            yaxis_title="Share"
        )

        output_drift_json = json.loads(fig.to_json())

        return BaseWidgetInfo(
            title=self.kind.title() + " drift: ".title() + output_sim_test + ", p_value=" + str(
                round(output_p_value, 6)),
            type="big_graph",
            size=2,
            params={
                "data": output_drift_json['data'],
                "layout": output_drift_json['layout']
            }
        )
