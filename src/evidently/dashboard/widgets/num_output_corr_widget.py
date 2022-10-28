#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd
import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.dashboard.widgets.utils import fig_to_json
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class NumOutputCorrWidget(Widget):
    def __init__(self, title: str, kind: str = "target"):
        super().__init__(title)
        self.title = title
        self.kind = kind  # target or prediction

    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        color_options = self.options_provider.get(ColorOptions)
        results = NumTargetDriftAnalyzer.get_results(analyzers_results)

        if self.kind == "target":
            if results.columns.utility_columns.target is None:
                return None

            metrics = results.target_metrics

        elif self.kind == "prediction":
            if results.columns.utility_columns.prediction is None:
                return None

            metrics = results.prediction_metrics

        else:
            raise ValueError(
                f"Widget [{self.title}] requires 'target' or 'prediction' kind parameter value"
            )

        if metrics is None:
            return None

        # calculate corr
        ref_output_corr = metrics.reference_correlations

        if ref_output_corr is None:
            return None

        current_output_corr = metrics.current_correlations

        if current_output_corr is None:
            return None

        # plot output correlations
        output_corr = go.Figure()

        output_corr.add_trace(
            go.Bar(
                y=list(ref_output_corr.values()),
                x=list(ref_output_corr.keys()),
                marker_color=color_options.get_reference_data_color(),
                name="Reference",
            )
        )

        output_corr.add_trace(
            go.Bar(
                y=list(current_output_corr.values()),
                x=list(current_output_corr.keys()),
                marker_color=color_options.get_current_data_color(),
                name="Current",
            )
        )

        output_corr.update_layout(
            xaxis_title="Features",
            yaxis_title="Correlation",
            yaxis=dict(range=(-1, 1), showticklabels=True),
        )

        # output_corr_json = json.loads(output_corr.to_json())
        output_corr_json = fig_to_json(output_corr)

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": output_corr_json["data"],
                "layout": output_corr_json["layout"],
            },
        )
