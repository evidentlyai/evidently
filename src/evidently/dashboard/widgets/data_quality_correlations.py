#!/usr/bin/env python
# coding: utf-8
import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo


class DataQualityCorrelationsWidget(Widget):
    period_prefix: str

    def analyzers(self):
        return [DataQualityAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:

        data_quality_results = DataQualityAnalyzer.get_results(analyzers_results)
        is_current_data = current_data is not None
        reference_correlations = data_quality_results.reference_correlations
        if is_current_data:
            current_correlations = data_quality_results.current_correlations
        else:
            current_correlations = None

        additional_graphs = []
        parts = []
        for kind in ["pearson", "spearman", "kendall", "cramer_v"]:
            if reference_correlations[kind].shape[0] > 1:
                correlation_figure = self._plot_correlation_figure(kind, reference_correlations, current_correlations)
                additional_graphs.append(
                    AdditionalGraphInfo(
                        kind,
                        {
                            "data": correlation_figure["data"],
                            "layout": correlation_figure["layout"],
                        },
                    )
                )

                parts.append({"title": kind, "id": kind})

        if is_current_data:
            metrics_values_headers = [
                "top 5 correlation diff category (Cramer_V)",
                "value ref",
                "value curr",
                "difference",
                "top 5 correlation diff numerical (Spearman)",
                "value ref",
                "value curr",
                "difference",
            ]

        else:
            metrics_values_headers = [
                "top 5 correlated category (Cramer_V)",
                "Value",
                "top 5 correlated numerical (Spearman)",
                "Value",
            ]

        metrics = self._make_metrics(reference_correlations, current_correlations)

        wi = BaseWidgetInfo(
            type="rich_data",
            title="",
            size=2,
            params={
                "header": "Correlations",
                "description": "",
                "metricsValuesHeaders": metrics_values_headers,
                "metrics": metrics,
                "details": {"parts": parts, "insights": []},
            },
            additionalGraphs=additional_graphs,
        )

        return wi

    def _plot_correlation_figure(
        self, kind: str, reference_correlations: dict, current_correlations: Optional[dict]
    ) -> dict:
        columns = reference_correlations[kind].columns
        heatmap_text = None
        heatmap_texttemplate = None
        if current_correlations is not None:
            cols = 2
            subplot_titles = ["reference", "current"]
        else:
            cols = 1
            subplot_titles = [""]

        fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)
        if len(columns) < 15:
            heatmap_text = np.round(reference_correlations[kind], 2).astype(str)
            heatmap_texttemplate = "%{text}"

        trace = go.Heatmap(
            z=reference_correlations[kind],
            x=columns,
            y=columns,
            text=heatmap_text,
            texttemplate=heatmap_texttemplate,
            coloraxis="coloraxis",
        )
        fig.add_trace(trace, 1, 1)
        if current_correlations is not None:
            if len(columns) < 15:
                heatmap_text = np.round(current_correlations[kind], 2).astype(str)
                heatmap_texttemplate = "%{text}"

            trace = go.Heatmap(
                z=current_correlations[kind],
                x=columns,
                y=columns,
                text=heatmap_text,
                texttemplate=heatmap_texttemplate,
                coloraxis="coloraxis",
            )
            fig.add_trace(trace, 1, 2)
        fig.update_layout(coloraxis={"colorscale": "RdBu_r"})
        correlation_figure = json.loads(fig.to_json())
        return correlation_figure

    def _get_df_corr_features_sorted(self, df_corr: pd.DataFrame) -> pd.DataFrame:
        df_corr = df_corr.stack().reset_index()
        df_corr.columns = ["col_1", "col_2", "value"]
        df_corr["value"] = np.round(df_corr["value"], 3)
        df_corr["abs_value"] = np.abs(df_corr["value"])
        df_corr = df_corr.sort_values(["col_1", "col_2"])
        df_corr["keep"] = df_corr["col_1"].str.get(0) < df_corr["col_2"].str.get(0)
        df_corr = df_corr[df_corr["keep"]]
        df_corr = df_corr.sort_values("abs_value", ascending=False)
        df_corr["features"] = df_corr["col_1"] + ", " + df_corr["col_2"]
        return df_corr[["features", "value"]]

    def _get_rel_diff_corr_features_sorted(self, ref_corr: pd.DataFrame, curr_corr: pd.DataFrame) -> pd.DataFrame:
        ref_corr = self._get_df_corr_features_sorted(ref_corr).rename(columns={"value": "value_ref"})
        curr_corr = self._get_df_corr_features_sorted(curr_corr).rename(columns={"value": "value_curr"})
        com_corr = ref_corr.merge(curr_corr, on="features", how="left")
        com_corr["value_diff"] = np.round((com_corr["value_ref"] - com_corr["value_curr"]), 3)
        com_corr["abs_value_diff"] = np.abs(com_corr["value_diff"])
        com_corr = com_corr.sort_values("abs_value_diff", ascending=False)
        return com_corr[["features", "value_ref", "value_curr", "value_diff"]]

    def _make_metrics(self, reference_correlations: dict, current_correlations: Optional[dict]):
        metrics = []
        if current_correlations is not None:
            if reference_correlations["spearman"].shape[0] > 1:
                com_num_corr = self._get_rel_diff_corr_features_sorted(
                    reference_correlations["spearman"], current_correlations["spearman"]
                )
            else:
                com_num_corr = pd.DataFrame()
            if reference_correlations["cramer_v"].shape[0] > 1:
                com_cat_corr = self._get_rel_diff_corr_features_sorted(
                    reference_correlations["cramer_v"], current_correlations["cramer_v"]
                )
            else:
                com_cat_corr = pd.DataFrame()
            for i in range(5):
                values = ["-", "-", "-", "-", "-", "-", "-", "-"]
                if i < com_cat_corr.shape[0]:
                    values[0] = com_cat_corr.iloc[i, 0]
                    values[1] = com_cat_corr.iloc[i, 1]
                    values[2] = com_cat_corr.iloc[i, 2]
                    values[3] = com_cat_corr.iloc[i, 3]
                if i < com_num_corr.shape[0]:
                    values[4] = com_num_corr.iloc[i, 0]
                    values[5] = com_num_corr.iloc[i, 1]
                    values[6] = com_num_corr.iloc[i, 2]
                    values[7] = com_num_corr.iloc[i, 3]
                metrics.append(
                    {"label": "", "values": values},
                )
        else:
            if reference_correlations["spearman"].shape[0] > 0:
                ref_num_corr = self._get_df_corr_features_sorted(reference_correlations["spearman"])
            else:
                ref_num_corr = pd.DataFrame()
            if reference_correlations["cramer_v"].shape[0] > 0:
                ref_cat_corr = self._get_df_corr_features_sorted(reference_correlations["cramer_v"])
            else:
                ref_cat_corr = pd.DataFrame()
            for i in range(5):
                values = ["-", "-", "-", "-"]
                if i < ref_cat_corr.shape[0]:
                    values[0] = ref_cat_corr.iloc[i, 0]
                    values[1] = ref_cat_corr.iloc[i, 1]
                if i < ref_num_corr.shape[0]:
                    values[2] = ref_num_corr.iloc[i, 0]
                    values[3] = ref_num_corr.iloc[i, 1]
                metrics.append(
                    {"label": "", "values": values},
                )
        return metrics
