#!/usr/bin/env python
# coding: utf-8
from ast import Num
import json
import logging
from numbers import Number
from typing import Optional

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.data_profile_analyzer import DataProfileAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget, GREY, RED, COLOR_DISCRETE_SEQUENCE


class DataProfileFeaturesWidget(Widget):
    def analyzers(self):
        return [DataProfileAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        data_profile_results = DataProfileAnalyzer.get_results(analyzers_results)
        columns = data_profile_results.utility_columns
        target_column = columns.target
        target_type = data_profile_results.ref_features_stats[target_column]['feature_type']
        cat_feature_names = data_profile_results.cat_feature_names
        date_column = columns.date
        self._transform_cat_features(reference_data, cat_feature_names, target_column, target_type)
        # set params data
        params_data = []

        all_features = ([target_column, date_column] + cat_feature_names
                        + data_profile_results.num_feature_names + data_profile_results.datetime_feature_names)
        for feature_name in all_features:
            feature_type = data_profile_results.ref_features_stats[feature_name]['feature_type']
            if feature_name == target_column:
                prefix = ', target'
            else:
                prefix = ''

            params_data.append(
                    {
                        "details": {
                            "parts": self.assemble_parts(target_column, date_column, feature_name, feature_type),
                            "insights": []
                        },
                        "f1": feature_name + prefix,
                        "f2": feature_type,
                        "f3": ' ', #data_profile_results.ref_features_stats[feature_name]['most common value'],
                        "f4": 'graph'
                    }
                )

        # set additionalGraphs
        additional_graphs_data = []

        # add aggregated data column
        freq = self._choose_agg_period(reference_data[date_column])
        reference_data[date_column + '_period'] = reference_data[date_column].dt.to_period(freq=freq)

        # additional graphs data
        for feature_name in all_features:
            feature_type = data_profile_results.ref_features_stats[feature_name]['feature_type']
            if date_column and feature_type != 'date':
                feature_in_time_figure = self._plot_feature_in_time(reference_data, date_column, feature_name, 
                                                                    feature_type)

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_in_time',
                        {
                            "title": "",
                            "size": 2,
                            "text": "",
                            "type": "big_graph",
                            "params":
                                {
                                    "data": feature_in_time_figure['data'],
                                    "layout": feature_in_time_figure['layout']
                                }
                        }
                    )
                )

            if target_column and feature_name!=target_column:
                feature_and_target_figure = self._plot_feature_and_target(reference_data, target_column, target_type,
                                                                   feature_name, feature_type)
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_and_target",
                        {
                            "title": "",
                            "size": 2,
                            "text": "",
                            "type": "big_graph",
                            "params":
                                {
                                    "data": feature_and_target_figure['data'],
                                    "layout": feature_and_target_figure['layout']
                                }
                        }
                    )
                )
            
            if feature_type == 'num':
                most_common_val = data_profile_results.ref_features_stats[feature_name]['most common value']
                most_common_val_rate = data_profile_results.ref_features_stats[feature_name]['most common value (%)']
                feature_views_figure = self._add_representation_of_data(reference_data, feature_name, most_common_val,
                                                                        most_common_val_rate)
            
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_views",
                        {
                            "title": "",
                            "size": 2,
                            "text": "",
                            "type": "big_graph",
                            "params":
                                {
                                    "data": feature_views_figure['data'],
                                    "layout": feature_views_figure['layout']
                                }
                        }
                    )
                )

        return BaseWidgetInfo(
            title='data profile report',
            type="big_table",
            details="",
            alertStats=AlertStats(),
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=2,
            params={
                "rowsPerPage": min(len(all_features), 10),
                "columns": [
                    {
                        "title": "Feature",
                        "field": "f1"
                    },
                    {
                        "title": "Type",
                        "field": "f2"
                    },
                    {
                        "title": "Characteristics",
                        "field": "f3"
                    },
                    {
                        "title": "Picture",
                        "field": "f4"
                    }
                ],
                "data": params_data
            },

            additionalGraphs=additional_graphs_data
        )

    def assemble_parts(self, target_column: str, date_column: str, feature_name: str, feature_type: str) -> list:
        parts = []
        if date_column and feature_type!='date':
            parts.append({
                            "title": feature_name + " in time",
                            "id": feature_name + "_in_time",
                            "type": "widget"
                        })
        if target_column and feature_name!=target_column:
            parts.append({
                            "title": feature_name + " and target",
                            "id": feature_name + "_and_target",
                            "type": "widget"
                        })
        if feature_type=='num':
            parts.append({
                            "title": feature_name + " views",
                            "id": feature_name + "_views",
                            "type": "widget"
                        })
        return parts

    def _plot_feature_in_time(self, df: pd.DataFrame, date_column: str, feature_name: str, feature_type: str) -> json:
        tmp = df[[date_column + '_period', feature_name]].copy()
        if feature_type == 'num':
            tmp = tmp.groupby(date_column + '_period')[feature_name].mean().reset_index()
            tmp[date_column] = tmp[date_column + '_period'].dt.to_timestamp()

            fig = px.line(tmp.sort_values(date_column), y=feature_name, x=date_column, line_shape="spline",
                          render_mode="svg")
            fig.update_traces(line_color='#ed0400')
            feature_in_time_figure = json.loads(fig.to_json())

        elif feature_type == 'cat':
            tmp = tmp.groupby([date_column + '_period', feature_name]).apply(lambda x: x.shape[0])
            tmp.name = 'number of observations'
            tmp = tmp.reset_index()
            tmp[date_column] = tmp[date_column + '_period'].dt.to_timestamp()

            fig = px.bar(tmp.sort_values(date_column), x=date_column, y='number of observations', color=feature_name,
                         color_discrete_sequence=COLOR_DISCRETE_SEQUENCE)
            feature_in_time_figure = json.loads(fig.to_json())

        return feature_in_time_figure

    def _plot_feature_and_target(self, df: pd.DataFrame, target_column: str, target_type:str, feature_name: str,
                                 feature_type: str) -> json:
        if feature_type == 'cat':
            tmp = df[[target_column, feature_name]].copy()
            cats = df[feature_name].dropna().unique().astype(str)
            subplots_num = tmp[feature_name].nunique()
            if target_type == 'num':
                fig = make_subplots(rows=1, cols=subplots_num, shared_yaxes=True)
                for (i, val) in enumerate(cats):
                    trace = go.Histogram(x=df[df[feature_name]==val][target_column], name=val,
                                         marker_color=COLOR_DISCRETE_SEQUENCE[i])
                    fig.append_trace(trace, 1, i+1)
            else:
                tmp = tmp.groupby([target_column, feature_name]).size()
                tmp.name = 'count_objects'
                tmp = tmp.reset_index()
                fig = make_subplots(rows=1, cols=subplots_num, shared_yaxes=True,
                                    subplot_titles=cats)
                for (i, val) in enumerate(cats):
                    trace = go.Bar(x=tmp.loc[tmp[feature_name]==val, target_column],
                                   y=tmp.loc[tmp[feature_name]==val, 'count_objects'],
                                   name=val, marker={'color': COLOR_DISCRETE_SEQUENCE})
                    fig.append_trace(trace, 1, i+1)
                fig.update_layout(showlegend=False)
            feature_and_target_figure = json.loads(fig.to_json())
        else:
            if target_type == 'num':
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df[feature_name], y=df[target_column], mode='markers', 
                              marker=dict(color=RED)))

            else:
                fig = px.strip(df, x=target_column, y=feature_name)
                fig.update_traces(marker=dict(color=RED, size=2))
        feature_and_target_figure = json.loads(fig.to_json())
        return feature_and_target_figure
    
    def _add_representation_of_data(self, df: pd.DataFrame, feature_name: str, most_common_value: Number, 
                                    most_common_value_rate: float) -> json:
        if most_common_value_rate >= 0.6:
            most_common_value_stats = pd.Series(['most common value' if x == most_common_value 
                                                else 'other' for x in df[feature_name]])
            most_common_value_stats = most_common_value_stats.value_counts()

            fig = make_subplots(rows=1, cols=2, shared_yaxes=False, 
                                subplot_titles=['most common value ratio', 
                                                'feature distribution without most common value'])
            trace_1 = go.Bar(x=most_common_value_stats.index.astype(str), y=most_common_value_stats,
                            marker={'color': COLOR_DISCRETE_SEQUENCE})
            fig.append_trace(trace_1, 1, 1)
            trace_2 = go.Histogram(x = df.loc[df[feature_name]!= most_common_value, feature_name],
                                marker={'color': RED})
            fig.append_trace(trace_2, 1, 2)
            fig.update_layout(showlegend=False)

        else:
            fig = go.Figure(data=[go.Histogram(x=df[feature_name], marker={'color': RED})])
            fig.update_xaxes(type="log")
            fig.update_layout(title_text=feature_name + " in log scale")
        
        feature_views_figure = json.loads(fig.to_json())
        return feature_views_figure

    def _transform_cat_features(self, df: pd.DataFrame, cat_feature_names: list[str], target_column: str,
                                target_type: str):
        if target_type == 'cat':
            cat_feature_names = cat_feature_names + [target_column]
        for feature_name in cat_feature_names: 
            if df[feature_name].nunique() > 6:
                cats = df[feature_name].value_counts()[:5].index.astype(str)
                df[feature_name] = df[feature_name].apply(lambda x: x if x in cats else 'other')

    def _choose_agg_period(self, datetime_feature: pd.Series) -> str:
        OPTIMAL_POINTS = 150
        days = (datetime_feature.max() - datetime_feature.min()).days
        time_points = pd.Series(index=['A', 'Q', 'M', 'W', 'D', 'H'],
                                        data=[abs(OPTIMAL_POINTS - days/365), abs(OPTIMAL_POINTS - days/90),
                                              abs(OPTIMAL_POINTS - days/30), abs(OPTIMAL_POINTS - days/7),
                                              abs(OPTIMAL_POINTS - days), abs(OPTIMAL_POINTS - days*24)])
        return time_points.idxmin()

