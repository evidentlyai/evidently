#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import numpy as np

import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget, GREY, RED
from evidently.dashboard.widgets.utils import CutQuantileTransformer
from evidently.options import DataDriftOptions, QualityMetricsOptions


class DataDriftTableWidget(Widget):
    def analyzers(self):
        return [DataDriftAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        data_drift_results = DataDriftAnalyzer.get_results(analyzers_results)
        all_features = data_drift_results.get_all_features_list()
        date_column = data_drift_results.utility_columns.date

        if current_data is None:
            raise ValueError("current_data should be present")

        # set params data
        params_data = []
        data_drift_options = self.options_provider.get(DataDriftOptions)
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        conf_interval_n_sigmas = quality_metrics_options.conf_interval_n_sigmas
        for feature_name in all_features:
            current_small_hist = data_drift_results.metrics.features[feature_name].current_small_hist
            ref_small_hist = data_drift_results.metrics.features[feature_name].ref_small_hist
            feature_type = data_drift_results.metrics.features[feature_name].feature_type
            p_value = data_drift_results.metrics.features[feature_name].p_value
            feature_confidence = data_drift_options.get_confidence(feature_name)
            distr_sim_test = "Detected" if p_value < (1. - feature_confidence) else "Not Detected"

            params_data.append(
                {
                    "details": {
                        "parts": [
                            {
                                "title": "Data drift",
                                "id": feature_name + "_drift",
                                "type": "widget"
                            },
                            {
                                "title": "Data distribution",
                                "id": feature_name + "_distr"
                            }
                        ],
                        "insights": []
                    },
                    "f1": feature_name,
                    "f6": feature_type,
                    "f3": {
                        "x": list(ref_small_hist[1]),
                        "y": list(ref_small_hist[0])
                    },
                    "f4": {
                        "x": list(current_small_hist[1]),
                        "y": list(current_small_hist[0])
                    },
                    "f2": distr_sim_test,
                    "f5": round(p_value, 6)
                }
            )

        # set additionalGraphs
        additional_graphs_data = []
        xbins = data_drift_options.xbins
        cut_quantile = quality_metrics_options.cut_quantile
        for feature_name in all_features:
            # plot distributions
            fig = go.Figure()
            if xbins and xbins.get(feature_name):
                current_xbins = xbins.get(feature_name)
                current_nbinsx = None
            else:
                current_xbins = None
                current_nbinsx = data_drift_options.get_nbinsx(feature_name)
            if cut_quantile and quality_metrics_options.get_cut_quantile(feature_name):
                side, q = quality_metrics_options.get_cut_quantile(feature_name)
                cqt = CutQuantileTransformer(side=side, q=q)
                cqt.fit(reference_data[feature_name])
                reference_data_to_plot = cqt.transform(reference_data[feature_name])
                current_data_to_plot = cqt.transform(current_data[feature_name])
            else:
                reference_data_to_plot = reference_data[feature_name]
                current_data_to_plot = current_data[feature_name]
            fig.add_trace(go.Histogram(x=reference_data_to_plot,
                                       marker_color=GREY,
                                       opacity=0.6,
                                       xbins=current_xbins,
                                       nbinsx=current_nbinsx,
                                       name='Reference',
                                       histnorm='probability'))

            fig.add_trace(go.Histogram(x=current_data_to_plot,
                                       marker_color=RED,
                                       opacity=0.6,
                                       xbins=current_xbins,
                                       nbinsx=current_nbinsx,
                                       name='Current',
                                       histnorm='probability'))
            fig.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                xaxis_title=feature_name,
                yaxis_title="Share"
            )

            distr_figure = json.loads(fig.to_json())

            # plot drift
            reference_mean = np.mean(reference_data[feature_name][np.isfinite(reference_data[feature_name])])
            reference_std = np.std(reference_data[feature_name][np.isfinite(reference_data[feature_name])], ddof=1)
            x_title = "Timestamp" if date_column else "Index"

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=current_data[date_column] if date_column else current_data.index,
                y=current_data[feature_name],
                mode='markers',
                name='Current',
                marker=dict(
                    size=6,
                    color=GREY
                )
            ))

            if date_column:
                x0 = current_data[date_column].sort_values()[1]
            else:
                x0 = current_data.index.sort_values()[1]

            fig.add_trace(go.Scatter(
                x=[x0, x0],
                y=[reference_mean - conf_interval_n_sigmas * reference_std,
                    reference_mean + conf_interval_n_sigmas * reference_std],
                mode='markers',
                name='Current',
                marker=dict(
                    size=0.01,
                    color='white',
                    opacity=0.005
                ),
                showlegend=False
            ))

            fig.update_layout(
                xaxis_title=x_title,
                yaxis_title=feature_name,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                shapes=[
                    dict(
                        type="rect",
                        # x-reference is assigned to the x-values
                        xref="paper",
                        # y-reference is assigned to the plot paper [0,1]
                        yref="y",
                        x0=0,
                        y0=reference_mean - conf_interval_n_sigmas * reference_std,
                        x1=1,
                        y1=reference_mean + conf_interval_n_sigmas * reference_std,
                        fillcolor="LightGreen",
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    dict(
                        type="line",
                        name='Reference',
                        xref="paper",
                        yref="y",
                        x0=0,  # min(testset_agg_by_date.index),
                        y0=reference_mean,
                        x1=1,  # max(testset_agg_by_date.index),
                        y1=reference_mean,
                        line=dict(
                            color="Green",
                            width=3
                        )
                    ),
                ]
            )

            drift_figure = json.loads(fig.to_json())

            # add distributions data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_distr',
                    {
                        "data": distr_figure['data'],
                        "layout": distr_figure['layout']
                    }
                )
            )

            # add drift data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_drift',
                    {
                        "title": "",
                        "size": 2,
                        "text": "",
                        "type": "big_graph",
                        "params":
                            {
                                "data": drift_figure['data'],
                                "layout": drift_figure['layout']
                            }
                    }
                )
            )
        n_drifted_features = data_drift_results.metrics.n_drifted_features
        dataset_drift = data_drift_results.metrics.dataset_drift
        n_features = data_drift_results.metrics.n_features
        drift_share = data_drift_results.metrics.share_drifted_features

        title_prefix = f'Drift is detected for {drift_share * 100:.2f}% of features ({n_drifted_features}' \
                       f' out of {n_features}). '
        title_suffix = 'Dataset Drift is detected.' if dataset_drift else 'Dataset Drift is NOT detected.'

        return BaseWidgetInfo(
            title=title_prefix + title_suffix,
            type="big_table",
            details="",
            alertStats=AlertStats(),
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=2,
            params={
                "rowsPerPage": min(n_features, 10),
                "columns": [
                    {
                        "title": "Feature",
                        "field": "f1"
                    },
                    {
                        "title": "Type",
                        "field": "f6"
                    },
                    {
                        "title": "Reference Distribution",
                        "field": "f3",
                        "type": "histogram",
                        "options": {
                            "xField": "x",
                            "yField": "y"
                        }
                    },
                    {
                        "title": "Current Distribution",
                        "field": "f4",
                        "type": "histogram",
                        "options": {
                            "xField": "x",
                            "yField": "y"
                        }
                    },
                    {
                        "title": "Data drift",
                        "field": "f2"
                    },
                    {
                        "title": "P-Value for Similarity Test",
                        "field": "f5",
                        "sort": "asc"
                    }
                ],
                "data": params_data
            },

            additionalGraphs=additional_graphs_data
        )
