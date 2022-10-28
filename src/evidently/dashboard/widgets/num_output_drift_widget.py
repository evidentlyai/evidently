#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd
import plotly.figure_factory as ff

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.dashboard.widgets.utils import CutQuantileTransformer
from evidently.dashboard.widgets.utils import fig_to_json
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions
from evidently.options import QualityMetricsOptions


class NumOutputDriftWidget(Widget):
    def __init__(self, title: str, kind: str = "target"):
        super().__init__(title)
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
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        cut_quantile = quality_metrics_options.cut_quantile

        if current_data is None:
            raise ValueError("current_data should be present")

        if self.kind == "target":
            if results.columns.utility_columns.target is None:
                return None

            column_name = results.columns.utility_columns.target
            metrics = results.target_metrics

        elif self.kind == "prediction":
            if results.columns.utility_columns.prediction is None:
                return None

            if not isinstance(results.columns.utility_columns.prediction, str):
                raise ValueError(
                    f"Widget [{self.title}] requires one str value for 'prediction' column"
                )

            column_name = results.columns.utility_columns.prediction
            metrics = results.prediction_metrics

        else:
            raise ValueError(
                f"Widget [{self.title}] requires 'target' or 'prediction' kind parameter value"
            )

        if metrics is None:
            return None

        # calculate output drift
        stattest_name = metrics.stattest_name
        drift_score = metrics.drift_score
        drift_detected = metrics.drift_detected
        output_sim_test = "detected" if drift_detected else "not detected"

        # plot output distributions
        quantile = quality_metrics_options.get_cut_quantile(column_name)
        if cut_quantile and quantile is not None:
            side, q = quantile
            cqt = CutQuantileTransformer(side=side, q=q)
            cqt.fit(reference_data[column_name])
            reference_data_to_plot = cqt.transform(reference_data[column_name])
            current_data_to_plot = cqt.transform(current_data[column_name])
        else:
            reference_data_to_plot = reference_data[column_name]
            current_data_to_plot = current_data[column_name]

        output_distr = ff.create_distplot(
            [reference_data_to_plot, current_data_to_plot],
            ["Reference", "Current"],
            colors=[
                color_options.get_reference_data_color(),
                color_options.get_current_data_color(),
            ],
            show_rug=True,
        )

        output_distr.update_layout(
            xaxis_title="Value",
            yaxis_title="Share",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        # output_drift_json = json.loads(output_distr.to_json())
        output_drift_json = fig_to_json(output_distr)

        return BaseWidgetInfo(
            title=f"{self.kind.title()} Drift: {output_sim_test},"
            f" drift score={round(drift_score, 6)} ({stattest_name})",
            type="big_graph",
            details="",
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=2,
            params={
                "data": output_drift_json["data"],
                "layout": output_drift_json["layout"],
            },
            additionalGraphs=[],
        )
