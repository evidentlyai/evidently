#!/usr/bin/env python
# coding: utf-8
import json
from typing import Optional, List

import pandas as pd
import numpy as np

import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer, DataDriftAnalyzerFeatureMetrics
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget, GREY, RED
from evidently.dashboard.widgets.utils import CutQuantileTransformer
from evidently.options import DataDriftOptions, QualityMetricsOptions


def _generate_feature_params(name: str, data: DataDriftAnalyzerFeatureMetrics, confidence: float) -> dict:
    current_small_hist = data.current_small_hist
    ref_small_hist = data.ref_small_hist
    feature_type = data.feature_type
    p_value = data.p_value
    distr_sim_test = "Detected" if p_value < (1. - confidence) else "Not Detected"
    parts = []
    if data.feature_type == "num":
        parts.append({
            "title": "Data drift",
            "id": f"{name}_drift",
            "type": "widget"
        })
    parts.append({
        "title": "Data distribution",
        "id": f"{name}_distr"
    })
    return {
        "details": {
            "parts": parts,
            "insights": []
        },
        "f1": name,
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


def _generate_additional_graph_num_feature(name: str,
                                           reference_data: pd.DataFrame,
                                           current_data: pd.DataFrame,
                                           date_column: Optional[str],
                                           data_drift_options: DataDriftOptions,
                                           quality_metrics_options: QualityMetricsOptions) -> List[AdditionalGraphInfo]:
    # plot distributions
    conf_interval_n_sigmas = quality_metrics_options.conf_interval_n_sigmas
    fig = go.Figure()
    if data_drift_options.xbins and data_drift_options.xbins.get(name):
        current_xbins = data_drift_options.xbins.get(name)
        current_nbinsx = None
    else:
        current_xbins = None
        current_nbinsx = data_drift_options.get_nbinsx(name)
    quantiles = quality_metrics_options.get_cut_quantile(name)
    if quantiles:
        side, q = quantiles
        cqt = CutQuantileTransformer(side=side, q=q)
        cqt.fit(reference_data[name])
        reference_data_to_plot = cqt.transform(reference_data[name])
        current_data_to_plot = cqt.transform(current_data[name])
    else:
        reference_data_to_plot = reference_data[name]
        current_data_to_plot = current_data[name]
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
        xaxis_title=name,
        yaxis_title="Share"
    )

    distr_figure = json.loads(fig.to_json())

    # plot drift
    reference_mean = np.mean(reference_data[name][np.isfinite(reference_data[name])])
    reference_std = np.std(reference_data[name][np.isfinite(reference_data[name])], ddof=1)
    x_title = "Timestamp" if date_column else "Index"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=current_data[date_column] if date_column else current_data.index,
        y=current_data[name],
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
        yaxis_title=name,
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
    return [
        AdditionalGraphInfo(
            f'{name}_distr',
            {
                "data": distr_figure['data'],
                "layout": distr_figure['layout']
            }
        ),
        AdditionalGraphInfo(
            f'{name}_drift',
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
        )]


def _generate_additional_graph_cat_feature(name: str,
                                           reference_data: pd.DataFrame,
                                           current_data: pd.DataFrame) -> List[AdditionalGraphInfo]:
    fig = go.Figure()
    feature_ref_data = reference_data[name].dropna()
    feature_cur_data = current_data[name].dropna()
    reference_data_to_plot = list(reversed(list(map(list, zip(*feature_ref_data.value_counts().items())))))
    current_data_to_plot = list(reversed(list(map(list, zip(*feature_cur_data.value_counts().items())))))
    fig.add_trace(go.Bar(x=reference_data_to_plot[1],
                         y=reference_data_to_plot[0],
                         marker_color=GREY,
                         opacity=0.6,
                         name='Reference'))

    fig.add_trace(go.Bar(x=current_data_to_plot[1],
                         y=current_data_to_plot[0],
                         marker_color=RED,
                         opacity=0.6,
                         name='Current'))
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_title=name,
        yaxis_title="Share"
    )

    distr_figure = json.loads(fig.to_json())
    return [AdditionalGraphInfo(
        f'{name}_distr',
        {
            "data": distr_figure['data'],
            "layout": distr_figure['layout']
        }
    )]


class DataDriftTableWidget(Widget):
    def analyzers(self):
        return [DataDriftAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        data_drift_results = DataDriftAnalyzer.get_results(analyzers_results)
        all_features = data_drift_results.columns.get_all_features_list()
        date_column = data_drift_results.columns.utility_columns.date

        if current_data is None:
            raise ValueError("current_data should be present")

        # set params data
        params_data = []
        data_drift_options = self.options_provider.get(DataDriftOptions)
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        for feature_name in all_features:
            feature_confidence = data_drift_options.get_confidence(feature_name)
            params_data.append(_generate_feature_params(feature_name,
                                                        data_drift_results.metrics.features[feature_name],
                                                        feature_confidence))

        # set additionalGraphs
        additional_graphs_data = []
        for feature_name in all_features:
            # plot distributions
            if data_drift_results.metrics.features[feature_name].feature_type == "num":
                additional_graphs_data += _generate_additional_graph_num_feature(
                    feature_name,
                    reference_data,
                    current_data,
                    date_column,
                    data_drift_options,
                    quality_metrics_options)
            elif data_drift_results.metrics.features[feature_name].feature_type == "cat":
                additional_graphs_data += _generate_additional_graph_cat_feature(
                    feature_name,
                    reference_data,
                    current_data)
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
